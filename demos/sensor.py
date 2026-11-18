#!/usr/bin/env python3
"""Step 3: read a distance sensor and close the sense, think, act loop.

Move your hand towards the HC-SR04: the LED turns on when it's closer than 20 cm.

Wiring (Pi powered off):
    HC-SR04 VCC  -> 5 V (physical pin 2)
    HC-SR04 TRIG -> GPIO23 (physical pin 16)
    HC-SR04 ECHO -> 1 kohm -> GPIO24 (physical pin 18), plus 2 kohm from GPIO24 to GND
    HC-SR04 GND  -> GND (physical pin 20)
    LED:            same as step 1 (GPIO17 / pin 11)

The ECHO pin outputs 5 V. The 1 kohm / 2 kohm voltage divider brings it down to
about 3.3 V. Never connect ECHO straight to a GPIO pin.

Run it:
    python3 demos/sensor.py
    python3 demos/sensor.py --threshold 30

gpiozero may print a PWMSoftwareFallback warning when it starts. It is harmless.
Press Ctrl+C to stop.
"""

import argparse
import logging
from time import sleep
from typing import Protocol

from gpiozero import LED, DistanceSensor

DEFAULT_ECHO_PIN = 24  # physical pin 18, through the voltage divider
DEFAULT_TRIGGER_PIN = 23  # physical pin 16
DEFAULT_LED_PIN = 17  # physical pin 11
DEFAULT_THRESHOLD_CM = 20.0
DEFAULT_INTERVAL_S = 0.2  # five readings a second
MAX_DISTANCE_M = 1.0  # gpiozero reports this value when no echo comes back

log = logging.getLogger(__name__)


class DistanceReader(Protocol):
    """Anything that reports a distance in metres, such as :class:`gpiozero.DistanceSensor`."""

    @property
    def distance(self) -> float:
        """The latest distance reading, in metres."""


class Output(Protocol):
    """Anything with a writable on/off ``value``, such as :class:`gpiozero.LED`."""

    value: bool


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
    parser = argparse.ArgumentParser(
        description="Turn an LED on when something is close to an HC-SR04 sensor."
    )
    parser.add_argument(
        "--threshold",
        type=positive_float,
        default=DEFAULT_THRESHOLD_CM,
        help="distance in cm below which the LED turns on (default: %(default)s)",
    )
    parser.add_argument(
        "--interval",
        type=positive_float,
        default=DEFAULT_INTERVAL_S,
        help="seconds between readings (default: %(default)s)",
    )
    parser.add_argument(
        "--echo-pin",
        type=int,
        default=DEFAULT_ECHO_PIN,
        help="GPIO number of ECHO, through the divider (default: %(default)s)",
    )
    parser.add_argument(
        "--trigger-pin",
        type=int,
        default=DEFAULT_TRIGGER_PIN,
        help="GPIO number of TRIG (default: %(default)s)",
    )
    parser.add_argument(
        "--led-pin",
        type=int,
        default=DEFAULT_LED_PIN,
        help="GPIO number of the LED (default: %(default)s)",
    )
    args = parser.parse_args(argv)

    max_cm = to_cm(MAX_DISTANCE_M)
    if args.threshold >= max_cm:
        parser.error(f"--threshold must be below {max_cm:.0f} cm, the sensor's maximum range")
    return args


def to_cm(distance_m: float) -> float:
    """Convert a distance in metres, as gpiozero reports it, to centimetres.

    Args:
        distance_m: Distance in metres.

    Returns:
        The same distance in centimetres.
    """
    return distance_m * 100


def is_close(distance_cm: float, threshold_cm: float) -> bool:
    """Think: decide whether something is closer than the threshold.

    Args:
        distance_cm: The measured distance in centimetres.
        threshold_cm: The distance below which something counts as close.

    Returns:
        ``True`` if the object is closer than ``threshold_cm``.
    """
    return distance_cm < threshold_cm


def step(sensor: DistanceReader, led: Output, threshold_cm: float) -> float:
    """Run one pass of the loop: sense, think, act.

    Args:
        sensor: Where to read the distance from.
        led: The output to switch.
        threshold_cm: The distance below which the LED turns on.

    Returns:
        The measured distance in centimetres.
    """
    cm = to_cm(sensor.distance)  # sense
    led.value = is_close(cm, threshold_cm)  # think -> act
    return cm


def main(argv: list[str] | None = None) -> int:
    """Read the sensor and drive the LED until Ctrl+C is pressed.

    Args:
        argv: Command-line arguments. ``None`` reads them from ``sys.argv``.

    Returns:
        The process exit code.
    """
    args = parse_args(argv)
    logging.basicConfig(level=logging.INFO, format="%(message)s")

    sensor = DistanceSensor(
        echo=args.echo_pin, trigger=args.trigger_pin, max_distance=MAX_DISTANCE_M
    )
    led = LED(args.led_pin)
    log.info(
        "The LED turns on under %.0f cm. Press Ctrl+C to stop.",
        args.threshold,
    )
    try:
        while True:
            cm = step(sensor, led, args.threshold)
            print(f"{cm:.0f} cm", flush=True)
            sleep(args.interval)
    except KeyboardInterrupt:
        log.info("Stopped.")
    finally:
        led.close()
        sensor.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
