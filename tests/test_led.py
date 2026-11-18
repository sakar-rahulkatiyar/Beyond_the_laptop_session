"""Tests for demos/led.py."""

import pytest
from gpiozero import LED

from demos import led as led_demo


def test_blink_toggles_once_per_cycle() -> None:
    with LED(led_demo.DEFAULT_LED_PIN) as led:
        led_demo.blink(led, interval=0.001, cycles=3)

        led.pin.assert_states([False, True, False, True])


@pytest.mark.parametrize(("cycles", "lit"), [(1, True), (2, False), (5, True)])
def test_blink_ends_in_the_expected_state(cycles: int, lit: bool) -> None:
    with LED(led_demo.DEFAULT_LED_PIN) as led:
        led_demo.blink(led, interval=0.001, cycles=cycles)

        assert led.is_lit is lit


def test_defaults_match_the_wiring_guide() -> None:
    args = led_demo.parse_args([])

    assert args.pin == 17
    assert args.interval == 0.5


@pytest.mark.parametrize("value", ["0", "-1", "fast"])
def test_interval_must_be_a_positive_number(value: str) -> None:
    with pytest.raises(SystemExit):
        led_demo.parse_args(["--interval", value])
