import json

with open("app_data.json", "r") as f:
    data = json.load(f)

js_content = f"window.APP_DATA = {json.dumps(data)};"

with open("app_data.js", "w") as f:
    f.write(js_content)

print("Exported app_data.js successfully!")
