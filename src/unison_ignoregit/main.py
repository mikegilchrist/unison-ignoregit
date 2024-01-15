import os
import sys

from .parser import GitLsFilesToUnisonIgnore
from .util import (
    build_cmd,
    collect_paths_from_cmd,
    collect_ignoregits_from_path,
    get_local_root_from_cmd,
    logger,
    run_cmd,
    should_parse_cmd,
)


def main(cmd=None):
    if cmd is None:
        cmd = sys.argv

    cmd_args = cmd[1:]

    if not should_parse_cmd(cmd_args):
        run_cmd(build_cmd(cmd_args, []))
    else:
        local_root = get_local_root_from_cmd(cmd_args)
        unison_ignores = []

        for abs_path, path in collect_paths_from_cmd(cmd_args):
            for ignoregit_dir, ignoregit_path in collect_ignoregits_from_path(abs_path):
                ignoregit_anchor = os.path.relpath(ignoregit_dir, local_root)
                if ignoregit_anchor == ".":
                    ignoregit_anchor = ""

                parser = GitLsFilesToUnisonIgnore(ignoregit_anchor)
                with open(ignoregit_path, "r") as fh:
                    unison_ignores.extend(parser.parse_ignoregit(fh))

        logger.info(
            f"Adding {len(unison_ignores)} ignore patterns based on `git ls-files` results"
        )
        cmd_new = build_cmd(cmd_args, unison_ignores)
        run_cmd(cmd_new)
