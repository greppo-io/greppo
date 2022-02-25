import ast
import io
import json
import logging
import pathlib
import secrets
import sys
from _ast import Assign
from _ast import Attribute
from _ast import Call
from _ast import keyword
from _ast import Load
from _ast import Name
from _ast import Store
from ast import Str
from contextlib import redirect_stdout
from typing import Any, Dict

from greppo import GreppoAppProxy
from .input_types import GreppoInputsNames, GreppoChartNames

logger = logging.getLogger('user_script_utils')


class RenameGreppoAppTransformer(ast.NodeTransformer):
    def __init__(self, hash_prefix):
        super().__init__()

        self.hash_prefix = hash_prefix

    def visit_Name(self, node):
        if node.id == "app":
            node.id = self.hash_prefix + "_app"

        return node


def append_send_data_method(code):
    code.body.append(
        Assign(
            targets=[Name(ctx=Store(), id="gpo_payload")],
            type_comment=None,
            value=Call(
                args=[],
                func=Attribute(
                    attr=GreppoAppProxy.gpo_prepare_data.__name__,
                    ctx=Load(),
                    value=Name(ctx=Load(), id="app"),
                ),
                keywords=[],
            ),
        )
    )

    return code


def append_raster_reference(code):
    code.body.append(
        Assign(
            targets=[Name(ctx=Store(), id="gpo_raster_reference_payload")],
            type_comment=None,
            value=Call(
                args=[],
                func=Attribute(
                    attr=GreppoAppProxy.gpo_reference_data.__name__,
                    ctx=Load(),
                    value=Name(ctx=Load(), id="app"),
                ),
                keywords=[],
            ),
        )
    )

    return code


class AddInputUpdatesToGpoVariableAndGetValueTransformer(ast.NodeTransformer):
    def __init__(self, input_updates: Dict[str, Any], hex_token_generator):
        super().__init__()

        self.input_updates = input_updates

        self.hex_token_generator = hex_token_generator

        self.greppo_input_calls = []

    def visit_Call(self, node):
        if not hasattr(node.func, "attr"):
            return node

        if node.func.attr not in GreppoInputsNames:
            return node

        # ==== Find name value for gpo variable and set name prefix
        for node_kwargs in node.keywords:
            if node_kwargs.arg == "name":
                string_container = node_kwargs.value  ## 3.6 uses an object called Str that has `s` instead of `value`.
                if type(string_container) == Str:
                    name = string_container.s
                else:
                    name = string_container.value

                input_name = self.hex_token_generator(nbytes=4) + "_" + name

                if type(string_container) == Str:
                    node_kwargs.value.s = input_name
                else:
                    node_kwargs.value.value = input_name

                break

        # ==== Add input_updates to the ctr.
        input_updates_kwarg = keyword(
            arg='input_updates',
            value=ast.parse(json.dumps(self.input_updates)).body[0].value
        )
        node.keywords.append(input_updates_kwarg)

        # ==== Create new Call node for get_value
        z = Call(args=[],
                    func=Attribute(
                        attr='get_value',
                        ctx=Load(),
                        value=node
                    ),
                    keywords=[])

        return z


class AddHexPrefixForCharts(ast.NodeTransformer):
    def __init__(self, input_updates, hex_token_generator):
        super().__init__()

        self.input_updates = input_updates

        self.hex_token_generator = hex_token_generator

    def visit_Call(self, node):
        if not hasattr(node.func, "attr"):
            return node

        if node.func.attr not in GreppoChartNames:
            return node

        # ==== Find all names for gpo_inputs and set hex id
        for node_kwargs in node.keywords:
            if node_kwargs.arg == "name":
                string_container = node_kwargs.value  ## 3.6 uses an object called Str that has `s` instead of `value`.
                if type(string_container) == Str:
                    input_name = string_container.s
                else:
                    input_name = string_container.value

                input_name = self.hex_token_generator(nbytes=4) + "_" + input_name

                if type(string_container) == Str:
                    node_kwargs.value.s = input_name
                else:
                    node_kwargs.value.value = input_name

                break

        input_updates_ast = ast.parse(str(self.input_updates)).body[0]
        if not hasattr(input_updates_ast, 'value'):
            raise Exception("Cannot parse input_updates: {}", self.input_updates)

        input_updates_keyword = keyword(
            arg="input_updates", value=input_updates_ast.value
        )

        # ==== Add input updates to node
        updated = False
        for pos, k in enumerate(node.keywords):
            if k.arg == "input_updates":
                node.keywords[pos] = input_updates_keyword
                updated = True
                break
        if not updated:
            node.keywords.append(input_updates_keyword)

        return node


def run_script(script_name, input_updates, hex_token_generator):
    script_dir = str(pathlib.Path(script_name).parent)

    with open(script_name) as f:
        lines = f.read()
        user_code = ast.parse(lines, script_name)

        add_input_updates_to_gpo_variable_and_get_value_t = AddInputUpdatesToGpoVariableAndGetValueTransformer(
            input_updates=input_updates, hex_token_generator=hex_token_generator
        )
        add_input_updates_to_gpo_variable_and_get_value_t.visit(user_code)
        ast.fix_missing_locations(
            user_code
        )

        transformer = AddHexPrefixForCharts(
            input_updates=input_updates, hex_token_generator=hex_token_generator
        )
        transformer.visit(user_code)
        ast.fix_missing_locations(
            user_code
        )

        user_code = append_send_data_method(user_code)
        user_code = append_raster_reference(user_code)

        # Transform gpo for locals() injection
        hash_prefix = hex_token_generator(nbytes=4)
        gpo_transformer = RenameGreppoAppTransformer(hash_prefix=hash_prefix)
        gpo_transformer.visit(user_code)

        ast.fix_missing_locations(user_code)

        gpo_app = GreppoAppProxy()

        locals_copy = locals().copy()
        locals_copy['app'] = gpo_app
        locals_copy[hash_prefix + "_app"] = gpo_app

        #logger.debug('\n\n------ Code Transform ------\n')
        #logger.debug(ast.unparse(user_code))
        #logger.debug('\n----------------------------\n\n')

        exec(compile(user_code, script_name, "exec"), locals_copy, locals_copy)

        raster_reference_payload = locals_copy.get("gpo_raster_reference_payload", None)

        return locals_copy["gpo_payload"], raster_reference_payload


async def script_task(
    script_name: str,
    input_updates: Dict[str, Any],
    hex_token_generator=secrets.token_hex,
):
    """
    async task that runs a user_script in a Greppo context (`gpo_send_data`) and generates payload for front-end
    consumption.
    """
    # logger.setLevel(logging.DEBUG)

    logging.info("Loading Greppo App at: " + script_name)

    with redirect_stdout(io.StringIO()) as loop_out:
        payload = run_script(
            script_name=script_name,
            input_updates=input_updates,
            hex_token_generator=hex_token_generator,
        )

    logger.debug("-------------")
    logger.debug("stdout from process")
    logger.debug("===")
    logger.debug(loop_out.getvalue())
    logger.debug("===")

    return payload
