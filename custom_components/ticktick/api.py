"""ticktick api client"""
import datetime
import json
from typing import Dict

import requests

from .const import ADD_TASK_URL, AUTH_URL, PROJECT_URL, TICKTICK_HOST


class TickTick:
    """Simple TickTick API Client"""

    _session: requests.Session

    def __init__(self):
        self._session = requests.Session()

    def login(self, username: str, password: str):
        """Log into ticktick api. ValueError is thrown when credentials are incorrect"""
        resp = self._session.post(f"https://{TICKTICK_HOST}{AUTH_URL}",
                                  json={
                                      'username': username,
                                      'password': password,
                                  })
        if resp.status_code != 200:
            raise ValueError("Invalid credentials")

    @staticmethod
    def datetime_to_json(dt: datetime.datetime) -> str:
        """Convert datetime object to string for TickTick"""
        # Example format: 2019-12-20T23:00:00.000+0000
        return dt.strftime("%Y-%m-%dT%H:%M:%S.000+0000")

    def get_projects(self) -> Dict[str, str]:
        """Return a dict of all project IDs and their names"""
        resp = self._session.get(
            f"https://{TICKTICK_HOST}{PROJECT_URL}")
        projects = {}
        for raw_project in resp.json().get('projectProfiles'):
            projects[raw_project.get('id')] = raw_project.get('name')
        return projects

    def add_task(self,
                 task_title: str,
                 content: str = '',
                 project: str = '',
                 due_date: datetime.datetime = None) -> bool:
        # Create Task
        if not due_date:
            # If there's no due_date set, we default to today
            due_date = datetime.datetime.now()
        data = {
            'sortOrder': 1,
            'title': task_title,
            'dueDate': TickTick.datetime_to_json(due_date),
            'content': content,
            'projectId': project
        }
        resp = self._session.post(
            f"https://{TICKTICK_HOST}{ADD_TASK_URL}", json=data)
        if resp.status_code == 200:
            return True
        return False
