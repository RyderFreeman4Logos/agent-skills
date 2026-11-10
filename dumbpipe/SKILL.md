---
name: dumbpipe
description: Install, upgrade, configure, supervise, and troubleshoot n0-computer/dumbpipe for encrypted TCP, Unix-socket, and SSH forwarding (OpenSSH ProxyCommand, including Termux/Android). Use this skill to share or receive a local service, connect with ssh/scp/sftp via an iroh ticket, create stable reusable tickets, manage dumbpipe with mise, deploy a systemd user service, allow several receiver devices, rotate access, or recover an unavailable tunnel.
compatibility: Foreground use requires a supported dumbpipe platform. Unix-socket workflows require Unix. Persistent systemd user services require Linux with a working systemd user manager.
metadata:
  version: "1.0.0"
---

# Dumbpipe

Use dumbpipe as a small encrypted transport between a **share side** and a **receive side**:

- The share side runs `listen-tcp` or `listen-unix` and connects each remote stream to an existing local backend.
- The receive side normally runs `connect-tcp` or `connect-unix` to create a local port or socket; for SSH, prefer per-session `dumbpipe connect` through OpenSSH `ProxyCommand`, with **no local listener**.

The names describe the Iroh side, not necessarily the local socket action. This distinction prevents the most common command reversal.

## Required workflow

1. Identify the role: share, receive, or both.
2. Identify the backend and any required local endpoint:
   - TCP: host/interface and port (including the actual `sshd` port when forwarding SSH).
   - Unix: absolute socket path.
   - SSH via `ProxyCommand`: remote SSH username, host alias, and ticket; **no receiver-side port/socket**.
3. When using a local TCP receiver, decide whether it must be loopback-only or intentionally reachable from the LAN. Default it to `127.0.0.1`, never `0.0.0.0`, unless the user explicitly requests LAN exposure.
4. Check `dumbpipe --help` before relying on remembered flags. If dumbpipe or mise is missing, or an upgrade is requested, read [references/install-and-upgrade.md](references/install-and-upgrade.md).
5. For a reusable share, create or reuse a persistent profile exactly as described in [references/persistent-profiles-and-tickets.md](references/persistent-profiles-and-tickets.md). Do not rotate or overwrite an existing identity without explicit user intent.
6. Follow the role-specific guide:
   - Share: [references/share-side.md](references/share-side.md)
   - SSH, SCP, or SFTP receive side (including Termux): [references/ssh-over-dumbpipe.md](references/ssh-over-dumbpipe.md), **preferred over `connect-tcp` for SSH**.
   - Other receive-side TCP/Unix applications: [references/receive-side.md](references/receive-side.md)
7. Validate in the foreground before creating a service whenever practical.
8. If a long-running share or receiver process needs persistence, unless already requested, ask after successful validation:

   > Should I install and enable this as a persistent systemd user service with `systemctl --user enable --now ...`?

   Do **not** create a receiver-side service for an SSH `ProxyCommand`: it runs on demand for each SSH connection. A share-side `listen-tcp` service can still be persistent.
9. If accepted, read [references/systemd-user-services.md](references/systemd-user-services.md), generate a profile-specific unit, enable it, inspect its status and logs, and test the forwarded service again.
10. For outages or repeated failures, read [references/recovery-and-diagnostics.md](references/recovery-and-diagnostics.md).

## Non-negotiable rules

- A persistent ticket requires the same persistent `IROH_SECRET`. Saving only a ticket printed by an ephemeral listener is not a complete persistent setup.
- Store persistent material under `${XDG_CONFIG_HOME:-$HOME/.config}/dumbpipe/` with directories mode `0700` and secret/ticket files mode `0600`.
- Never disclose `IROH_SECRET`. It is the endpoint's private identity. A ticket is not the private key, but treat it as connection-sensitive information and do not publish it unintentionally.
- Give each independently operated share profile its own `IROH_SECRET`. Do not run several independent listener processes concurrently with the same identity.
- Do not use bare, one-shot `listen` stdio mode for a multi-client persistent service; it stops after its first successful session. `connect` **is appropriate** as a per-SSH-connection `ProxyCommand` against a persistent `listen-tcp` share.
- `listen-tcp` and `listen-unix` can accept multiple endpoint connections and streams. One ticket can therefore be used by multiple receiver devices concurrently.
- There is no built-in per-receiver ticket revocation model. To revoke devices independently, give each device or trust group a separate share profile and ticket. Rotating one shared profile invalidates access for every receiver using it.
- Prefer `Restart=always` for dumbpipe user services. Some current code paths can exit successfully even when the intended local bind failed, so `Restart=on-failure` is not sufficient.
- Restart once as a recovery attempt. If that does not restore service, inspect the backend, ticket, bind address, socket permissions, network, and logs; then retry with bounded backoff rather than a tight loop.

## Reference loading map

Read only the files needed for the current task:

- First installation, glibc fallback, or upgrades: [references/install-and-upgrade.md](references/install-and-upgrade.md)
- Stable identity, XDG layout, ticket generation, verification, or rotation: [references/persistent-profiles-and-tickets.md](references/persistent-profiles-and-tickets.md)
- Publishing a TCP port or Unix socket: [references/share-side.md](references/share-side.md)
- Consuming a ticket through a local TCP port or Unix socket: [references/receive-side.md](references/receive-side.md)
- SSH, SCP, SFTP, `ProxyCommand`, or Termux/Android: [references/ssh-over-dumbpipe.md](references/ssh-over-dumbpipe.md)
- `systemctl --user enable`, boot persistence, unit templates, or lingering: [references/systemd-user-services.md](references/systemd-user-services.md)
- Unavailable or unstable service, blocked `dns.iroh.link`/n0 relays, or explicit relay selection: [references/recovery-and-diagnostics.md](references/recovery-and-diagnostics.md)
- Encryption, exposure, ticket sharing, multi-device behavior, and revocation boundaries: [references/security-and-semantics.md](references/security-and-semantics.md)
- Re-checking upstream facts or behavior after a dumbpipe/mise release: [references/upstream-sources.md](references/upstream-sources.md)

## Completion report

Report the following without printing the secret:

- Role and transport on each side.
- Share profile name and the path containing its persistent ticket.
- Local backend or receiver address/socket; for `ProxyCommand`, report the SSH aliases and ticket **variable names or file paths**, never actual ticket values.
- Whether TCP is loopback-only or LAN-exposed (or no receiver-side listener for `ProxyCommand`).
- Foreground test result.
- Unit name and enabled/active status, when deployed.
- Whether user lingering was enabled.
- Multi-receiver/revocation implications when one ticket will be copied to several devices.
