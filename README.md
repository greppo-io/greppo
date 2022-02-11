# Hey there, this is <a href="https://greppo.io/" style="color: #F5325B;"><img src="./assets/logo.png" height="28"> Greppo</a>...

[![Discord](https://badgen.net/badge/icon/discord?icon=discord&label)](https://discord.gg/RNJBjgh8gz) ![Twitter URL](https://img.shields.io/twitter/url?style=social&url=https%3A%2F%2Ftwitter.com%2Fgreppo_io)

**A Python framework for building geospatial web-applications.**

Greppo is an open-source Python framework that makes it easy to build applications. It provides a toolkit for to quickly integrate data, algorithms, visualizations and UI for interactivity.

<img src="./assets/docs.svg" style=""> **Documentation**: [docs.greppo.io](https://docs.greppo.io)

<img src="./assets/globe.svg" style=""> **Website**: https://greppo.io

<img src="./assets/chat.svg" style=""> **Discord Community**: https://discord.gg/RNJBjgh8gz

If you run into any problems, ping us on Discord, Twitter or open an issue on GitHub.

## Installation

```shell
$ pip install greppo
```

We suggest you use a virtual environment to manage your packages for this project. For more infromation and troubleshooting visit the [Installation Guide](https://docs.greppo.io).

**Windows users**: Installation of Fiona (one of Greppo's dependencies) on Windows machines usually doesn't work by default. A manual installation with e.g. [wheel files by Christoph Gohlke](https://www.lfd.uci.edu/~gohlke/pythonlibs/) the  would be a work around.

## A simple example

```python
# inside app.py

from greppo import app
import geopandas as gpd

data_gdf = gpd.read_file("geospatial_data.geojson")

buildings_gdf = gpd.read_file("./data/buildings.geojson")

app.overlay_layer(
    buildings_gdf,
    name="Buildings",
    description="Buildings in a neighbourhood in Amsterdam",
    style={"fillColor": "#F87979"},
    visible=True,
)

app.base_layer(
    name="Open Street Map",
    visible=True,
    url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",
    subdomains=None,
    attribution='&copy; <a target="_blank" href="http://osm.org/copyright">OpenStreetMap</a> contributors',
)
```

Then run the aplication using the `greppo` cli command:

```shell
greppo serve app.py
```

To view the app that is being served, enter this address of the localhost `localhost:8080/` in your web browser. (Note: the port of `8080` might be different depending on other programs you're running. Check the port indicated in the command line interface.)

<img src="./assets/app.png" style="border-radius: 0.5rem;">

## Support & Community

Do you have questions? Ideas? Want to share your project? Join us on discord [Invite Link](https://discord.gg/RNJBjgh8gz).

## License

Greppo is licensed under Apache V2.
