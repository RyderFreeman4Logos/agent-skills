# Recovery and diagnostics

Read this file when a dumbpipe route is unavailable, unstable, or repeatedly restarting.

## Recovery principle

A restart is a reasonable first recovery attempt because it recreates the local Iroh endpoint and local listener state. It is not a substitute for diagnosis. If one controlled restart does not recover service, do not hammer the service with rapid restarts.

Use these retry delays for manual or external health-driven recovery:

```text
15 seconds, 30 seconds, 60 seconds, 120 seconds, then 300 seconds between later attempts
```

Stop retrying when the user asks, when a destructive ambiguity appears, or when a persistent configuration error is identified. Native systemd backoff should handle process exits on systemd 254+; older units should use at least a 30-second fixed restart delay.

## 1. Classify the failure

Determine which statement is true:

- The systemd unit is inactive or failed.
- The process is active but the local TCP port/socket is absent.
- The local endpoint exists but requests fail immediately.
- Requests connect locally but hang or fail remotely.
- Only the application protocol fails; transport appears open.
- The service works intermittently after network changes.

This classification determines whether to inspect systemd, local binding, the ticket/remote route, or the backend application.

## 2. Inspect before restarting

```bash
unit_name="dumbpipe-share-example.service"  # adjust role/profile
systemctl --user --no-pager --full status "$unit_name" || true
journalctl --user -u "$unit_name" -n 150 --no-pager || true
systemctl --user show "$unit_name" \
  -p ActiveState -p SubState -p Result -p ExecMainCode -p ExecMainStatus \
  -p NRestarts || true
```

Check the relevant local endpoints:

```bash
ss -ltn
ss -lun
find "${XDG_RUNTIME_DIR:-/run/user/$(id -u)}" -maxdepth 2 -type s -ls 2>/dev/null
```

For a Unix backend or receiver, also use `test -S` and `stat` on the exact path.

## 3. Verify the share backend

On a share-side service, first prove the original backend works without dumbpipe:

- TCP: connect directly to the configured backend host/port with its normal client.
- Unix: verify the socket exists, has the expected owner/mode, and accepts its normal client.

Restarting dumbpipe cannot restore a backend application that is down.

## 4. Perform one controlled restart

```bash
systemctl --user restart "$unit_name"
sleep 15
systemctl --user --no-pager --full status "$unit_name"
journalctl --user -u "$unit_name" -n 100 --no-pager
```

Test the real application data path, not merely the process state.

If it still fails, wait according to the backoff schedule before another attempt and investigate the causes below. Do not run an unbounded `while true; do restart; done` loop.

## 5. High-value failure checks

### Local bind conflict

A different process may own the receiver port. Current `connect-tcp` can log a bind error and then exit successfully. This is why the recommended unit uses `Restart=always`.

```bash
ss -ltnp 2>/dev/null || ss -ltn
```

Change the local port only with user approval, or stop the conflicting process when it is clearly owned by the intended workflow.

### Missing Unix parent directory or bad permissions

`connect-unix` can remove an existing target path before binding, but it requires the parent directory to exist and be writable. For a systemd receiver, prefer `RuntimeDirectory=` as documented in the service guide.

### Wrong or rotated ticket

Compare the receiver's stored ticket with the sender's intended current ticket through an approved channel. Do not expose the sender secret.

On the sender, verify that the saved secret re-derives the saved ticket using [persistent-profiles-and-tickets.md](persistent-profiles-and-tickets.md).

### Ephemeral sender identity

If the sender starts without `IROH_SECRET`, every restart can create a different identity. Repair it by creating a persistent share profile and redistributing its verified short ticket.

### Duplicate identity use

Do not run independent listeners simultaneously with the same `IROH_SECRET`. Stop duplicates and assign each share profile its own identity.

### Remote/backend unavailable while process remains alive

Some forwarding errors happen inside per-connection tasks and are logged while the main process continues accepting local connections. In that state, systemd sees an active service and cannot infer data-plane health. A single restart may reset state, but repeated restarts will not repair an offline sender, invalid ticket, failed relay path, or dead backend.

### Network or relay reachability

Dumbpipe attempts direct NAT traversal and can fall back to an Iroh relay. Inspect DNS, outbound UDP/TCP policy, captive portals, VPN/firewall changes, and time synchronization. Do not assume that opening the application TCP port on the Internet is required; that is not how dumbpipe routes the remote connection.

### Incompatible prebuilt binary

A `GLIBC_... not found` message is an installation problem, not a tunnel problem. Follow the source-build fallback in [install-and-upgrade.md](install-and-upgrade.md).

## 6. When process restart policy is insufficient

Systemd's `Restart=` reacts to process exit. It does not know whether a still-running dumbpipe process can complete an application request. For a critical service, use an application-level health check outside dumbpipe that:

1. Sends a harmless real request through the receiver endpoint.
2. Requires several consecutive failures before acting.
3. Restarts the unit once.
4. Uses the bounded backoff schedule if failure persists.
5. Records the failure and restart reason.

Do not probe a state-changing API without a safe health endpoint. Do not deploy an aggressive watchdog merely because one request timed out.

## 7. Escalation report

When recovery fails, report:

- Unit state, restart count, and last meaningful log error.
- Whether the original share backend works directly.
- Whether the receiver local port/socket exists.
- Whether the sender profile ticket re-derives correctly.
- Whether the ticket was recently rotated.
- Whether multiple listeners share one identity.
- Whether network/VPN/firewall conditions changed.
- Last retry time and next backoff interval.

Never include `IROH_SECRET` in the report.
