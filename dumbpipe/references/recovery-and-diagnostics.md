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

### Blocked n0 discovery or selected relay

An active service and a valid identity-only ticket do not prove that discovery or the selected relay is reachable. Two observed failures were a blocked `dns.iroh.link` publish path and a blocked `usw1-1` relay, while `use1-1` and `euc1-1` remained reachable. A share on an unrestricted network can still be unreachable from a filtered receiver if its home relay is blocked there.

Before changing configuration:

1. Check local proxy settings, VPN and firewall policy, then compare probes on both share and receive devices. Do not disable network protections as a diagnostic shortcut.
2. Inspect private diagnostics for `Failed to publish to pkarr`, `InvalidContentType`, TLS errors and connection timeouts. Dumbpipe can print its private key even without verbose logging: keep diagnostic files mode `0600`; do not publish raw logs or send them to journald unredacted.
3. Probe discovery and candidate relays, independently of the application tunnel:

   ```sh
   curl --max-time 10 -I https://dns.iroh.link/
   curl --max-time 10 -I https://usw1-1.relay.n0.iroh.link/
   curl --max-time 10 -I https://use1-1.relay.n0.iroh.link/
   curl --max-time 10 -I https://euc1-1.relay.n0.iroh.link/
   curl --max-time 10 -I https://aps1-1.relay.n0.iroh.link/
   ```

   TLS `wrong version number` or `InvalidContentType` can indicate interception, but does not identify its cause by itself. If permitted, resolve the hostname and probe that IP over plain HTTP with the original `Host:` header; a redirect to a named vendor block page is stronger evidence. A 2026-11-09 field report identified a Charter/Spectrum CUJO block page this way. Do not generalize that diagnosis to every TLS failure. HTTP/TLS reachability is only a control probe, not proof that the relay protocol works.
4. Determine the **share's** advertised relay, not only which relay the receive device prefers. Keep tickets private. If the remote share uses a blocked home relay, changing only the receiver is insufficient.

For a verified blocked-relay path, use a relay-capable binary and preserve the existing identity:

```sh
# On the share device, with its existing IROH_SECRET already loaded.
# Stop the previous listener before reusing that identity.
"$HOME/.local/bin/dumbpipe-relay" listen-tcp --host 127.0.0.1:22 \
  --relay https://use1-1.relay.n0.iroh.link
```

Use the real backend port. Check `listen-tcp --help` for `--relay` first: stock v0.40.1 does not provide it. As checked on 2026-11-10, [upstream PR #121](https://github.com/n0-computer/dumbpipe/pull/121) is still open (head `e2181df077ff077f564bc15b3eea93b74412da9f`), and its base is another topic branch, not the release. A custom v0.40.1-based binary supplied this capability in the field, but its precise source integration was not reproducibly established; do not assume checking out that PR alone reproduces the deployed artifact. Establish and review the exact source/base, record the binary digest, test host compatibility, and install the custom binary outside mise's managed directory so an updater cannot overwrite it. Track [#121](https://github.com/n0-computer/dumbpipe/pull/121) and [#105](https://github.com/n0-computer/dumbpipe/issues/105); retire the custom build after a released replacement passes the same tests.

Save the **full ticket printed by this running listener**, including its relay route, in the existing private XDG share profile; update receiver ticket files atomically with mode `0600`. Never distribute the secret or the entire diagnostic log. A full ticket supplies the route without requiring pkarr discovery; a short identity-only ticket still depends on successful discovery. Stock v0.40.1 receivers have worked unchanged with such full tickets.

The flag can be repeated for several reachable relays, but a saved full ticket describes the relay selected at that moment. With static receiver tickets, pin one verified relay so a restart cannot select another home relay and leave tickets stale. Keep another reachable relay as an explicit fallback, refreshing receiver tickets when changing it. If selecting multiple relays, verify how clients learn the new route after every restart rather than assuming the old ticket follows it.

Back up the old unit, identity and receiver ticket before deployment. Test a temporary listener with a separate identity first, then change the production unit's executable/relay while retaining its original `IROH_SECRET`. Reload systemd and restart the affected listener, not the backend. Test a harmless request through the receiver (for SSH, the server banner/handshake, for example `ssh-keyscan -p <receiver-port> 127.0.0.1`; verify fingerprints separately). Use a genuinely separate network or an explicitly approved relay-only test so a direct LAN path cannot hide relay failure. Recheck after a listener restart and verify any health watchdog recovers. Restoring the old unit and receiver ticket, followed by `daemon-reload` and the affected unit restarts, provides rollback; it may also restore the original broken route.

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
