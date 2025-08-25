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