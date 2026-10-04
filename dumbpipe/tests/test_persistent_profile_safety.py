#!/usr/bin/env python3
"""Exercise the documented profile snippet against a planted temp-file symlink."""

from __future__ import annotations

import os
import re
import stat
import subprocess
import tempfile
from pathlib import Path

DOC = Path(__file__).resolve().parents[1] / "references/persistent-profiles-and-tickets.md"


def main() -> None:
    text = DOC.read_text(encoding="utf-8")
    section = text.split("## Create a new share profile safely\n", 1)[1]
    snippet = re.search(r"```bash\n(.*?)\n```", section, re.DOTALL)
    assert snippet is not None, "profile procedure code block missing"

    with tempfile.TemporaryDirectory(prefix="dumbpipe-profile-regression-") as temporary:
        root = Path(temporary)
        config = root / "config"
        home = root / "home"
        home.mkdir()
        profile = config / "dumbpipe/shares/example"
        profile.mkdir(parents=True)
        planted_target = root / "outside-profile-target"
        planted_target.write_text("sentinel\n", encoding="utf-8")
        planted_link = profile / ".identity.env.tmp"
        planted_link.symlink_to(planted_target)

        key = "a" * 64
        mock = root / "dumbpipe-mock"
        mock.write_text(
            "#!/bin/sh\n"
            "[ \"$1\" = generate-ticket ] || exit 91\n"
            "printf '%s\\n' 'fixture-ticket'\n"
            f"printf 'using secret key %s\\n' '{key}' >&2\n",
            encoding="utf-8",
        )
        mock.chmod(0o700)

        env = os.environ.copy()
        env.pop("IROH_SECRET", None)
        env.update(HOME=str(home), XDG_CONFIG_HOME=str(config), DUMBPIPE_BIN=str(mock))
        result = subprocess.run(
            ["bash", "-c", snippet.group(1)],
            cwd=root,
            env=env,
            capture_output=True,
            text=True,
            check=False,
        )
        assert result.returncode == 0, "documented profile procedure failed with mocked dumbpipe"
        assert planted_target.read_text(encoding="utf-8") == "sentinel\n", "planted symlink target was modified"
        assert planted_link.is_symlink(), "planted symlink was unexpectedly replaced"

        identity = profile / "identity.env"
        ticket = profile / "ticket"
        assert identity.is_file() and not identity.is_symlink(), "identity must be an independently created file"
        assert identity.read_text(encoding="utf-8") == f"IROH_SECRET={key}\n", "identity content mismatch"
        assert stat.S_IMODE(identity.stat().st_mode) == 0o600, "identity permissions must be 0600"
        assert ticket.read_text(encoding="utf-8") == "fixture-ticket\n", "ticket content mismatch"
        assert stat.S_IMODE(ticket.stat().st_mode) == 0o600, "ticket permissions must be 0600"

    print("dumbpipe profile symlink regression OK")


if __name__ == "__main__":
    main()
