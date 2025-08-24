#!/usr/bin/env python3
import json, os, shutil, subprocess, sys, pathlib

ROOT = pathlib.Path(os.getcwd())
MANIFEST = ROOT / "rbxcontainer.json"
REGISTRY = ROOT / "rbxcontainer.registry.json"

SRC_DIR = ROOT / "src"
PKG_DIR = SRC_DIR / "packages"

ROJO = ROOT / "default.project.json"

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

def init_cmd():
    # manifest
    if not MANIFEST.exists():
        save_json(MANIFEST, {
            "dependencies": {},
            "packagesPath": "src/packages",
            "target": "ReplicatedStorage"
        })
        print("[rbxcontainer] created rbxcontainer.json")
    else:
        print("[rbxcontainer] rbxcontainer.json already exists")

    # ensure src folder exists
    SRC_DIR.mkdir(exist_ok=True)

    # ensure packages dir inside src
    PKG_DIR.mkdir(exist_ok=True)
    print("[rbxcontainer] ensured src/packages/")

    # if default.project.json exists → wire packages
    if ROJO.exists():
        project = load_json(ROJO, None)
        if project is None:
            return

        tree = project.setdefault("tree", {})
        repl = tree.setdefault("ReplicatedStorage", {"$className": "ReplicatedStorage"})

        # only add Packages if not already present
        if "Packages" not in repl:
            repl["Packages"] = {"$path": "src/packages"}
            save_json(ROJO, project)
            print("[rbxcontainer] wired Rojo: src/packages -> ReplicatedStorage/Packages")
    else:
        print("[rbxcontainer] no default.project.json found (skipping Rojo wiring)")



def add_cmd(name, url=None):
    manifest = load_json(MANIFEST, None)
    if manifest is None:
        die("No rbxcontainer.json. Run `rbxcontainer init` first.")
    registry = load_json(REGISTRY, {})
    if url is None:
        url = registry.get(name)
        if not url:
            die(f"No registry entry for '{name}'. Add it to rbxcontainer.registry.json or run `rbxcontainer add {name} <git-url>`.")
    manifest["dependencies"][name] = {"git": url}
    save_json(MANIFEST, manifest)
    print(f"[rbxcontainer] added {name} -> {url} to rbxcontainer.json")

def remove_cmd(name):
    manifest = load_json(MANIFEST, None)
    if manifest is None:
        die("No rbxcontainer.json. Run `rbxcontainer init` first.")
    if name in manifest.get("dependencies", {}):
        del manifest["dependencies"][name]
        save_json(MANIFEST, manifest)
        print(f"[rbxcontainer] removed {name} from rbxcontainer.json")
    else:
        print(f"[rbxcontainer] {name} not in manifest")
    # remove folder if exists
    pkg_path = PKG_DIR / name
    if pkg_path.exists():
        shutil.rmtree(pkg_path)
        print(f"[rbxcontainer] deleted {pkg_path}")

def install_cmd():
    ensure_git()
    manifest = load_json(MANIFEST, None)
    if manifest is None:
        die("No rbxcontainer.json. Run `rbxcontainer init` first.")
    deps = manifest.get("dependencies", {})
    if not deps:
        print("[rbxcontainer] no dependencies to install")
        return
    PKG_DIR.mkdir(exist_ok=True)
    for name, meta in deps.items():
        url = meta.get("git")
        if not url:
            print(f"[rbxcontainer] skip {name}: no 'git' url")
            continue
        dst = PKG_DIR / name
        if dst.exists():
            print(f"[rbxcontainer] updating {name} ...")
            # try fast-forward
            try:
                if (dst / ".git").exists():
                    sh(["git", "fetch", "--all"], cwd=dst)
                    sh(["git", "pull", "--ff-only"], cwd=dst)
                else:
                    print(f"[rbxcontainer] {name} is not a git repo; skipping update")
            except subprocess.CalledProcessError:
                print(f"[rbxcontainer] warning: could not fast-forward {name}")
        else:
            print(f"[rbxcontainer] cloning {name} from {url} ...")
            sh(["git", "clone", "--depth=1", url, str(dst)])
    print("[rbxcontainer] install complete")


def list_cmd():
    manifest = load_json(MANIFEST, {"dependencies":{}})
    deps = manifest.get("dependencies", {})
    if not deps:
        print("[rbxcontainer] (no dependencies)")
        return
    print("[rbxcontainer] dependencies:")
    for k,v in deps.items():
        print(f"  - {k}: {v.get('git','?')}")
    print("\n[rbxcontainer] installed folders:")
    if not PKG_DIR.exists():
        print("  (none)")
        return
    for p in sorted(PKG_DIR.iterdir()):
        if p.is_dir():
            print("  -", p.name)

def help_cmd():
    print("""rbxcontainer — tiny Rojo package helper

Usage:
  rbxcontainer init
  rbxcontainer add <name> [git-url]
  rbxcontainer remove <name>
  rbxcontainer install
  rbxcontainer list
  rbxcontainer help

Notes:
- Registry lives in rbxcontainer.registry.json (edit freely).
- Packages clone to ./Packages/<name>.
- Rojo mapping is auto-wired to ReplicatedStorage/Packages/rbxcontainer/<name>.
""")

def main():
    if len(sys.argv) < 2:
        help_cmd(); return
    cmd = sys.argv[1]
    if cmd == "init": init_cmd()
    elif cmd == "add":
        if len(sys.argv) < 3: die("usage: rbxcontainer add <name> [git-url]")
        add_cmd(sys.argv[2], sys.argv[3] if len(sys.argv) >= 4 else None)
    elif cmd == "install": install_cmd()
    elif cmd == "remove":
        if len(sys.argv) < 3: die("usage: rbxcontainer remove <name>")
        remove_cmd(sys.argv[2])
    elif cmd == "list": list_cmd()
    elif cmd in ("help","-h","--help"): help_cmd()
    else: die(f"unknown command '{cmd}'. try: rbxcontainer help")

if __name__ == "__main__":
    main()