from __future__ import annotations

import re
import argparse

from subprocess import check_output
from typing import Sequence

def prepare_commit_msg(commit_msg_filepath):
    branch = (
        check_output(["git", "symbolic-ref", "--short",
    "HEAD"]).decode("utf-8").strip()
    )
    regex = r"^[A-Z]{1,9}-[0-9]{1,9}"
    found_obj = re.match(regex, branch)
    if found_obj:
        prefix = found_obj.group(0)
        with open(commit_msg_filepath, "r+") as f:
            commit_msg = f.read()
            if commit_msg.find(prefix) == -1:
                f.seek(0, 0)
                f.write(f"[{prefix}] {commit_msg}")
    
    return 0

def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('filename', type=argparse.FileType('r'), help='Filename pre-commit believes are changed.')
    args = parser.parse_args(argv)

    return prepare_commit_msg(args.filename)

if __name__ == '__main__':
    raise SystemExit(main())
