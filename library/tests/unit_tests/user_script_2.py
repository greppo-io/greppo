from greppo import app

x = app.number(name="x", value=3)
number_1 = app.number(value=1, name="Number input 1")

import numpy as np

print("number 1 from the script:", number_1)

print(np.ones(10) * number_1)
