"""Tests for demos/web.py."""

from collections.abc import Iterator

import pytest
from flask.testing import FlaskClient
from gpiozero import LED

from demos import web as web_demo


@pytest.fixture
def led() -> Iterator[LED]:
    with LED(web_demo.DEFAULT_LED_PIN) as device:
        yield device


@pytest.fixture
def client(led: LED) -> FlaskClient:
    app = web_demo.create_app(led)
    app.testing = True
    return app.test_client()


def test_on_switches_the_led_on(client: FlaskClient, led: LED) -> None:
    response = client.get("/led/on")

    assert response.status_code == 200
    assert response.get_data(as_text=True) == "ON"
    assert led.is_lit


def test_off_switches_the_led_off(client: FlaskClient, led: LED) -> None:
    led.on()

    response = client.get("/led/off")

    assert response.status_code == 200
    assert response.get_data(as_text=True) == "OFF"
    assert not led.is_lit


def test_status_reports_the_current_state(client: FlaskClient, led: LED) -> None:
    assert client.get("/led").get_data(as_text=True) == "OFF"

    led.on()

    assert client.get("/led").get_data(as_text=True) == "ON"


@pytest.mark.parametrize("state", ["blink", "ON", "1", "true"])
def test_unknown_states_are_rejected(client: FlaskClient, led: LED, state: str) -> None:
    response = client.get(f"/led/{state}")

    assert response.status_code == 400
    assert not led.is_lit


def test_home_page_links_to_both_states(client: FlaskClient) -> None:
    page = client.get("/").get_data(as_text=True)

    assert 'href="/led/on"' in page
    assert 'href="/led/off"' in page


def test_defaults_match_the_slides() -> None:
    args = web_demo.parse_args([])

    assert (args.host, args.port, args.led_pin) == ("0.0.0.0", 5000, 17)  # noqa: S104


@pytest.mark.parametrize("port", ["0", "65536", "http"])
def test_port_must_be_valid(port: str) -> None:
    with pytest.raises(SystemExit):
        web_demo.parse_args(["--port", port])
