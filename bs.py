#!/usr/bin/env python3
"""BASTIAN entry point.

Run with no arguments to launch the interactive console:
    python bs.py
"""

import argparse
import os
import sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from bastian import __version__  # noqa: E402


def _configure_stdio():
    """Use UTF-8 for console I/O so the block UI renders correctly."""
    if os.name == "nt":
        try:
            import ctypes

            kernel32 = ctypes.windll.kernel32
            kernel32.SetConsoleOutputCP(65001)
            kernel32.SetConsoleCP(65001)
        except Exception:
            pass
    for stream in (sys.stdin, sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8", errors="replace")
        except (AttributeError, ValueError):
            pass


def _parser():
    parser = argparse.ArgumentParser(
        prog="bs.py",
        description="BASTIAN - interactive multi-target security research toolkit.",
        epilog="Run without arguments to open the interactive console.",
    )
    parser.add_argument(
        "-v",
        "--version",
        action="version",
        version="BASTIAN " + __version__,
    )
    return parser


def main(argv=None):
    _parser().parse_args(argv)
    _configure_stdio()

    from bastian import menu

    try:
        menu.main()
    except KeyboardInterrupt:
        print()
        return 130
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
