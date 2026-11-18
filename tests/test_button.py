"""Tests for demos/button.py."""

import pytest
from gpiozero import LED, Button

from demos import button as button_demo


def test_each_press_toggles_the_led() -> None:
    with (
        LED(button_demo.DEFAULT_LED_PIN) as led,
        Button(button_demo.DEFAULT_BUTTON_PIN, bounce_time=None) as button,
    ):
        button_demo.connect(button, led)
        assert not led.is_lit

        button.pin.drive_low()  # press: the button connects the pin to ground
        assert led.is_lit

        button.pin.drive_high()  # release: nothing happens
        assert led.is_lit

        button.pin.drive_low()  # press again
        assert not led.is_lit


def test_defaults_match_the_wiring_guide() -> None:
    args = button_demo.parse_args([])

    assert args.led_pin == 17
    assert args.button_pin == 2
    assert args.bounce_time == pytest.approx(0.05)


def test_bounce_time_can_be_turned_off() -> None:
    args = button_demo.parse_args(["--bounce-time", "0"])

    assert args.bounce_time == 0


def test_bounce_time_cannot_be_negative() -> None:
    with pytest.raises(SystemExit):
        button_demo.parse_args(["--bounce-time", "-0.1"])
