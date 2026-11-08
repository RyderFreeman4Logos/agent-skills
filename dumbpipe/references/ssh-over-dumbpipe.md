# SSH over dumbpipe (including Termux)

Read this reference when a user wants to access SSH, SCP, or SFTP through dumbpipe, especially from Termux/Android. For SSH, prefer OpenSSH's built-in `ProxyCommand` with `dumbpipe connect` over setting up a separate local `connect-tcp` listener.

## How it works

```text
ssh / scp / sftp
  ↕ OpenSSH ProxyCommand (stdin / stdout)
dumbpipe connect <ticket>                  [receive device; one process per SSH connection]
  ↕ iroh / encrypted QUIC (direct or relay)
dumbpipe listen-tcp --host 127.0.0.1:22    [share device; long-lived listener]
  ↕ local TCP
sshd
```

OpenSSH's [ProxyCommand](https://man.openbsd.org/ssh_config.5#ProxyCommand) runs a helper process and uses its standard input/output as the SSH transport. Dumbpipe's `connect` subcommand is such a helper. Neither OpenSSH nor dumbpipe needs a special SSH integration or a receiver-side listening port. The remote `listen-tcp` listener is still required; **do not replace it with the one-shot `listen` stdio command** when multiple SSH sessions may be needed.

SSH host-key verification, authentication, encryption, multiplexing, and higher-level features remain OpenSSH's responsibility. Dumbpipe supplies an encrypted outer transport, not an alternative to SSH identity verification.

## 1. Share side: expose an existing sshd

Determine the **actual port** on which sshd listens on the share device. For a typical Linux sshd:

```sh
# On the share device; keep this listener running.
dumbpipe listen-tcp --host 127.0.0.1:22
```

Some Termux sshd installations listen on `127.0.0.1:8022` instead; use that address only when verified. Ensure sshd works locally before debugging dumbpipe.

For a stable, reusable ticket, create or reuse the share's `IROH_SECRET` profile exactly as in [persistent-profiles-and-tickets.md](persistent-profiles-and-tickets.md), then run `listen-tcp` with that identity. The sample command above is **ephemeral** unless `IROH_SECRET` is already set. Keep the share listener running (a systemd user service is suitable on supported Linux systems). A receiver needs the ticket, **never** the share-side secret.

## 2. Receive side: one ticket environment variable per host

Install `dumbpipe` and OpenSSH on the receiving device. On Termux, `pkg install openssh` provides the SSH client if it is not already installed.

In a shell startup file loaded **before** launching `ssh` (for example `~/.zshrc` when using interactive zsh), export separate ticket variables:

```sh
export TICKET_HOME='endpoint...'
export TICKET_WORK='endpoint...'
```

Replace each placeholder with the corresponding **full, valid ticket**. Treat ticket values as connection-sensitive. Do not commit them to a repository or paste them into public logs. Secure files with restrictive permissions; shell exports are inherited only by child processes of that shell, not automatically by unrelated app launches.

Put this in `~/.ssh/config` (replace `myuser` with the remote SSH username):

```sshconfig
Host home
    User myuser
    ProxyCommand dumbpipe connect "$TICKET_HOME"

Host work
    User myuser
    ProxyCommand dumbpipe connect "$TICKET_WORK"
```

No `HostName localhost` or `HostKeyAlias` is needed. The `Host home` and `Host work` aliases distinguish SSH host-key records in `known_hosts`; DNS resolution of those aliases is not required because the proxy handles the connection. **Keep `StrictHostKeyChecking` enabled and verify the sshd host-key fingerprint on first connection**. Changing a ticket must not silently change the trusted SSH server.

Use the aliases with normal SSH tooling:

```sh
ssh home
ssh -vvv work
scp ./file.txt home:~/
sftp work
```

The receiving device starts a new dumbpipe `connect` process for each OpenSSH connection. There is no receiver-side socket or background systemd service to manage.

### Alternative: use an XDG ticket file instead of exported variables

This is useful if `ssh` is started from an app that does **not** inherit your interactive shell exports. First store the received ticket under the existing per-receiver XDG profile layout documented in [receive-side.md](receive-side.md), for example:

```text
${XDG_CONFIG_HOME:-$HOME/.config}/dumbpipe/receivers/home/ticket
```

The receiver profile directory should be mode `0700` and the ticket file mode `0600`. Then use this **alternative** `~/.ssh/config` stanza (not alongside another `Host home` stanza):

```sshconfig
Host home
    User myuser
    ProxyCommand sh -c 'exec dumbpipe connect "$(cat "${XDG_CONFIG_HOME:-$HOME/.config}/dumbpipe/receivers/home/ticket")"'
```

The ticket filename is fixed in the SSH configuration; the inner shell reads the file and passes its contents as one argument to dumbpipe. This avoids depending on `TICKET_HOME` being exported, though the ticket still becomes a command-line argument to dumbpipe. Adapt the `home` profile path for other hosts. This variant requires `sh` and `cat` to be available on the receiving device.

## Termux / Android notes

On some Termux installations, a normal Rust release build of dumbpipe (observed with v0.40.1) exits with `android context was not initialized` from `ndk-context`. The following **source-build workaround** was used to avoid a process-level `abort`:

```sh
CARGO_PROFILE_RELEASE_PANIC=unwind cargo install --locked --force dumbpipe
```

This may still print a `tokio-rt-worker` panic: a panic caught internally can be printed by the panic hook without terminating dumbpipe. **Neither `panic=unwind` nor `ProxyCommand` guarantees that all Android networking problems are fixed.** In one reported Termux setup, `connect-tcp` remained unusable while `ssh` through `dumbpipe connect` and `ProxyCommand` succeeded. Do not claim this workaround is universally necessary or sufficient.

Upstream tracking: [dumbpipe #96](https://github.com/n0-computer/dumbpipe/issues/96) and [termux-packages #30605](https://github.com/termux/termux-packages/issues/30605). Check upstream behavior again when upgrading.

## Troubleshooting and security

1. Verify sshd responds locally on the share device and `listen-tcp` is running with the expected **persistent identity**.
2. Ensure the right ticket variable is exported in the shell invoking SSH: `test -n "$TICKET_HOME"` (do **not** print the ticket).
3. Use `ssh -G home` to inspect the effective SSH configuration without connecting; then `ssh -vvv home` to distinguish a proxy connection failure from SSH authentication or a host-key mismatch.
4. A local `Connection established` message from `connect-tcp` is not proof of a working remote SSH session. The SSH server banner/handshake is a better end-to-end check.
5. If using the XDG-file form, verify that the file exists, is readable by its owner, contains only the expected ticket, and has restrictive permissions.
6. Do not disable SSH host-key checking to resolve a ticket or networking error. The ticket identifies a dumbpipe endpoint; **SSH must independently authenticate the server**.
7. For a Termux DNS panic, check whether the process continued and whether SSH traffic works; the panic message alone is insufficient to diagnose the connection.

For general outages also read [recovery-and-diagnostics.md](recovery-and-diagnostics.md). For ticket exposure and revocation limits, see [security-and-semantics.md](security-and-semantics.md).
