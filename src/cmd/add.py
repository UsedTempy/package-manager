from src.packages.utils import save_json, load_json, die
from src.packages.hierarchy import MANIFEST, REGISTRY

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