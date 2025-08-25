from src.packages.utils import load_json
from src.packages.hierarchy import MANIFEST, PKG_DIR

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