import ast
import io
import logging
import secrets
from _ast import Assign
from _ast import Attribute
from _ast import Call
from _ast import keyword
from _ast import Load
from _ast import Name
from _ast import Store
from contextlib import redirect_stdout
from typing import Any

from greppo import GreppoAppProxy
from .input_types import GreppoInputsNames


logger = logging.getLogger('user_script_utils')


class Transformer(ast.NodeTransformer):
    def __init__(self, input_updates, hex_token_generator):
        super().__init__()

        self.input_updates = input_updates

        self.hex_token_generator = hex_token_generator

    def visit_Call(self, node):
        if not hasattr(node.func, "attr"):
            return node

        if node.func.attr not in GreppoInputsNames:
            return node

        # ==== Find all names for gpo_inputs and set hex id
        for node_kwargs in node.keywords:
            if node_kwargs.arg == "name":
                input_name = node_kwargs.value.value
                input_name = self.hex_token_generator(nbytes=4) + "_" + input_name
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


def run_script(script_name, input_updates, hex_token_generator):
    with open(script_name) as f:
        lines = f.read()
        user_code = ast.parse(lines, script_name)

        transformer = Transformer(
            input_updates=input_updates, hex_token_generator=hex_token_generator
        )
        transformer.visit(user_code)
        ast.fix_missing_locations(
            user_code
        )  # TODO double check why this happens with on node position copy

        user_code = append_send_data_method(user_code)

        # Transform gpo for locals() injection
        hash_prefix = hex_token_generator(nbytes=4)
        gpo_transformer = RenameGreppoAppTransformer(hash_prefix=hash_prefix)
        gpo_transformer.visit(user_code)

        ast.fix_missing_locations(user_code)

        # TODO maybe have a fresh locals obj?
        locals()[hash_prefix + "_app"] = GreppoAppProxy()

        exec(compile(user_code, script_name, "exec"), globals(), locals())

        return locals()["gpo_payload"]


async def script_task(
    script_name: str,
    input_updates: dict[str, Any],
    hex_token_generator=secrets.token_hex,
):
    """
    async task that runs a user_script in a Greppo context (`gpo_send_data`) and generates payload for front-end
    consumption.
    """
    logging.info("Loading Greppo App at: " + script_name)

    with redirect_stdout(io.StringIO()) as loop_out:
        payload = run_script(
            script_name=script_name,
            input_updates=input_updates,
            hex_token_generator=hex_token_generator,
        )

    logger.setLevel(logging.DEBUG)

    logger.info("-------------")
    logger.info("stdout from process")
    logger.info("===")
    logger.info(loop_out.getvalue())
    logger.info("===")

    return payload
