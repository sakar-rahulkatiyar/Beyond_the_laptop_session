# Security Policy

## Supported versions

Only the latest version on the `main` branch is supported.

## Reporting a vulnerability

Please don't report security problems in public issues. Use GitHub's [private vulnerability reporting](https://github.com/sakar-rahulkatiyar/Beyond_the_laptop_session/security/advisories/new), or email rahul@sakarrobotics.com.

## Known limits

These are teaching demos, not production code:

- `demos/web.py` uses Flask's built-in development server with no login, and it switches the LED with plain GET requests so that a phone's address bar can do it. Run it only on a network you trust, such as your phone's hotspot, and never expose it to the internet.
- The demos run as your normal user and don't need `sudo`.
