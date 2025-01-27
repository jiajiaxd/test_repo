import argparse
import json
import re

def update_version(version):
    with open("utils/static.py", "r") as f:
        content = f.read()
    
    # 使用正则表达式更新版本号
    new_content = re.sub(
        r'CURRENT_VERSION = ".*?"',
        f'CURRENT_VERSION = "{version}"',
        content
    )
    
    with open("utils/static.py", "w") as f:
        f.write(new_content)

def update_public_json(args):
    with open("public.json", "r") as f:
        data = json.load(f)
    
    # 更新公告信息
    if args.broadcast:
        data["broadcast"] = args.broadcast
    
    # 添加版本信息（下载信息稍后填充）
    if args.version:
        new_version = {
            "version": args.version,
            "changelog": args.changelog,
            "level": args.level,
            "significance": args.significance,
            "downloads": []
        }
        
        # 查找并替换已有版本或添加新版本
        found = False
        for i, v in enumerate(data["versions"]):
            if v["version"] == args.version:
                data["versions"][i] = new_version
                found = True
                break
        if not found:
            data["versions"].append(new_version)
    
    with open("public.json", "w") as f:
        json.dump(data, f, indent=2)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--version")
    parser.add_argument("--changelog")
    parser.add_argument("--level")
    parser.add_argument("--significance")
    parser.add_argument("--broadcast")
    args = parser.parse_args()

    if args.version:
        update_version(args.version)
        update_public_json(args)
    elif args.broadcast:
        update_public_json(args)