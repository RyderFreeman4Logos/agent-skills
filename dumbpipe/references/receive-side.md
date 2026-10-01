# Receive-side workflows

Read this file when the user has a dumbpipe ticket and wants a local TCP port or Unix socket that forwards to the share side.

## Store the received ticket

Use an XDG receiver profile. Do not place the ticket in shell history when avoidable.

```bash
set -euo pipefail
profile="example"
ticket="${DUMBPIPE_TICKET:?Set DUMBPIPE_TICKET without a trailing newline}"
case "$profile" in
  ""|*[!A-Za-z0-9_.-]*)
    printf 'Invalid dumbpipe profile name: %s\n' "$profile" >&2
    exit 2
    ;;
esac

profile_dir="${XDG_CONFIG_HOME:-$HOME/.config}/dumbpipe/receivers/$profile"
umask 077
install -d -m 700 "$profile_dir"
printf '%s\n' "$ticket" >"$profile_dir/ticket"
chmod 600 "$profile_dir/ticket"
```

For interactive entry without echoing the ticket:

```bash
IFS= read -r -s -p 'Dumbpipe ticket: ' DUMBPIPE_TICKET
printf '\n'
export DUMBPIPE_TICKET
```

The ticket is a positional command argument. `IROH_SECRET` is not the ticket and normally does not need to persist on the receive side.

## Receive through a local TCP port

Default to loopback-only:

```bash
profile="example"
local_addr="127.0.0.1:3001"
profile_dir="${XDG_CONFIG_HOME:-$HOME/.config}/dumbpipe/receivers/$profile"

exec "$HOME/.local/share/mise/shims/dumbpipe" \
  connect-tcp --addr "$local_addr" "$(tr -d '\r\n' <"$profile_dir/ticket")"
```

Use `0.0.0.0:<port>` or `[::]:<port>` only when the user explicitly wants other LAN hosts to reach the receiver. State that this creates an additional local-network exposure boundary and verify the host firewall and application authentication.

Check that the selected local port is free before starting:

```bash
ss -ltn
```

## Receive through a local Unix socket

Prefer a runtime path rather than XDG config because Unix sockets are ephemeral runtime objects:

```bash
set -euo pipefail
profile="example"
profile_dir="${XDG_CONFIG_HOME:-$HOME/.config}/dumbpipe/receivers/$profile"
runtime_root="${XDG_RUNTIME_DIR:-/run/user/$(id -u)}"
local_dir="$runtime_root/dumbpipe-$profile"
local_socket="$local_dir/listener.sock"

install -d -m 700 "$local_dir"
exec "$HOME/.local/share/mise/shims/dumbpipe" \
  connect-unix --socket-path "$local_socket" \
  "$(tr -d '\r\n' <"$profile_dir/ticket")"
```

Dumbpipe removes an existing file at its receive-side Unix socket path before binding, but it does not create a missing parent directory. Verify ownership and permissions before replacing any path; never point it at an unrelated socket.

## Mixed transport is valid

The two local transports do not have to match. Examples:

- Share-side `listen-unix` plus receive-side `connect-tcp` exposes a remote Unix backend through a local TCP port.
- Share-side `listen-tcp` plus receive-side `connect-unix` exposes a remote TCP backend through a local Unix socket.

The ticket selects the remote endpoint; the chosen `connect-*` command selects the local presentation.

## Validate the application

Test the actual protocol through the new local endpoint. Examples:

```bash
# HTTP over local TCP
curl --fail --show-error http://127.0.0.1:3001/

# Confirm a local Unix socket exists
stat "$local_socket"
test -S "$local_socket"
```

Use an application-specific client for non-HTTP protocols. A listening local port alone is not proof that the remote share/backend is usable.

## Service question

After foreground validation, ask unless already decided:

> Should I install and enable this receiver as `dumbpipe-receive-<profile>.service` using `systemctl --user enable --now`?

If accepted, continue with [systemd-user-services.md](systemd-user-services.md).

## Reusing one ticket on several devices

Yes: several devices may store the same ticket and run their own `connect-tcp` or `connect-unix` processes against one `listen-tcp`/`listen-unix` share. They can be active concurrently.

All such devices share the same access lifecycle. Dumbpipe does not let the sender revoke only one of them while preserving the same shared ticket for the others. Use distinct share profiles/tickets when independent revocation is required.
