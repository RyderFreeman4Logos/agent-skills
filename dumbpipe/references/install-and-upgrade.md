# Install and upgrade with mise

Read this file only for first-time installation, repair, or upgrade work.

## Goals

- Install mise once.
- Let mise manage Rust, `cargo-binstall`, and dumbpipe.
- Prefer a prebuilt dumbpipe binary when it runs on the host.
- Fall back to a local source build when the prebuilt artifact requires a newer glibc.
- Keep dumbpipe on a global `latest` selector so later upgrades are one command.

## 1. Inspect before changing anything

```bash
command -v mise || true
command -v dumbpipe || true
printf 'shell=%s\n' "${SHELL:-unknown}"
```

If `mise` already works, do not reinstall it. If dumbpipe is already managed by mise, inspect it with:

```bash
mise ls cargo:dumbpipe
mise current cargo:dumbpipe 2>/dev/null || true
dumbpipe --help
```

Do not assume `dumbpipe --version` exists; use mise's package state and `dumbpipe --help` as the portable checks.

## 2. Install mise once

For Bash, Zsh, or Fish, prefer the official shell-specific installer because it installs mise and adds activation idempotently:

```bash
# Bash
curl https://mise.run/bash | sh

# Zsh
curl https://mise.run/zsh | sh

# Fish
curl https://mise.run/fish | sh
```

For another shell, use the generic installer and then follow mise's activation instructions for that shell:

```bash
curl https://mise.run | sh
```

The default binary path is normally `~/.local/bin/mise`. Start a fresh shell or activate it for the current shell before continuing. Examples:

```bash
# Bash
export PATH="$HOME/.local/bin:$PATH"
eval "$(mise activate bash)"

# Zsh
export PATH="$HOME/.local/bin:$PATH"
eval "$(mise activate zsh)"

# Fish
$HOME/.local/bin/mise activate fish | source
```

Verify:

```bash
mise --version
```

Do not add duplicate activation lines if the installer already added one.

## 3. Install Rust, cargo-binstall, and dumbpipe through mise

Run in this order:

```bash
mise use -g rust@stable
mise use -g cargo-binstall@latest
mise use -g cargo:dumbpipe@latest
```

This records the global dumbpipe selector as `latest`, normally in mise's global XDG configuration, and creates/refreshes the dumbpipe shim.

Verify:

```bash
mise ls cargo:dumbpipe
"$HOME/.local/share/mise/shims/dumbpipe" --help
```

If the shim is unexpectedly absent after a successful install:

```bash
mise reshim
```

## 4. glibc mismatch fallback

Mise uses an external `cargo-binstall` when available. Mise automatically falls back to `cargo install` only when cargo-binstall reports “no prebuilt artifact” using its designated exit code. A downloaded binary that later fails with a message such as `GLIBC_2.xx not found` is a different failure and needs an explicit source build.

First try the source path while preserving the global `latest` selector:

```bash
MISE_CARGO_BINSTALL=false mise use -g cargo:dumbpipe@latest
```

If mise considers the broken version already installed, force a source reinstall:

```bash
MISE_CARGO_BINSTALL=false mise install --force cargo:dumbpipe@latest
mise reshim
```

A source build may require the host's normal C build toolchain. Install only the missing distribution packages reported by the compiler. On Debian/Ubuntu, common prerequisites are `build-essential` and `pkg-config`, but do not install them blindly when compilation already succeeds.

After a glibc fallback succeeds, record the local convention so future agents do not retry an incompatible prebuilt artifact:

```bash
install_root="${XDG_CONFIG_HOME:-$HOME/.config}/dumbpipe/install"
umask 077
install -d -m 700 "$install_root"
: > "$install_root/source-build-required"
chmod 600 "$install_root/source-build-required"
```

## 5. One-line upgrades

Normal host:

```bash
mise upgrade cargo:dumbpipe
```

Host marked as requiring a local source build:

```bash
MISE_CARGO_BINSTALL=false mise upgrade cargo:dumbpipe
```

Before choosing the line, check:

```bash
test -e "${XDG_CONFIG_HOME:-$HOME/.config}/dumbpipe/install/source-build-required"
```

Mise itself can be upgraded separately:

```bash
mise self-update
```

A running service keeps the old executable mapped until it is restarted. After upgrading dumbpipe, restart and verify each affected unit, for example:

```bash
MISE_CARGO_BINSTALL=false mise upgrade cargo:dumbpipe \
  && systemctl --user restart dumbpipe-share-example.service \
  && systemctl --user --no-pager --full status dumbpipe-share-example.service
```

Use the normal upgrade command instead of the source-build command when the marker is absent.

## 6. systemd path rule

For generated user units, prefer the stable mise shim:

```text
%h/.local/share/mise/shims/dumbpipe
```

The shim tracks mise upgrades without editing every unit. Set `WorkingDirectory=%h` in units so the global mise configuration is in scope. If mise was installed with a non-default data directory, resolve the actual shim path and substitute its absolute path in the unit.
