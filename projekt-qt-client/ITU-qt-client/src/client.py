#!/usr/bin/python3
# -*- coding: utf-8 -*-

import json
import src.error
import requests

address = "0.0.0.0"
port = "60606"
address += ":" + port


class Client:
    def __init__(self):
        self.session = requests.Session()

    def connect(self, username, password):
        return self.login(username, password)

    # Private methods
    def __check_response(self, response):
        if response is None:
            eprint("No response received.")
            return False
        if response.status_code != 200:
            eprint("Bad response. Code: " + response.status_code)
            return False
        succesful = json.loads(response.json())
        if not succesful["success"]:
            eprint("Request was not succesful.")
            return False
        return True

    # Public methods
    def start_timer(self, time, action, script):
        data = {  # TODO ked tak neviem co dostanem
            "time": time,
            "action": action,
            "script": script
        }
        response = self.session.post(address + "/api/timer/start", data=data, timeout=5)
        return True if __check_response(response) else False

    def stop_timer(self):
        response = self.session.get(address + "/api/timer/stop", timeout=5)
        return True if __check_response(response) else False

    def stat_timer(self):
        response = self.session.get(address + "/api/timer/status", timeout=5)
        return True if __check_response(response) else False

    def start_monitor(self, time, action, resource):
        data = {  # TODO ked tak neviem co dostanem
            "time": time,
            "action": action,
            "resource": resource
        }
        response = self.session.post(address + "/api/monitor/start", data=data, timeout=5)
        return True if __check_response(response) else False

    def stop_monitor(self):
        response = self.session.get(address + "/api/monitor/stop", timeout=5)
        return True if __check_response(response) else False

    def stat_monitor(self):
        response = self.session.get(address + "/api/monitor/status", timeout=5)
        return True if __check_response(response) else False

    def login(self, username, password):
        data = {
            "login": username,
            "password": password
        }
        response = self.session.post(address + "/api/login", data=data, timeout=5)
        return True if __check_response(response) else False

    def logout(self):
        response = self.session.get(address + "/api/logout", timeout=5)
        return True if __check_response(response) else False
