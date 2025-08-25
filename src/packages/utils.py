import json, subprocess, sys

def die(msg, code=1):
    print(f"[rbxcontainer] {msg}")
    sys.exit(code)

def load_json(path, default):
    if not path.exists():
        return default
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def save_json(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write("\n")

def ensure_git():
    try:
        subprocess.run(["git", "--version"], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except Exception:
        die("Git not found. Install Git and try again.")

def sh(cmd, cwd=None):
    subprocess.run(cmd, check=True, cwd=cwd)