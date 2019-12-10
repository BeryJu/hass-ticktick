#!/bin/bash
mkdir hass-config
cp -Rf custom_components hass-config/
hass -c hass-config --debug
