import os

files = os.listdir()
posts = [f for f in files if f.endswith(".md")]

lines = [f"* [{post}]({post})\n" for post in posts]

with open("index.md", "w") as f:
    f.writelines(lines)
