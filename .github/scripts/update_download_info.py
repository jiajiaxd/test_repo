import os
import json
import hashlib

def calculate_hash(file_path):
    hasher = hashlib.sha256()
    with open(file_path, "rb") as f:
        while chunk := f.read(8192):
            hasher.update(chunk)
    return hasher.hexdigest()

def update_download_info():
    with open("public.json", "r") as f:
        data = json.load(f)
    
    version = os.environ.get("VERSION")
    repo = os.environ["GITHUB_REPOSITORY"]
    
    for v in data["versions"]:
        if v["version"] == version:
            downloads = []
            for file in os.listdir("releases"):
                if file.endswith((".exe", "")):  # 根据实际文件扩展名调整
                    file_path = os.path.join("releases", file)
                    downloads.append({
                        "os": "windows" if "windows" in file else "ubuntu",
                        "download_url": f"https://github.com/{repo}/releases/download/{version}/{file}",
                        "hash": calculate_hash(file_path)
                    })
            v["downloads"] = downloads
            break
    
    with open("public.json", "w") as f:
        json.dump(data, f, indent=2)

if __name__ == "__main__":
    update_download_info()