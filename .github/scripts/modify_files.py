import json
import re
from pathlib import Path

def update_version(version: str):
    static_file = Path("utils/static.py")
    content = static_file.read_text(encoding="utf-8")
    
    # 使用正则表达式精确匹配版本号
    updated = re.sub(
        r'(CURRENT_VERSION\s*=\s*["\'])([\d.]+)(["\'])',
        fr'\g<1>{version}\3',
        content
    )
    static_file.write_text(updated, encoding="utf-8")

def update_public_json(args):
    public_file = Path("public.json")
    
    try:
        data = json.loads(public_file.read_text(encoding="utf-8"))
    except FileNotFoundError:
        data = {"versions": [], "broadcast": ""}

    # 更新广播消息（当有输入时覆盖）
    if args.broadcast is not None:
        data["broadcast"] = args.broadcast

    # 添加/更新版本信息
    if args.version:
        new_version = {
            "version": args.version,
            "changelog": args.changelog,
            "level": args.level,
            "significance": args.significance,
            "downloads": []  # 稍后由update_downloads.py填充
        }
        
        # 查找现有版本
        existing = next(
            (v for v in data["versions"] if v["version"] == args.version),
            None
        )
        
        if existing:
            existing.update(new_version)
        else:
            data["versions"].insert(0, new_version)  # 新版本置顶

    public_file.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", 
                          encoding="utf-8")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="更新项目文件")
    parser.add_argument("--version", help="新版本号")
    parser.add_argument("--changelog", help="版本更新日志")
    parser.add_argument("--level", help="严重等级")
    parser.add_argument("--significance", help="变更等级")
    parser.add_argument("--broadcast", help="广播消息内容")
    
    args = parser.parse_args()
    
    # 当有广播参数时（包括空字符串）
    if args.broadcast is not None:
        update_public_json(args)
    
    # 当有版本参数时
    if args.version:
        update_version(args.version)
        update_public_json(args)