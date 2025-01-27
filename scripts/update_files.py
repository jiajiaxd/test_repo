import argparse
import json
import re

def update_static_version(version):
    with open("utils/static.py", "r") as f:
        content = f.read()
    
    content = re.sub(
        r'CURRENT_VERSION\s*=\s*["\']\d+\.\d+\.\d+["\']',
        f'CURRENT_VERSION = "{version}"',
        content
    )
    
    with open("utils/static.py", "w") as f:
        f.write(content)

def update_public_json(args):
    try:
        with open("public.json", "r") as f:
            data = json.load(f)
    except FileNotFoundError:
        data = {"versions": []}

    new_version = {
        "version": args.version,
        "changelog": args.changelog,
        "level": args.level,
        "significance": args.significance,
        "download_url": {},
        "hash": {}
    }

    data["versions"].insert(0, new_version)
    
    with open("public.json", "w") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--version", required=True)
    parser.add_argument("--changelog", required=True)
    parser.add_argument("--level", required=True)
    parser.add_argument("--significance", required=True)
    args = parser.parse_args()
    
    update_static_version(args.version)
    update_public_json(args)