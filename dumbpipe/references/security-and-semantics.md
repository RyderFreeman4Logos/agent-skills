# Security and operating semantics

Read this file when deciding exposure, sharing one ticket with several devices, revocation, or the security boundary.

## What dumbpipe provides

Dumbpipe uses Iroh endpoints and QUIC. Iroh attempts direct connectivity through NAT traversal and hole punching and falls back to a relay when a direct path cannot be established. The transport is encrypted with TLS.

Endpoint addressing is based on a 256-bit endpoint identity rather than a fixed IP address, so a persistent identity can remain address-independent across ordinary location changes.

## What dumbpipe does not provide

Do not claim that dumbpipe adds application accounts, HTTP authorization, per-user roles, request filtering, rate limits, or per-receiver revocation. The forwarded application still needs its own authentication and authorization where appropriate.

A ticket lets a holder locate and attempt to connect to the endpoint. It is not the endpoint's private key and cannot by itself impersonate the sender, but it should still be distributed only to intended receivers.

`IROH_SECRET` is the endpoint's private identity material. Never send it to a receiver, paste it into chat, commit it, or include it in logs.

## One ticket, multiple receiver devices

For `listen-tcp` and `listen-unix`, **yes**: one ticket can be used by multiple receive-side devices, including concurrently. The listener loops over incoming endpoint connections, and each accepted stream is forwarded to a new local backend connection.

For stdio `listen`, **no persistent multi-client guarantee**: it stops accepting after the first successful session and then exits.

## Revocation consequence

All devices holding the same ticket share one access lifecycle. Rotating the share identity/ticket revokes all of them together once the old listener stops. Dumbpipe has no built-in operation equivalent to “revoke receiver B but keep receiver A on this same ticket.”

Use separate share profiles/tickets for:

- Independent device revocation.
- Different trust groups.
- Different audit or availability policies.
- Different backend authorization boundaries.

This can require multiple listener processes and possibly multiple local ports/sockets, but it is the cleanest dumbpipe-level isolation.

## Local exposure defaults

- Share-side backend: prefer loopback or a protected Unix socket when the application does not need LAN exposure.
- Receive-side TCP: bind `127.0.0.1:<port>` by default.
- Receive-side Unix: place the socket under `$XDG_RUNTIME_DIR` with a mode-`0700` parent.
- Bind `0.0.0.0:<port>` or `[::]:<port>` only on explicit request and after checking firewall and application authentication.

Dumbpipe's encrypted remote transport does not make an intentionally LAN-exposed receive port private.

## File and log handling

Recommended permissions:

```text
XDG dumbpipe directories: 0700
identity.env:              0600
ticket / ticket.env:       0600
systemd unit files:        0600 or 0644, but never embed IROH_SECRET directly
```

A listener prints connection instructions/ticket information to stderr. Under systemd this may enter the user's journal. Do not export journals publicly without reviewing them. A correctly configured persistent listener should not print its private key because `IROH_SECRET` is already supplied.

## Identity collision rule

Use a unique secret for each independently operated share profile. Reusing one endpoint identity in multiple simultaneous listener processes creates ambiguous ownership/routing and makes lifecycle operations unsafe even if a particular version appears to tolerate it.

## Mixed local transports

The share and receive commands can mix TCP and Unix sockets. Encryption and remote routing occur between Iroh endpoints; the local adapters on either end are independent choices.

## Application-level limits still apply

Even though a dumbpipe listener can carry many connections, the backend may have its own concurrency, session, licensing, authentication, or state constraints. Confirm those before promising that many receiver devices can safely use the application at once.
