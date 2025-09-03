import argparse
from .fetch_packages import fetch_package_names, save_packages
from .installer import parallel_install
from .db import init_db


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=["fetch", "goinstall", "rinstall"])
    parser.add_argument("--packages", default="packages.txt")
    args = parser.parse_args()

    init_db()

    if args.command == "fetch":
        pkgs = fetch_package_names()
        save_packages(pkgs, args.packages)
        print(f"Saved {len(pkgs)} packages to {args.packages}")
    else:
        with open(args.packages) as f:
            pkgs = [line.strip() for line in f if line.strip()]
        parallel_install(pkgs, args.command)


if __name__ == "__main__":
    main()
