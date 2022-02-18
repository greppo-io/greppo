from greppo import app

app.map(max_zoom= 18, center=[25, 25], zoom=10)

app.base_layer(provider='CartoDB Positron', visible=True)

text_1 = app.text(name='Text input', value='Some text...')

app.display(name='text-1-display', value=f'Value of text input: {text_1}')