import pathlib, os

ROOT = pathlib.Path(os.getcwd())
MANIFEST = ROOT / "rbxcontainer.json"
REGISTRY = ROOT / "rbxcontainer.registry.json"

SRC_DIR = ROOT / "src"
PKG_DIR = SRC_DIR / "packages"

ROJO = ROOT / "default.project.json"