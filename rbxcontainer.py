#!/usr/bin/env python3
import sys
from src.packages.utils import die
from src.cmd.add import add_cmd
from src.cmd.help import help_cmd
from src.cmd.init import init_cmd
from src.cmd.install import install_cmd
from src.cmd.list import list_cmd
from src.cmd.remove import remove_cmd

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