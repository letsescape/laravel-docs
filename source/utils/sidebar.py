import json
import os
import re


def parse_documentation_md(content, version):
    """Parse documentation.md content and create sidebar structure.

    Args:
        content: Raw content of documentation.md
        version: Version string (e.g., "12.x")

    Returns:
        dict: Sidebar structure compatible with Docusaurus versioned sidebars
    """
    lines = content.split('\n')
    sidebar = {"tutorialSidebar": []}
    current_category = None

    for line in lines:
        # Match main category: - ## Category Name
        category_match = re.match(r'^- ## (.+)$', line)
        if category_match:
            current_category = {
                "type": "category",
                "label": category_match[1],
                "collapsed": True,
                "items": []
            }
            sidebar["tutorialSidebar"].append(current_category)
            continue

        # Match items within a category: - [Label](/docs/{{version}}/path)
        item_match = re.match(r'^\s+- \[[^\]]+\]\(/docs/\{\{version\}\}/([^)]+)\)$', line)
        if item_match and current_category:
            item_path = item_match[1]
            # Remove anchor links (e.g., 'starter-kits#laravel-breeze' -> 'starter-kits')
            if '#' in item_path:
                item_path = item_path.split('#')[0]
            current_category["items"].append(item_path)
            continue

        # Match API Documentation link
        api_match = re.match(r'^- \[API Documentation\]\((.+)\)$', line)
        if api_match:
            api_url = api_match[1]
            if '{{version}}' in api_url:
                api_url = api_url.replace('{{version}}', version)
            sidebar["tutorialSidebar"].append({
                "type": "link",
                "label": "API Documentation",
                "href": api_url
            })

    # Set second category to be expanded by default (first is Prologue, kept collapsed)
    if len(sidebar["tutorialSidebar"]) > 1:
        sidebar["tutorialSidebar"][1]["collapsed"] = False

    return sidebar


def generate_sidebar(version, repo_root):
    """Generate sidebar JSON file for a specific version.

    Args:
        version: Version string (e.g., "12.x")
        repo_root: Absolute path to the repository root

    Returns:
        bool: True if sidebar was generated successfully, False otherwise
    """
    doc_path = os.path.join(
        repo_root, "versioned_docs", f"version-{version}", "origin", "documentation.md"
    )
    output_path = os.path.join(
        repo_root, "versioned_sidebars", f"version-{version}-sidebars.json"
    )

    if not os.path.exists(doc_path):
        print(f"  documentation.md 파일을 찾을 수 없음: {version}")
        return False

    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    with open(doc_path, 'r', encoding='utf-8') as f:
        content = f.read()

    sidebar = parse_documentation_md(content, version)

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(sidebar, f, indent=2)
        f.write('\n')

    print(f"  사이드바 생성 완료: {version}")
    return True


def generate_all_sidebars(branches, repo_root):
    """Generate sidebar JSON files for all versioned branches.

    Args:
        branches: List of branch names (e.g., ["master", "12.x", "11.x"])
        repo_root: Absolute path to the repository root
    """
    # Filter out 'master' since it doesn't have a Docusaurus version
    versions = [b for b in branches if b != "master"]

    for version in versions:
        generate_sidebar(version, repo_root)
