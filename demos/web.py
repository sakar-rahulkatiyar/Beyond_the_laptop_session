#!/usr/bin/env python3
"""Step 4: control the LED from your phone.

Starts a small web server on the Pi. On a phone that is on the same network, open:

    http://<pi-ip>:5000/          a page with On and Off buttons
    http://<pi-ip>:5000/led/on    switch the LED on
    http://<pi-ip>:5000/led/off   switch the LED off
    http://<pi-ip>:5000/led       read the current state

Find the Pi's address with ``hostname -I``. Install Flask once with
``sudo apt install python3-flask``.

Security: this uses Flask's built-in development server with no login, and it
changes the LED with plain GET requests so a phone's address bar can do it. That
is fine for a demo on a network you trust, such as your phone's hotspot. Never
expose it to the internet; a real device would use POST requests behind
authentication. Campus Wi-Fi often blocks device-to-device traffic, so a phone
hotspot is the most reliable option.

Run it:
    python3 demos/web.py
    python3 demos/web.py --host 127.0.0.1 --port 8000

Press Ctrl+C to stop.
"""

import argparse
import logging
from typing import Protocol

from flask import Flask
from gpiozero import LED

DEFAULT_LED_PIN = 17  # physical pin 11
DEFAULT_HOST = "0.0.0.0"  # noqa: S104 - listen on every interface so phones can connect
DEFAULT_PORT = 5000

STATES = {"on": True, "off": False}

INDEX_PAGE = """<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Raspberry Pi LED</title>
  <style>
    body { font-family: system-ui, sans-serif; text-align: center; margin: 3rem 1rem; }
    a { display: block; max-width: 16rem; margin: 1rem auto; padding: 1rem;
        border-radius: 0.75rem; color: #fff; font-size: 1.5rem; text-decoration: none; }
    .on { background: #e8702a; }
    .off { background: #222; }
  </style>
</head>
<body>
  <h1>Raspberry Pi LED</h1>
  <a class="on" href="/led/on">On</a>
  <a class="off" href="/led/off">Off</a>
</body>
</html>
"""

log = logging.getLogger(__name__)


class Output(Protocol):
    """Anything with a readable and writable on/off ``value``, such as :class:`gpiozero.LED`."""

    value: bool


def port_number(text: str) -> int:
    """Parse a TCP port number from the command line.

    Args:
        text: The value as typed on the command line.

    Returns:
        The port number.

    Raises:
        argparse.ArgumentTypeError: If the port is outside 1-65535.
    """
    port = int(text)
    if not 1 <= port <= 65535:
        raise argparse.ArgumentTypeError(f"must be between 1 and 65535, got {text}")
    return port


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    """Read the command-line options.

    Args:
        argv: Arguments to parse. ``None`` reads them from ``sys.argv``.

    Returns:
        The parsed options.
    """
    parser = argparse.ArgumentParser(description="Switch an LED from a web browser.")
    parser.add_argument(
        "--host",
        default=DEFAULT_HOST,
        help="address to listen on; 127.0.0.1 allows only this Pi (default: %(default)s)",
    )
    parser.add_argument(
        "--port",
        type=port_number,
        default=DEFAULT_PORT,
        help="port to listen on (default: %(default)s)",
    )
    parser.add_argument(
        "--led-pin",
        type=int,
        default=DEFAULT_LED_PIN,
        help="GPIO number of the LED (default: %(default)s)",
    )
    return parser.parse_args(argv)


def describe(led: Output) -> str:
    """Return ``"ON"`` or ``"OFF"`` for the LED's current state.

    Args:
        led: The LED to describe.

    Returns:
        The state as text.
    """
    return "ON" if led.value else "OFF"


def create_app(led: Output) -> Flask:
    """Build the web app that controls ``led``.

    Keeping this separate from :func:`main` lets the tests pass in a mock LED.

    Args:
        led: The LED to control.

    Returns:
        The Flask application.
    """
    app = Flask(__name__)

    @app.get("/")
    def index() -> str:
        return INDEX_PAGE

    @app.get("/led")
    def status() -> str:
        return describe(led)

    @app.get("/led/<state>")
    def switch(state: str) -> tuple[str, int]:
        if state not in STATES:
            return "Unknown state. Use /led/on or /led/off.", 400
        led.value = STATES[state]
        return describe(led), 200

    return app


def main(argv: list[str] | None = None) -> int:
    """Serve the web app until Ctrl+C is pressed.

    Args:
        argv: Command-line arguments. ``None`` reads them from ``sys.argv``.

    Returns:
        The process exit code.
    """
    args = parse_args(argv)
    logging.basicConfig(level=logging.INFO, format="%(message)s")

    led = LED(args.led_pin)
    app = create_app(led)
    log.info(
        "Open http://<pi-ip>:%d/ on your phone. Find <pi-ip> with: hostname -I",
        args.port,
    )
    try:
        app.run(host=args.host, port=args.port, debug=False)
    finally:
        led.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
