"""Shared test fixtures.

gpiozero's MockFactory replaces the real GPIO pins with simulated ones, so the
tests run on any computer. No Raspberry Pi is needed.
"""

from collections.abc import Iterator

import pytest
from gpiozero import Device
from gpiozero.pins.mock import MockFactory


@pytest.fixture(autouse=True)
def mock_pins() -> Iterator[MockFactory]:
    """Give every test a fresh set of simulated GPIO pins."""
    factory = MockFactory()
    Device.pin_factory = factory
    yield factory
    factory.reset()
