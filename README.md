# TickTick Integration from Home Assistant

This integration adds a custom service `ticktick.add_task`, which allows you to dynamically add tasks your Todo-list.

## Installation

Add this repository to [HACS](https://hacs.xyz/) and install over the Integrations tab.

## Exposed Services

- `ticktick.add_task`
  Adding a task with title and content. Optionally, a `due_date` can be set.
- `ticktick.get_projects`
  Lists all projects and their ID. You can use the IDs to add a Task to a specific List/Project

### Missing features:

- Allow changing of priority
