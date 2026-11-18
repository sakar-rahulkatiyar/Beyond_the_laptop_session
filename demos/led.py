#!/usr/bin/env python3
"""Step 1: blink an LED.

Toggles GPIO17 every half second, so the LED blinks once a second.

Wiring (Pi powered off):
    GPIO17 (physical pin 11) -> 330 ohm resistor -> LED long leg (+)
    LED short leg (-)        -> GND (physical pin 9)

Run it:
    python3 demos/led.py
    python3 demos/led.py --interval 0.2    # blink faster

Press Ctrl+C to stop.
"""

import argparse
import logging
from time import sleep
from typing import Protocol

from gpiozero import LED

DEFAULT_LED_PIN = 17  # GPIO number used in code; the wire goes to physical pin 11
DEFAULT_INTERVAL_S = 0.5

log = logging.getLogger(__name__)


class Toggleable(Protocol):
    """Anything with a ``toggle()`` method, such as :class:`gpiozero.LED`."""

    def toggle(self) -> None:
        """Switch from on to off, or from off to on."""


def positive_float(text: str) -> float:
    """Parse a command-line value that must be a number greater than zero.

    Args:
        text: The value as typed on the command line.

    Returns:
        The parsed number.

    Raises:
        argparse.ArgumentTypeError: If the number is zero or negative.
    """
    value = float(text)
    if value <= 0:
        raise argparse.ArgumentTypeError(f"must be greater than 0, got {text}")
    return value


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    """Read the command-line options.

    Args:
        argv: Arguments to parse. ``None`` reads them from ``sys.argv``.

    Returns:
        The parsed options.
    """
    parser = argparse.ArgumentParser(description="Blink an LED connected to a GPIO pin.")
    parser.add_argument(
        "--pin",
        type=int,
        default=DEFAULT_LED_PIN,
        help="GPIO number of the LED (default: %(default)s, which is physical pin 11)",
    )
    parser.add_argument(
        "--interval",
        type=positive_float,
        default=DEFAULT_INTERVAL_S,
        help="seconds between toggles (default: %(default)s)",
    )
    return parser.parse_args(argv)


def blink(led: Toggleable, interval: float, cycles: int | None = None) -> None:
    """Toggle ``led`` every ``interval`` seconds.

    Args:
        led: The LED to toggle.
        interval: Seconds to wait after each toggle.
        cycles: How many times to toggle. ``None`` keeps going until interrupted.
    """
    count = 0
    while cycles is None or count < cycles:
        led.toggle()
        sleep(interval)
        count += 1


def main(argv: list[str] | None = None) -> int:
    """Blink the LED until Ctrl+C is pressed.

    Args:
        argv: Command-line arguments. ``None`` reads them from ``sys.argv``.

    Returns:
        The process exit code.
    """
    args = parse_args(argv)
    logging.basicConfig(level=logging.INFO, format="%(message)s")

    led = LED(args.pin)
    log.info("Blinking the LED on GPIO%d. Press Ctrl+C to stop.", args.pin)
    try:
        blink(led, args.interval)
    except KeyboardInterrupt:
        log.info("Stopped.")
    finally:
        led.close()  # release the pin so other programs can use it
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
