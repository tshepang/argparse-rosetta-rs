#!/usr/bin/env python3

import pathlib
import json
import argparse


def main():
    repo_root = pathlib.Path(__name__).parent
    runs_root = repo_root / "runs"
    default_run_path = sorted(runs_root.glob("*.json"))[-1]

    parser = argparse.ArgumentParser()
    parser.add_argument("--run", metavar="PATH", type=pathlib.Path, default=default_run_path, help="Default: %(default)s")
    args = parser.parse_args()

    data = json.loads(args.run.read_text())
    cases = sorted(data["libs"].values(), key=lambda c: (c["crate"] if c["crate"] else "", c["name"]))

    print("Name | Overhead (release) | Build (debug) | Deps | Version")
    print("-----|--------------------|---------------|------|--------")
    for case in cases:
        row = [
            case["name"],
            fmt_size(case, cases[0]),
            fmt_time(case),
            str(case["deps"]),
            case["version"] if case["version"] else "-",
        ]
        print(" | ".join(row))
    print()
    print(f"*System: {data['os']} {data['os_ver']} ({data['arch']})*")


def fmt_time(case):
    value = case["build"]["results"][0]["median"]
    return "{:.0f}s".format(value)


def fmt_size(case, null_case):
    delta = (case["size"] - null_case["size"]) / 1024
    return "{:,.0f} KiB".format(delta)


if __name__ == "__main__":
    main()