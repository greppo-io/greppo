from greppo import app

app.base_layer(provider='CartoDB Positron', visible=True)

text_1 = app.text(name='Text input', value='Some text...')

app.display(name='text-1-display', value=f'Value of text input: {text_1}')