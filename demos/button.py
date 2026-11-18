#!/usr/bin/env python3
"""Step 2: add a button.

Press the button and the LED toggles. There is no loop: gpiozero calls
``led.toggle`` for us every time the button is pressed. Reacting to events
like this, instead of checking again and again, is how most real systems work.

Wiring (Pi powered off):
    LED:    same as step 1 (GPIO17 / pin 11 through 330 ohm, GND / pin 9)
    Button: one leg -> GPIO2 (physical pin 3), other leg -> GND (physical pin 6)

The button needs no resistor: gpiozero turns on the pin's pull-up.

Run it:
    python3 demos/button.py
    python3 demos/button.py --bounce-time 0.1    # if one press toggles twice

Press Ctrl+C to stop.
"""

import argparse
import logging
from signal import pause

from gpiozero import LED, Button

DEFAULT_LED_PIN = 17  # physical pin 11
DEFAULT_BUTTON_PIN = 2  # physical pin 3
DEFAULT_BOUNCE_S = 0.05  # ignore contact bounce shorter than 50 ms

log = logging.getLogger(__name__)


def non_negative_float(text: str) -> float:
    """Parse a command-line value that must be zero or more.

    Args:
        text: The value as typed on the command line.

    Returns:
        The parsed number.

    Raises:
        argparse.ArgumentTypeError: If the number is negative.
    """
    value = float(text)
    if value < 0:
        raise argparse.ArgumentTypeError(f"must be 0 or more, got {text}")
    return value


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    """Read the command-line options.

    Args:
        argv: Arguments to parse. ``None`` reads them from ``sys.argv``.

    Returns:
        The parsed options.
    """
    parser = argparse.ArgumentParser(description="Toggle an LED each time a button is pressed.")
    parser.add_argument(
        "--led-pin",
        type=int,
        default=DEFAULT_LED_PIN,
        help="GPIO number of the LED (default: %(default)s, which is physical pin 11)",
    )
    parser.add_argument(
        "--button-pin",
        type=int,
        default=DEFAULT_BUTTON_PIN,
        help="GPIO number of the button (default: %(default)s, which is physical pin 3)",
    )
    parser.add_argument(
        "--bounce-time",
        type=non_negative_float,
        default=DEFAULT_BOUNCE_S,
        help="seconds to ignore switch bounce after a press, 0 to turn off (default: %(default)s)",
    )
    return parser.parse_args(argv)


def connect(button: Button, led: LED) -> None:
    """Make every press of ``button`` toggle ``led``.

    Args:
        button: The button to watch.
        led: The LED to toggle.
    """
    button.when_pressed = led.toggle


def main(argv: list[str] | None = None) -> int:
    """Wait for button presses until Ctrl+C is pressed.

    Args:
        argv: Command-line arguments. ``None`` reads them from ``sys.argv``.

    Returns:
        The process exit code.
    """
    args = parse_args(argv)
    logging.basicConfig(level=logging.INFO, format="%(message)s")

    led = LED(args.led_pin)
    # gpiozero expects None, not 0, to turn debouncing off.
    button = Button(args.button_pin, bounce_time=args.bounce_time or None)
    connect(button, led)
    log.info(
        "Press the button on GPIO%d to toggle the LED on GPIO%d. Press Ctrl+C to stop.",
        args.button_pin,
        args.led_pin,
    )
    try:
        pause()  # sleep until a signal arrives; button events still run
    except KeyboardInterrupt:
        log.info("Stopped.")
    finally:
        button.close()
        led.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
