"""The TickTick integration."""
import asyncio

from requests import Session
import voluptuous as vol

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.core import ServiceCall

from requests import Session
from typing import Callable
from .const import DOMAIN
from .api import login, add_task

CONFIG_SCHEMA = vol.Schema({DOMAIN: vol.Schema({})}, extra=vol.ALLOW_EXTRA)


def handle_add_task(session: Session) -> Callable:
    def handler(call: ServiceCall):
        title = call.data.get('title', '')
        content = call.data.get('content', '')
        due_date = call.data.get('due_date', '')
        add_task(session, title, content, due_date)
    return handler


def setup(hass: HomeAssistant, config):
    """Set up the TickTick integration."""
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Set up TickTick from a config entry."""

    session = login(entry.data.get('username'), entry.data.get('password'))
    if DOMAIN not in hass.data:
        hass.data[DOMAIN] = {}
    hass.data[DOMAIN][entry.entry_id] = session
    hass.services.async_register(DOMAIN, 'add_task', handle_add_task(session))

    return True
