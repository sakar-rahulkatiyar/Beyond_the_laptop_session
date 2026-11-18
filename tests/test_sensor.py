"""Tests for demos/sensor.py."""

import pytest
from gpiozero import LED

from demos import sensor as sensor_demo


class FakeSensor:
    """Stands in for gpiozero's DistanceSensor with a fixed reading."""

    def __init__(self, distance_m: float) -> None:
        self.distance = distance_m


@pytest.mark.parametrize(("metres", "centimetres"), [(0.0, 0.0), (0.15, 15.0), (1.0, 100.0)])
def test_to_cm(metres: float, centimetres: float) -> None:
    assert sensor_demo.to_cm(metres) == pytest.approx(centimetres)


@pytest.mark.parametrize(("cm", "close"), [(5.0, True), (19.9, True), (20.0, False), (80.0, False)])
def test_is_close_uses_a_strict_threshold(cm: float, close: bool) -> None:
    assert sensor_demo.is_close(cm, threshold_cm=20.0) is close


def test_step_turns_the_led_on_when_something_is_close() -> None:
    with LED(sensor_demo.DEFAULT_LED_PIN) as led:
        cm = sensor_demo.step(FakeSensor(0.12), led, threshold_cm=20.0)

        assert cm == pytest.approx(12.0)
        assert led.is_lit


def test_step_turns_the_led_off_when_nothing_is_close() -> None:
    with LED(sensor_demo.DEFAULT_LED_PIN) as led:
        led.on()

        cm = sensor_demo.step(FakeSensor(0.5), led, threshold_cm=20.0)

        assert cm == pytest.approx(50.0)
        assert not led.is_lit


def test_defaults_match_the_wiring_guide() -> None:
    args = sensor_demo.parse_args([])

    assert (args.echo_pin, args.trigger_pin, args.led_pin) == (24, 23, 17)
    assert args.threshold == pytest.approx(20.0)
    assert args.interval == pytest.approx(0.2)


@pytest.mark.parametrize("threshold", ["0", "-5", "100", "150"])
def test_threshold_must_be_inside_the_sensor_range(threshold: str) -> None:
    with pytest.raises(SystemExit):
        sensor_demo.parse_args(["--threshold", threshold])
