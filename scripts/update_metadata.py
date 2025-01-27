import argparse
import hashlib
import json
import requests

def get_release_assets(repo, version, token):
    headers = {"Authorization": f"Bearer {token}"}
    url = f"https://api.github.com/repos/{repo}/releases/tags/{version}"
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()["assets"]

def calculate_sha256(url, token):
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(url, headers=headers, stream=True)
    sha256 = hashlib.sha256()
    
    for chunk in response.iter_content(chunk_size=8192):
        if chunk:
            sha256.update(chunk)
    
    return sha256.hexdigest()

def update_public_json(version, repo, token):
    with open("public.json", "r") as f:
        data = json.load(f)
    
    assets = get_release_assets(repo, version, token)
    
    for entry in data["versions"]:
        if entry["version"] == version:
            for asset in assets:
                platform = "windows" if "windows" in asset["name"].lower() else "linux"
                entry["download_url"][platform] = asset["browser_download_url"]
                entry["hash"][platform] = calculate_sha256(asset["url"], token)
            break
    
    with open("public.json", "w") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--version", required=True)
    parser.add_argument("--repo", required=True)
    args = parser.parse_args()
    
    token = open("/github_token.txt").read().strip()  # Token will be injected via GITHUB_TOKEN env
    update_public_json(args.version, args.repo, token)