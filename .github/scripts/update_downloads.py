import hashlib
import json
import os
from pathlib import Path

def calculate_sha256(file_path: Path) -> str:
    sha = hashlib.sha256()
    with file_path.open("rb") as f:
        while chunk := f.read(4096):
            sha.update(chunk)
    return sha.hexdigest()

def update_download_info(version: str, repo: str):
    public_file = Path("public.json")
    data = json.loads(public_file.read_text(encoding="utf-8"))
    
    # 查找目标版本
    target = next(v for v in data["versions"] if v["version"] == version)
    
    # 扫描构建产物
    downloads = []
    for build in Path("releases").iterdir():
        if build.is_file():
            os_name = "Windows" if "windows" in build.name.lower() else "Linux"
            downloads.append({
                "os": os_name,
                "download_url": f"https://github.com/{repo}/releases/download/v{version}/{build.name}",
                "hash": f"sha256:{calculate_sha256(build)}"
            })
    
    target["downloads"] = downloads
    
    public_file.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n",
                          encoding="utf-8")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--version", required=True)
    parser.add_argument("--repo", required=True)
    args = parser.parse_args()
    
    update_download_info(args.version, args.repo)