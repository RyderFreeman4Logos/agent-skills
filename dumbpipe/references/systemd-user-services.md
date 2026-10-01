# systemd user services

Read this file only after the user asks for persistence or accepts the service question.

## Preconditions

```bash
command -v systemctl
systemctl --user show-environment >/dev/null
systemctl --version | head -n 1
```

Resolve these values before writing a unit:

- Sanitized profile name: `^[A-Za-z0-9_.-]+$`
- Absolute XDG profile path
- Actual mise dumbpipe shim path, normally `%h/.local/share/mise/shims/dumbpipe`
- Exact backend or local receiver endpoint
- systemd major version

Use one unit per profile:

- Share: `dumbpipe-share-<profile>.service`
- Receive: `dumbpipe-receive-<profile>.service`

Do not silently replace a unit with different semantics. Show or diff an existing unit before changing it.

## Restart policy

Use this base policy:

```ini
[Unit]
StartLimitIntervalSec=0

[Service]
Restart=always
RestartSec=15s
```

`StartLimitIntervalSec=0` prevents systemd from permanently stopping automatic retries after a short burst. `Restart=always` is intentional: current `connect-tcp` code can return a successful process status after a local TCP bind error, which `Restart=on-failure` would miss. Explicit `systemctl --user stop` still stops the service without immediately restarting it.

For systemd 254 or newer, add native increasing delay:

```ini
RestartSteps=5
RestartMaxDelaySec=5min
```

For older systemd, omit those two unknown directives and use a conservative fixed delay instead:

```ini
RestartSec=30s
```

Do not create a tight restart loop.

## Prepare environment files

A share profile already has `identity.env`:

```text
IROH_SECRET=<32-byte lowercase hex secret>
```

Keep it mode `0600` and never print it.

For a receiver service, create a systemd environment form from the stored raw ticket:

```bash
profile="example"
profile_dir="${XDG_CONFIG_HOME:-$HOME/.config}/dumbpipe/receivers/$profile"
umask 077
printf 'DUMBPIPE_TICKET=%s\n' "$(tr -d '\r\n' <"$profile_dir/ticket")" \
  >"$profile_dir/ticket.env"
chmod 600 "$profile_dir/ticket.env"
```

The ticket format contains no intended whitespace. `${DUMBPIPE_TICKET}` in `ExecStart=` expands to exactly one argument.

## Unit template: share a TCP backend

Replace every `@...@` placeholder with a literal, correctly escaped value before installation.

```ini
[Unit]
Description=Dumbpipe share @PROFILE@ to TCP backend @BACKEND@
StartLimitIntervalSec=0

[Service]
Type=simple
WorkingDirectory=%h
UMask=0077
NoNewPrivileges=true
EnvironmentFile=@ABSOLUTE_SHARE_PROFILE_DIR@/identity.env
ExecStart=%h/.local/share/mise/shims/dumbpipe listen-tcp --host @BACKEND@
Restart=always
RestartSec=15s
# Include only on systemd >= 254:
RestartSteps=5
RestartMaxDelaySec=5min

[Install]
WantedBy=default.target
```

Example backend: `127.0.0.1:3000`.

## Unit template: share a Unix backend

```ini
[Unit]
Description=Dumbpipe share @PROFILE@ to Unix backend
StartLimitIntervalSec=0

[Service]
Type=simple
WorkingDirectory=%h
UMask=0077
NoNewPrivileges=true
EnvironmentFile=@ABSOLUTE_SHARE_PROFILE_DIR@/identity.env
ExecStart=%h/.local/share/mise/shims/dumbpipe listen-unix --socket-path @ABSOLUTE_BACKEND_SOCKET@
Restart=always
RestartSec=15s
# Include only on systemd >= 254:
RestartSteps=5
RestartMaxDelaySec=5min

[Install]
WantedBy=default.target
```

Do not add `PrivateTmp=true` when the backend socket is under `/tmp`; doing so can hide the real backend socket from dumbpipe.

