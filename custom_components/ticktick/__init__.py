"""The TickTick integration."""
import asyncio
from typing import Callable

from requests import Session

import voluptuous as vol
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, ServiceCall
from dateutil import parser
from datetime import datetime, timedelta
from .api import TickTick
from .const import DOMAIN

CONFIG_SCHEMA = vol.Schema({DOMAIN: vol.Schema({})}, extra=vol.ALLOW_EXTRA)


def handle_add_task(client: TickTick) -> Callable:
    def handler(call: ServiceCall):
        title = call.data.get('title', '')
        content = call.data.get('content', '')
        project = call.data.get('project', '')

        due_date_raw = call.data.get('due_date', '')
        due_date = None
        if due_date_raw != "":
            if due_date_raw.startswith("+"):
                # If due_date starts with +, use it as an offest to now
                due_date = datetime.now() + timedelta(minutes=int(due_date_raw))
            else:
                # Otherwise we try to parse it absolutely
                due_date = parser.parse(due_date_raw)
        client.add_task(title, content, project, due_date)
    return handler


def handle_get_projects(client: TickTick, hass: HomeAssistant) -> Callable:
    def handler(call: ServiceCall):
        projects = client.get_projects()
        project_list = "".join([f"<li>{name}: {id}</li>" for id,
                                name in projects.items()])
        hass.components.persistent_notification.async_create(
            f"The following projects were found: <ul>{project_list}</ul>",
            title='TickTick Projects',
            notification_id='ticktick_projects_list',
        )
    return handler


def setup(hass: HomeAssistant, config):
    """Set up the TickTick integration."""
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Set up TickTick from a config entry."""

    client = TickTick()
    client.login(entry.data.get('username'), entry.data.get('password'))
    if DOMAIN not in hass.data:
        hass.data[DOMAIN] = {}
    hass.data[DOMAIN][entry.entry_id] = client

    hass.services.async_register(DOMAIN, 'add_task', handle_add_task(client))
    hass.services.async_register(
        DOMAIN, 'get_projects', handle_get_projects(client, hass))

    return True
