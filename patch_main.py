with open("main.py", "r") as f:
    content = f.read()

import_statement = "from fastapi.staticfiles import StaticFiles\nfrom fastapi.responses import FileResponse\n"
if "StaticFiles" not in content:
    content = content.replace("from fastapi import FastAPI, Depends, Request", "from fastapi import FastAPI, Depends, Request\n" + import_statement)

route_code = """
app.mount("/src", StaticFiles(directory="frontend/src"), name="src")

@app.get("/")
def serve_index():
    return FileResponse("frontend/index.html")
"""

old_route = """@app.get("/")
def home():
    return {"message": "CodeReview AI is running!"}"""

if old_route in content:
    content = content.replace(old_route, route_code)

with open("main.py", "w") as f:
    f.write(content)
print("main.py patched successfully")
