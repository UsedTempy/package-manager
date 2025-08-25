from src.packages.utils import save_json, load_json, die
from src.packages.hierarchy import MANIFEST, PKG_DIR
import shutil

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