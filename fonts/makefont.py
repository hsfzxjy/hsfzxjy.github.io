#!/usr/bin/env python3
import os
import string
import argparse
import tempfile
import subprocess
from glob import glob
from pathlib import Path

ROOT_DIR = Path(__file__).absolute().parent
WORK_DIR = ROOT_DIR


def unicode_to_hex(char):
    return "U+" + hex(ord(char))[2:].upper().zfill(4)


def execute(args):
    p = subprocess.Popen(args)
    p.wait()


def get_text(args):
    assert args.text or args.alphabet
    if args.text:
        return args.text

    return string.ascii_letters + string.punctuation + string.digits


def get_font_list(args):
    for font_path in args.font:
        font_path = Path(font_path)
        if font_path.name.startswith("slim."):
            continue

        yield font_path


def output_path(font_path: Path):
    return font_path.parent / ("slim." + font_path.name)


def main(args):
    os.chdir(WORK_DIR)

    with tempfile.NamedTemporaryFile("w") as f:
        f.writelines(map(unicode_to_hex, get_text(args)))
        f.flush()

        for font_path in get_font_list(args):
            print(f"Subsetting {font_path}...")
            execute(
                [
                    "pyftsubset",
                    f"--unicodes-file={f.name}",
                    str(font_path),
                    f"--output-file={output_path(font_path)}",
                ]
            )


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--text", default="")
    parser.add_argument("--font", default=["sawarabi-mincho-medium.ttf"], nargs="+")
    parser.add_argument("--alphabet", action="store_true")
    args = parser.parse_args()

    main(args)
