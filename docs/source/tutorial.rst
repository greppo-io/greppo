Mental model
============

Greppo's interface is simple and is designed with the intention of getting out of the users way. We want to make it easy
to build a geo-spatial app quickly.

Greppo focuses on two ideas,

#. Use native python code and other standard libraries for analysis.
#. Use simple macros to prepare a user code for execution within Greppo.

The first idea ensures as much freedom as possible in terms of compatability with libraries commonly used for data
science and geo-spatial analysis. The second is to keep Greppo in the background and only surface a small interface
for the user to work with. Both ideas keep the mental bandwidth of using a new library low and focus on simple and
intuitive UX.

With this in mind, the following code snippets breaks down a common user-script to illustrate the two ideas. The entire
code as a single file is here <TODO> and to run the code before looking at the explanation, simply run `` <TODO>.

#. Imports

.. code-block :: python

    import geopandas as gpd
    import numpy as np
    import pandas as pd
    from greppo_app import gpo

#. For each Greppo app, we have a base layer that is a required setup from the user.

    .. code-block :: python

        gpo.base_layer(
            name="CartoDB Light",
            visible=True,
            url="https://cartodb-basemaps-a.global.ssl.fastly.net/light_all/{z}/{x}/{y}@2x.png",
            subdomains=None,
            attribution='&copy; <a target="_blank" href="http://osm.org/copyright">OpenStreetMap</a> contributors',
        )

#. :code:`gpo.number` is Greppo primitive for user interaction for a number. Each defines the inputs they want in app, in
    this case a number, that they will use to manipulate the GIS data. Here, for :code:`gpo.number` there is a
    :code:`value` arg that defines the initial default value and a :code:`name` arg that is a _unique_ identifier for
    that input. Greppo uses the :code:`name` to provide a reactive feedback when rendering the app.

    .. code-block :: python

        number_1 = gpo.number(value=10, name="Number input 1")

#. Regular GDF code a Data Scientist is familiar with.

    .. code-block :: python

        data_gdf_1 = gpd.read_file("tests/data/communes.geojson")

#. Here the Greppo user closes the feedback loop and uses the :code:`gpo.number` input to perform analysis. This example
   is trivial but gives you a clear idea of how things work. When Greppo renders this code, the User can interact
   with the front-end to dynamically pass values and recompute the data.

    .. code-block :: python

        data_gdf_1["Value"] = pd.Series(
            np.ones(len(data_gdf_1["code"])) * number_1, index=data_gdf_1.index
        )

#. As with the :code:`gpo.base_layer`, a Greppo app must define a required :code:`gpo.overlay_layer`.

    .. code-block :: python

        gpo.overlay_layer(
            data_gdf_1,
            title="Communes",
            description="Communes in Normandy, France",
            style={"fillColor": "#F87979"},
            visible=True,
        )

#. Generic Python to perform some action, in this case construct a list of random numbers.

    .. code-block :: python

        y = []
        for i in range(10, 0, -1):
            y.append(np.random.randint(0, 100))

#. To complete this trivial example, this :code:`gpo.line_chart` gives you an idea of the visualization tools a Greppo
   app has access to. Here, the random number list generated above is plotted as a line chart.

    .. code-block :: python

        gpo.line_chart(
            name="some-name",
            title="some_title",
            description="some_chart",
            x=[i for i in range(10)],
            y=y,
        )
