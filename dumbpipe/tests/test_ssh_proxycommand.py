#!/usr/bin/env python3
"""Regression-test the documented OpenSSH ProxyCommand recipes without a network."""

from __future__ import annotations

import os
import re
import shutil
import subprocess
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REFERENCE = ROOT / "references/ssh-over-dumbpipe.md"
SKILL = ROOT / "SKILL.md"


def ssh_with_mock(config: Path, alias: str, env: dict[str, str], receipt: Path) -> None:
    """The proxy mock exits before any real SSH transport or network is possible."""
    receipt.unlink(missing_ok=True)
    cmd = [
        "ssh",
        "-F", str(config),
        "-o", "BatchMode=yes",
        "-o", "ConnectTimeout=2",
        alias,
    ]
    result = subprocess.run(cmd, env=env, capture_output=True, text=True, timeout=8, check=False)
    assert result.returncode != 0, "the deliberately failing proxy should prevent SSH from connecting"
    assert receipt.is_file(), (
        f"SSH failed to launch dumbpipe via ProxyCommand for {alias}:\n"
        f"stdout: {result.stdout}\nstderr: {result.stderr}"
    )


def main() -> None:
    docs = REFERENCE.read_text(encoding="utf-8")
    skill = SKILL.read_text(encoding="utf-8")
    assert "references/ssh-over-dumbpipe.md" in skill
    assert "CARGO_PROFILE_RELEASE_PANIC=unwind" in docs
    assert "StrictHostKeyChecking" in docs
    blocks = re.findall(r"\x60\x60\x60sshconfig\n(.*?)\n\x60\x60\x60", docs, re.DOTALL)
    assert len(blocks) == 2, f"expected two documented SSH config variants, found {len(blocks)}"

    for block in blocks:
        assert "HostKeyAlias" not in block, "should rely on separate SSH Host aliases"
        assert "HostName localhost" not in block, "do not collapse distinct host key identities"
        assert "StrictHostKeyChecking no" not in block

    if not shutil.which("ssh"):
        print("Skipping SSH config execution: openssh-client is not installed")
        return

    with tempfile.TemporaryDirectory(prefix="dumbpipe-ssh-proxy-regression-") as tmp:
        temp = Path(tmp)
        homedir = temp / "home"
        bindir = temp / "bin"
        homedir.mkdir()
        bindir.mkdir()
        receipt = temp / "receipt"
        dumbpipe = bindir / "dumbpipe"
        dumbpipe.write_text(
            "#!/bin/sh\n"
            "printf '%s\\n' \"$#\" \"$1\" \"$2\" > \"$DUMBPIPE_TEST_RECEIPT\"\n"
            "exit 77\n",
            encoding="utf-8",
        )
        dumbpipe.chmod(0o755)

        env = os.environ.copy()
        env.update(
            HOME=str(homedir),
            PATH=str(bindir) + os.pathsep + os.environ.get("PATH", ""),
            DUMBPIPE_TEST_RECEIPT=str(receipt),
            TICKET_HOME="endpoint-fixture-home",
            TICKET_WORK="endpoint-fixture-work",
        )

        config = temp / "ssh_config"
        config.write_text(blocks[0] + "\n", encoding="utf-8")
        config.chmod(0o600)
        for alias, ticket in (("home", "endpoint-fixture-home"), ("work", "endpoint-fixture-work")):
            ssh_with_mock(config, alias, env, receipt)
            assert receipt.read_text(encoding="utf-8").splitlines() == [
                "2", "connect", ticket
            ], f"incorrect forwarding for {alias}"

        config.write_text(blocks[1] + "\n", encoding="utf-8")
        config_home = temp / "xdg-config"
        ticket_dir = config_home / "dumbpipe/receivers/home"
        ticket_dir.mkdir(parents=True)
        ticket_dir.chmod(0o700)
        ticket_path = ticket_dir / "ticket"
        ticket_path.write_text("endpoint-fixture-xdg\n", encoding="utf-8")
        ticket_path.chmod(0o600)
        env["XDG_CONFIG_HOME"] = str(config_home)
        env.pop("TICKET_HOME", None)
        env.pop("TICKET_WORK", None)

        ssh_with_mock(config, "home", env, receipt)
        assert receipt.read_text(encoding="utf-8").splitlines() == [
            "2", "connect", "endpoint-fixture-xdg"
        ], "XDG ticket file was not passed as one argument"

        # Effective SSH configuration must not force 'localhost' as HostName.
        inspect = subprocess.run(
            ["ssh", "-G", "-F", str(config), "home"],
            env=env,
            capture_output=True,
            text=True,
            timeout=8,
            check=True,
        )
        assert "hostname home\n" in inspect.stdout
        assert "hostkeyalias " not in inspect.stdout.lower()

    print("dumbpipe SSH ProxyCommand regression OK (env + XDG file recipes)")


if __name__ == "__main__":
    main()
