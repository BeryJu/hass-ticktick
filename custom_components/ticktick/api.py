"""ticktick api client"""

import json
import datetime
import requests
from .const import TICKTICK_HOST, AUTH_URL, ADD_TASK_URL


def login(username: str, password: str) -> requests.Session:
    """Log into ticktick api and return `requests.Session`"""
    session = requests.Session()
    resp = session.post(f"https://{TICKTICK_HOST}{AUTH_URL}",
                        json={
                            'username': username,
                            'password': password,
                        })
    if resp.status_code != 200:
        raise ValueError("Invalid credentials")
    return session


def datetime_to_json(dt: datetime.datetime) -> str:
    """Convert datetime object to string for TickTick"""
    # Example format: 2019-12-20T23:00:00.000+0000
    return dt.strftime("%Y-%m-%dT%H:%M:%S.000+0000")


def add_task(session: requests.Session,
             task_title: str,
             content: str = '',
             due_date: datetime.datetime = None) -> bool:
    # Create Task
    if not due_date:
        # If there's no due_date set, we default to today
        due_date = datetime.datetime.now()
    data = {
        'sortOrder': 1,
        'title': task_title,
        'dueDate': datetime_to_json(due_date),
        'content': content
    }
    resp = session.post(f"https://{TICKTICK_HOST}{ADD_TASK_URL}", json=data)
    if resp.status_code == 200:
        return True
    return False
