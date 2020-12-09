#!/usr/bin/python3
# -*- coding: utf-8 -*-

import src.error
import requests

port = "60606"
address = "localhost:" + port


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
        return True

    def __check_connection(response):
        if response:
            pass
            # TODO

    # Public methods
    def start_timer(self):
        # TODO
        pass

    def stop_timer(self):
        response = self.session.get(address + "/api/timer/stop", timeout=5)
        return True if __check_response(response) else False

    def stat_timer(self):
        response = self.session.get(address + "/api/timer/status", timeout=5)
        return True if __check_response(response) else False

    def start_monitor(self):
        # TODO
        pass

    def stop_monitor(self):
        response = self.session.get(address + "/api/monitor/stop", timeout=5)
        return True if __check_response(response) else False

    def stat_monitor(self):
        response = self.session.get(address + "/api/monitor/status", timeout=5)
        return True if __check_response(response) else False

    def login(self, username, password):
        response = self.session.post(address + "/api/login", data='{"login":user, "password":password}', timeout=5)
        __check_connection(response)
        return True if __check_response(response) else False

    def logout(self):
        response = self.session.get(address + "/api/logout", timeout=5)
        return True if __check_response(response) else False
