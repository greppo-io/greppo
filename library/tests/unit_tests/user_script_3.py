from greppo import app


multiselect1 = app.multiselect(
    name="Second selector", options=[1, "True", "France"], default=["a"]
)
