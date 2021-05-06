# import glob
import pathlib
from urllib.parse import quote

BASE_DIR = pathlib.Path(__file__).parent
all_links = {}

for path in BASE_DIR.glob("**/*.md"):
    parent = path.parent
    parent_str = str(parent)
    path_stem = str(path.stem)
    if parent_str == "/" or parent_str == "" or parent_str == ".":
        continue
    if parent_str not in all_links:
        all_links[parent_str] = {
            "title": f"[{parent_str.title()}]({parent_str})",
            "links": [],
        }
    if path_stem.lower() == "index":
        continue
    if path_stem.lower() == "readme":
        continue
    article_quote = quote(path.stem)
    link = f"[{path.stem}]({path.parent}/{article_quote})"
    all_links[parent_str]["links"].append(link)
    all_links[parent_str]["links"].sort(key=lambda x: x[1])
link_markdown = ""
for folder, values in all_links.items():
    if str(folder) == ".":
        continue
    folder_index_md = ""
    for k, v in values.items():
        if k == "title":
            if v.strip() == ".":
                continue
            folder_index_md += f"### {v}\n"
        if k == "links":
            for link in v:
                folder_index_md += f"- {link}\n"
                folder_index_md += "\n"
    folder_path = BASE_DIR / folder
    folder_idx = folder_path / "index.md"
    folder_readme_str = ""
    folder_readme_path = folder_path / "README.md"
    if folder_readme_path.exists():
        folder_readme_str = folder_readme_path.read_text()
    folder_idx.write_text(folder_readme_str + "\n\n" + folder_index_md)
    folder_index_md += "\n"
    link_markdown += folder_index_md

root_readme_md = BASE_DIR / "README.md"
root_readme_str = ""
if root_readme_md.exists():
    root_readme_str = root_readme_md.read_text()

index_str = root_readme_str + "\n" + link_markdown
index_md = BASE_DIR / "index.md"
index_md.write_text(index_str)
