from src.packages.utils import load_json, die, sh, ensure_git
from src.packages.hierarchy import MANIFEST, PKG_DIR
import subprocess

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