## Unit template: receive through TCP

```ini
[Unit]
Description=Dumbpipe receiver @PROFILE@ on @LOCAL_ADDR@
StartLimitIntervalSec=0

[Service]
Type=simple
WorkingDirectory=%h
UMask=0077
NoNewPrivileges=true
EnvironmentFile=@ABSOLUTE_RECEIVER_PROFILE_DIR@/ticket.env
ExecStart=%h/.local/share/mise/shims/dumbpipe connect-tcp --addr @LOCAL_ADDR@ ${DUMBPIPE_TICKET}
Restart=always
RestartSec=15s
# Include only on systemd >= 254:
RestartSteps=5
RestartMaxDelaySec=5min

[Install]
WantedBy=default.target
```

Default `@LOCAL_ADDR@` to `127.0.0.1:<port>`. Use an all-interface address only on explicit request.

## Unit template: receive through a Unix socket

Use a profile-specific runtime directory so it is recreated after reboot and isolated from other receiver profiles:

```ini
[Unit]
Description=Dumbpipe receiver @PROFILE@ on a local Unix socket
StartLimitIntervalSec=0

[Service]
Type=simple
WorkingDirectory=%h
UMask=0077
NoNewPrivileges=true
EnvironmentFile=@ABSOLUTE_RECEIVER_PROFILE_DIR@/ticket.env
RuntimeDirectory=dumbpipe-@PROFILE@
RuntimeDirectoryMode=0700
ExecStart=%h/.local/share/mise/shims/dumbpipe connect-unix --socket-path %t/dumbpipe-@PROFILE@/listener.sock ${DUMBPIPE_TICKET}
Restart=always
RestartSec=15s
# Include only on systemd >= 254:
RestartSteps=5
RestartMaxDelaySec=5min

[Install]
WantedBy=default.target
```

The resulting local socket is:

```text
$XDG_RUNTIME_DIR/dumbpipe-@PROFILE@/listener.sock
```

## Non-default mise or XDG paths

The templates assume the default mise data path. If the shim is elsewhere, substitute its absolute path in `ExecStart=`.

Resolve the XDG profile directory before writing the unit. `EnvironmentFile=` should contain the actual absolute path. Quote paths according to systemd syntax when they contain spaces. If mise's global configuration itself depends on a non-default `XDG_CONFIG_HOME`, add an explicit unit environment assignment with the resolved value so the shim sees the same configuration.

## Install, enable, and verify

```bash
unit_name="dumbpipe-share-example.service"  # or receive
unit_source="/path/to/rendered/$unit_name"
unit_dir="${XDG_CONFIG_HOME:-$HOME/.config}/systemd/user"

umask 077
install -d -m 700 "$unit_dir"
install -m 600 "$unit_source" "$unit_dir/$unit_name"
systemctl --user daemon-reload
systemctl --user enable --now "$unit_name"
systemctl --user --no-pager --full status "$unit_name"
journalctl --user -u "$unit_name" -n 100 --no-pager
```

Then test the actual forwarded application again. `active (running)` proves only that the process is alive.

Useful operations:

```bash
systemctl --user restart "$unit_name"
systemctl --user stop "$unit_name"
systemctl --user disable --now "$unit_name"
journalctl --user -u "$unit_name" -f
```

## Start at boot and survive logout

An enabled user unit normally starts when that user's manager starts. If the service must run before interactive login or remain managed after all sessions log out, inspect and, with user approval, enable lingering:

```bash
loginctl show-user "$USER" -p Linger
loginctl enable-linger "$USER"
loginctl show-user "$USER" -p Linger
```

Local policy may require authentication. Do not prepend `sudo` automatically. Explain that lingering keeps the user's service manager available at boot and after logout.

## Upgrade behavior

The mise shim resolves the currently selected dumbpipe version on each process start. After `mise upgrade cargo:dumbpipe`, restart affected units so they execute the new binary, and retest the forwarding path.
