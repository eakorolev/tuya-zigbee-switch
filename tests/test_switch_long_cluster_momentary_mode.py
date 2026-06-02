import pytest

from tests.conftest import Device, RelayButtonPair
from tests.zcl_consts import (
    ZCL_ATTR_ONOFF_CONFIGURATION_SWITCH_RELAY_INDEX,
    ZCL_CLUSTER_ON_OFF_SWITCH_CONFIG,
    ZCL_ONOFF_CONFIGURATION_RELAY_MODE_DETACHED,
    ZCL_ONOFF_CONFIGURATION_RELAY_MODE_LONG,
    ZCL_ONOFF_CONFIGURATION_SWITCH_TYPE_MOMENTARY,
)


@pytest.fixture()
def momentary_device(device: Device, relay_button_pair: RelayButtonPair) -> Device:
    device.zcl_switch_mode_set(
        relay_button_pair.switch_endpoint, ZCL_ONOFF_CONFIGURATION_SWITCH_TYPE_MOMENTARY
    )
    device.zcl_switch_relay_mode_set(
        relay_button_pair.switch_endpoint, ZCL_ONOFF_CONFIGURATION_RELAY_MODE_DETACHED
    )
    return device


def test_long_press_ep_momentary_mode_long_press_mode_relay_control(
    momentary_device: Device, relay_button_pair: RelayButtonPair
):
    momentary_device.zcl_switch_relay_mode_set(
        relay_button_pair.long_press_endpoint,
        ZCL_ONOFF_CONFIGURATION_RELAY_MODE_LONG,
    )

    momentary_device.press_button(relay_button_pair.button_pin)

    assert momentary_device.zcl_relay_get(relay_button_pair.relay_endpoint) == "0"
    assert momentary_device.get_gpio(relay_button_pair.relay_pin) == 0

    momentary_device.step_time(2_000)  # Long press

    assert momentary_device.zcl_relay_get(relay_button_pair.relay_endpoint) == "1"
    assert momentary_device.get_gpio(relay_button_pair.relay_pin) == 1

    momentary_device.release_button(relay_button_pair.button_pin)

    assert momentary_device.zcl_relay_get(relay_button_pair.relay_endpoint) == "1"
    assert momentary_device.get_gpio(relay_button_pair.relay_pin) == 1


def test_long_press_ep_momentary_mode_detached_mode_relay_control(
    momentary_device: Device, relay_button_pair: RelayButtonPair
):
    momentary_device.zcl_switch_relay_mode_set(
        relay_button_pair.long_press_endpoint,
        ZCL_ONOFF_CONFIGURATION_RELAY_MODE_DETACHED,
    )
    momentary_device.click_button(relay_button_pair.button_pin)

    assert momentary_device.zcl_relay_get(relay_button_pair.relay_endpoint) == "0"
    assert momentary_device.get_gpio(relay_button_pair.relay_pin) == 0

    momentary_device.long_click_button(relay_button_pair.button_pin)

    assert momentary_device.zcl_relay_get(relay_button_pair.relay_endpoint) == "0"
    assert momentary_device.get_gpio(relay_button_pair.relay_pin) == 0


# OnOff Commands Tests for Momentary Mode


# Level Control Commands Tests for Momentary Mode


@pytest.mark.parametrize(
    "relay_index",
    [1, 2, 3],
)
def test_long_press_ep_momentary_mode_relay_index_configuration(
    momentary_device: Device,
    relay_index: int,
    relay_button_pairs: list[RelayButtonPair],
):
    momentary_device.zcl_switch_relay_mode_set(
        relay_button_pairs[0].long_press_endpoint,
        ZCL_ONOFF_CONFIGURATION_RELAY_MODE_LONG,
    )
    momentary_device.write_zigbee_attr(
        relay_button_pairs[0].long_press_endpoint,
        ZCL_CLUSTER_ON_OFF_SWITCH_CONFIG,
        ZCL_ATTR_ONOFF_CONFIGURATION_SWITCH_RELAY_INDEX,
        relay_index,
    )

    momentary_device.long_click_button(relay_button_pairs[0].button_pin)

    target_pair = relay_button_pairs[relay_index - 1]

    assert momentary_device.zcl_relay_get(target_pair.relay_endpoint) == "1"
    assert momentary_device.get_gpio(target_pair.relay_pin) == 1

    momentary_device.long_click_button(relay_button_pairs[0].button_pin)

    assert momentary_device.zcl_relay_get(target_pair.relay_endpoint) == "0"
    assert momentary_device.get_gpio(target_pair.relay_pin) == 0
