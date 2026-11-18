"""Entrypoint for the news-image-20261117 entry (Python 3.13, stdlib only).

The image is drawn at build time by draw.py (Pillow, local only) and shipped
in this repository as entry.png; this program simply copies it to the output
directory, exactly like the kit's starter. Deterministic: the same bytes are
written on every run.

Outside the grader's container, MAKEFUN_OUTPUT_DIR stands in for /output:
    mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
"""
import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    src = os.path.join(HERE, "entry.png")
    dst = os.path.join(out_dir, "entry.png")
    shutil.copyfile(src, dst)


if __name__ == "__main__":
    main()
