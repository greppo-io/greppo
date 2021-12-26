from greppo import app

app.display(value='App title', name="title")
app.display(value='App description', name="description")
text = """# Title
## Description

### List
- A
- B
- C
"""
app.display(value=text, name="text1")