# Quickstart 
It's easy to get started with Greppo.

### Install Greppo
First install the Greppo python package using your python installation,
```shell
pip install greppo
```

### Setup the project
Create a new dir for your Greppo project, and create a new script,
```shell
mkdir my-greppo-app
cd my-greppo-app
touch app.py
```

&nbsp;

Create a new file `app.py` that will setup the user script,
```shell
touch app.py
```

&nbsp;

Populate script with a simple app to get started with,
```python
from greppo import app
import numpy as np

x = app.number(name="x", value=3)

print('Numbers list: ', np.ones(10) * x)
```

&nbsp;

This script creates a single input `x` that the user can interact with and the script generates a list of the current
number value with a list size of 10,

### Run app
Run the app and you're on your way building a geo-spatial app in seconds!
```shell
greppo serve app.py
```