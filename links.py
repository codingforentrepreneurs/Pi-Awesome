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
    path_quote = quote(str(path))
    page_link = f"[{path.stem}]({path.parent}/{article_quote})"
    raw_link = ""
    if "md" in path.suffix:
        raw_link = f"{path_quote}"
    link = page_link
    if raw_link != "":
        link = f"{page_link} ([Raw]({raw_link}))"
    all_links[parent_str]["links"].append(link)
    all_links[parent_str]["links"].sort(key=lambda x: x[1])

link_markdown = ""
for folder, values in all_links.items():
    if str(folder) == "." or str(folder) == "shell-scripts":
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

root_header_md = BASE_DIR / "header.md"
root_readme_str = ""
if root_header_md.exists():
    root_readme_str = root_header_md.read_text()
    root_readme_str += "\n\n"

shell_scipts_links_str = ""
shell_scipts_header_md = BASE_DIR / "shell-scripts" / "header.md"
if shell_scipts_header_md.exists():
    shell_scipts_links_str += shell_scipts_header_md.read_text()
    shell_scipts_links_str += "\n\n"

script_list = list(BASE_DIR.glob("**/*.sh"))
script_list.sort()
for item in script_list:
    path = pathlib.Path(item)
    link = f"### `{path.stem}{path.suffix}`\n"
    link += f"[Download]({str(path)}) | "
    link += f"[Raw](https://github.com/codingforentrepreneurs/Pi-Awesome/blob/main/{str(path)})\n"  # noqa
    fname = path.name
    cmd_1 = f"curl https://www.piawesome.com/shell-scripts/{fname} -O {fname}"
    cmd_2 = f"chmod +x {fname}"
    cmd_3 = f"sh {fname}"
    run_command = f"```\n{cmd_1}\n{cmd_2}\n{cmd_3}\n```"
    cmd_ssl = f"curl -sSL https://www.piawesome.com/shell-scripts/{fname}"
    root_command = f"```\nsudo {cmd_ssl} | sh \n```"
    description = path.parent / f"{path.stem}.md"
    if description.exists():
        link += "\n"
        link += description.read_text() + "\n\n"
    link += "\n\n" + root_command + "\nOr\n" + run_command + "\n\n"
    shell_scipts_links_str += link


index_str = root_readme_str + "\n"
index_str += link_markdown + "\n\n"
index_str += shell_scipts_links_str
index_md = BASE_DIR / "index.md"
index_md.write_text(index_str)

readme_md = BASE_DIR / "README.md"
readme_md.write_text(index_str)
