# Upstream sources and verification notes

Use this file to re-check behavior after upstream releases. Operational commands should be checked against the installed `dumbpipe --help` before execution.

Research snapshot: **2026-08-30**.

## Dumbpipe

- Repository and README:
  - https://github.com/n0-computer/dumbpipe
  - https://raw.githubusercontent.com/n0-computer/dumbpipe/main/README.md
- CLI implementation:
  - https://raw.githubusercontent.com/n0-computer/dumbpipe/main/src/main.rs
- Package metadata:
  - https://github.com/n0-computer/dumbpipe/blob/main/Cargo.toml
- Persistent-secret documentation issue:
  - https://github.com/n0-computer/dumbpipe/issues/92

Facts verified from the snapshot:

- `IROH_SECRET` supplies the endpoint secret; absent it, dumbpipe generates a random secret and prints it to stderr.
- `generate-ticket` creates a short endpoint ticket intended for a later listener using the same secret.
- `listen-tcp` and `listen-unix` accept multiple endpoint connections and forward streams to fresh local backend connections.
- Stdio `listen` stops after its first successful session.
- `connect-tcp` creates a local TCP listener and attempts the remote connection per accepted local connection.
- A local TCP bind error in the current `connect-tcp` implementation is logged and returns success, motivating `Restart=always` in supervised mode.
- `connect-unix` removes an existing target path before binding its local Unix listener; the parent directory still must exist.
- The README states that any number of TCP connections may flow through one dumb pipe and labels the terminal-sharing receive side as “client(s).”
- The README describes Iroh NAT traversal, relay fallback, address-independent endpoint IDs, and TLS encryption.
- At the snapshot date, `Cargo.toml` reports dumbpipe `0.39.0` and Rust `1.91` as the minimum. Do not hard-pin these values unless the user requests reproducibility.

## mise

- Installation:
  - https://mise.jdx.dev/installing-mise.html
- Cargo backend:
  - https://mise.jdx.dev/dev-tools/backends/cargo.html
- Shims:
  - https://mise.jdx.dev/dev-tools/shims.html
- Upgrade command:
  - https://mise.jdx.dev/cli/upgrade.html
- Install command:
  - https://mise.jdx.dev/cli/install.html

Facts verified from the snapshot:

- The official shell-specific installers install mise and add shell activation idempotently.
- `mise use -g rust` provides Cargo for the cargo backend.
- `mise use -g cargo:<crate>` installs and records a global `latest` selector when no version is pinned.
- When external cargo-binstall is installed, mise uses it and disables its compile strategy.
- Mise automatically falls back to `cargo install` only for cargo-binstall's designated “no prebuilt artifact” result; other binstall failures need explicit handling.
- `MISE_CARGO_BINSTALL=false` disables binstall for an invocation and forces the cargo-install path.
- `mise upgrade cargo:dumbpipe` upgrades the globally selected fuzzy/latest version.
- The default shim directory is `~/.local/share/mise/shims`, and shims are suitable for non-interactive execution.

## systemd

- Service restart behavior:
  - https://www.freedesktop.org/software/systemd/man/systemd.service.html
  - https://manpages.debian.org/testing/systemd/systemd.service.5.en.html
- Unit start limiting:
  - https://www.freedesktop.org/software/systemd/man/systemd.unit.html
  - https://man.archlinux.org/man/systemd.unit.5.en
- User lingering:
  - https://www.freedesktop.org/software/systemd/man/loginctl.html

Facts verified from the snapshot:

- `Restart=always` covers clean and unclean exits, but an explicit systemd stop does not trigger an automatic restart.
- `RestartSteps=` and `RestartMaxDelaySec=` were added in systemd 254 and provide increasing restart intervals.
- `StartLimitIntervalSec=0` disables start-rate limiting; otherwise reaching the limit can stop automatic restart attempts.
- `${NAME}` in `ExecStart=` expands one environment variable into exactly one argument, including when the variable came from `EnvironmentFile=`.
- `loginctl enable-linger` allows a user's manager to run services while the user is not logged in.

## Agent Skills format

- Specification:
  - https://agentskills.io/specification
- Authoring best practices:
  - https://agentskills.io/skill-creation/best-practices

This skill follows progressive disclosure: the required `SKILL.md` is concise, while one-time installation, detailed commands, unit templates, and troubleshooting live in focused files under `references/`.
