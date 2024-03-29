#!/usr/bin/python3
# -*- coding: utf-8 -*-

import json
from src.error import eprint
import requests


class Client:
    def __init__(self, addr="http://localhost:60606"):
        self.address = addr
        self.code    = None
        self.session = requests.Session()

    def connect(self, username, password):
        return self.login(username, password)

    def __check_response(self, response):
        if response is None:
            eprint("No response received.")
            self.code = None
            return False
        if response.status_code >= 500:
            eprint("Server error: " + str(response.status_code))
            self.code = response.status_code
            return False
        if response.status_code >= 400:
            eprint("Client error: " + str(response.status_code))
            self.code = response.status_code
            return False

        self.code = response.status_code
        return True

    def start_timer(self, time, action, script):
        address = self.address + "/api/timer/start"
        data = {"time": time, "action": action, "script": script}
        response = self.session.post(address, json=data, timeout=5)
        return True if self.__check_response(response) else False

    def stop_timer(self):
        address = self.address + "/api/timer/stop"
        response = self.session.get(address, timeout=5)
        return True if self.__check_response(response) else False

    def stat_timer(self) -> dict:
        address = self.address + "/api/timer/status"
        response = self.session.get(address, timeout=5)
        if not self.__check_response(response):
            return dict()
        else:
            return response.json()

    def start_monitor(self, monitors):
        address = self.address + "/api/monitor/start"
        response = self.session.post(address, json=monitors, timeout=5)
        return True if self.__check_response(response) else False

    def stop_monitor(self):
        address = self.address + "/api/monitor/stop"
        response = self.session.get(address, timeout=5)
        return True if self.__check_response(response) else False

    def stat_monitor(self) -> dict:
        address = self.address + "/api/monitor/status"
        response = self.session.get(address, timeout=5)
        if not self.__check_response(response):
            return dict()
        else:
            return response.json()

    def get_processes(self) -> dict:
        address = self.address + "/api/get/processes"
        response = self.session.get(address, timeout=5)
        if not self.__check_response(response):
            return dict()
        else:
            return response.json()

    def permissons_view(self) -> dict:
        address = self.address + "/api/permissions/view"
        response = self.session.get(address, timeout=5)
        if not self.__check_response(response):
            return dict()
        else:
            return response.json()

    def permissions_edit(self, username, level):
        address = self.address + "/api/permissions/edit/" + username + "/" + str(level)
        response = self.session.get(address, timeout=5)
        return True if self.__check_response(response) else False

    def login(self, username, password):
        address = self.address + "/api/login"
        data = {"login": username, "password": password}
        try:
            response = self.session.post(address, json=data, timeout=5)
        except requests.exceptions.ConnectionError as e:
            eprint(str(e))
            return False
        return True if self.__check_response(response) else False

    def logout(self):
        address = self.address + "/api/logout"
        response = self.session.get(address, timeout=5)
        return True if self.__check_response(response) else False
