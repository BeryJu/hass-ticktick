# TickTick Integration from Home Assistant

This integration adds a custom service `ticktick.add_task`, which allows you to dynamically add tasks your Todo-list.

## Installation

Add this repository to [HACS](https://hacs.xyz/) and install over the Integrations tab.

## Exposed Services

- `ticktick.add_task`

  Adding a task with title and content. Optionally, a `due_date` can be set.

  The `due_date` can either be in the format of `+123`, which will create a Task due in 123 Minutes.

  Otherwise, you can set `due_date` to an absolute date. This must be in a format supported by [dateutil](https://dateutil.readthedocs.io/en/stable/parser.html#module-dateutil.parser)
- `ticktick.get_projects`

  Lists all projects and their ID. You can use the IDs to add a Task to a specific List/Project

## Google Assistant

This requires IFTTT and an externally reachable HASS instance.

**Instructions based on [this](https://github.com/aFrankLion/hass-google_keep#ifttt-applet-and-home-assistant-automation)**

A combination of the [Google Assistant](https://ifttt.com/google_assistant) trigger and the [Webhooks](https://ifttt.com/maker_webhooks) action is used to trigger the new Home Assistant service via Google Assistant.
One IFTTT applet must be made per Google Keep list of interest, with the list name (e.g., 'Grocery' in the example below) hardcoded into the applet.
For example:

**IF**: Google Assistant/Say a phrase with a text ingredient

- _What do you want to say?_: `Add $ to the grocery list`
- _What do you want the Assistant to say in response?_: `Okay, adding $ to your grocery list`

**THEN**: Webhooks/Make a web request

- _URL_: `https://thisismyhassurl.org/api/webhook/ABCXYZ123456`
- _Method_: `POST`
- _Content Type_: `application/json`
- _Body_: `{ "action":"call_service", "service":"ticktick.add_task", "title":"{{TextField}}", "project":"whatever your project ID is" }`

A Home Assistant automation to receive and process Google Assistant inputs via IFTTT can have the form:

```yaml
automation:
  - id: ifttt_google_assistant_ticktock
    alias: "IFTTT: Google Assistant to TickTick"
    trigger:
      platform: event
      event_type: ifttt_webhook_received
      event_data:
        action: call_service
    action:
      - service_template: "{{ trigger.event.data.service }}"
        data_template:
          title: "{{ trigger.event.data.title }}"
          project: "{{ trigger.event.data.project }}"
```

### Missing features:

- Allow changing of priority
