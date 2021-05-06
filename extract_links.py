# import glob
import pathlib
from urllib.parse import quote

BASE_DIR = pathlib.Path(__file__).parent


def get_markdowned_links(
    use_raw=True, ignore_dirs=["/", "", "."], ignore_basename=["index", "readme"]
):
    extracted_links = {}
    for path in BASE_DIR.glob("**/*.md"):
        directory = path.parent
        directory_str = str(directory)
        basename = str(path.stem)
        # path_sutffix = str(path.suffix)
        if directory_str in ignore_dirs:
            continue
        if basename.lower() in ignore_basename:
            continue
        if directory_str not in extracted_links:
            extracted_links[directory_str] = {
                "title": f"[{directory_str.title()}](/{directory_str})",
                "links": [],
                "abs_links": [],
            }
        basename_url_quoted = quote(basename)
        path_quote = quote(str(path))
        base_href = f"/{path.parent}/{basename_url_quoted}"
        path_href = f"/{path_quote}"
        link_wo_extension = f"[{path.stem}]({base_href})"
        link_w_extension = f"[{path.name}]({path_href})"
        if use_raw:
            link_wo_extension = f"{link_wo_extension} ([Raw]({path_href}))"
        extracted_links[directory_str]["links"].append(link_wo_extension)
        extracted_links[directory_str]["links"].sort(key=lambda x: x[1])
        extracted_links[directory_str]["abs_links"].append(link_w_extension)
        extracted_links[directory_str]["abs_links"].sort(key=lambda x: x[1])
    return extracted_links


def extracted_links_to_md(
    links_key="links", extracted_links={}, ignore_dirs=["shell-scripts", "."]
):
    for _dir, value in extracted_links.items():
        if _dir in ignore_dirs:
            continue
        if not isinstance(value, dict):
            continue
        _dir_desc_md = ""
        for k, v in value.items():
            if isinstance(v, str):
                if f"{v}".strip() == ".":
                    continue
                if k == "title":
                    _dir_desc_md += f"### {v}\n"
            if k == links_key:
                for link in v:
                    _dir_desc_md += f"- {link}\n"
                    _dir_desc_md += "\n"

    return _dir_desc_md


def make_dir_index(markdown_str, dirname):
    dirname_path = BASE_DIR / dirname
    folder_path = BASE_DIR / folder
    dir_index_md = dirname_path / "index.md"
    dir_readme_str = ""
    dir_readme_path = folder_path / "README.md"
    if dir_readme_path.exists():
        dir_readme_str = dir_readme_path.read_text()
    dir_index_md.write_text(dir_readme_str + "\n\n" + markdown_str)


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
readme_title_str = ""
readme_title_md = BASE_DIR / "header_title.md"
if readme_title_md.exists():
    readme_title_str = readme_title_md.read_text()
readme_md.write_text(f"{readme_title_str}\n{index_str}")
