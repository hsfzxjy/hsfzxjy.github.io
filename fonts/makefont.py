#!/usr/bin/env python3
import os
import argparse
import tempfile
import subprocess
from glob import glob
from pathlib import Path

ROOT_DIR = Path(__file__).absolute().parent
WORK_DIR = ROOT_DIR


def unicode_to_hex(char):
    return 'U+' + hex(ord(char))[2:].upper().zfill(4)


def execute(args):
    p = subprocess.Popen(args)
    p.wait()


def main(args):
    os.chdir(WORK_DIR)

    with tempfile.NamedTemporaryFile('w') as f:
        f.writelines(map(unicode_to_hex, args.TEXT))
        f.flush()

        print(f'Subsetting...')
        execute(
            [
                'pyftsubset',
                f'--unicodes-file={f.name}',
                args.font,
                f'--output-file=slim.{args.font}',
            ]
        )


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('TEXT')
    parser.add_argument('--font', default='sawarabi-mincho-medium.ttf')
    args = parser.parse_args()

    main(args)