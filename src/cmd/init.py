from src.packages.utils import save_json, load_json
from src.packages.hierarchy import MANIFEST, SRC_DIR, PKG_DIR, ROJO

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