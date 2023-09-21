"""
Command line tool for bulk exporting a range of TCX files from Polar Flow.

Usage is as follows:

    python polarflowexport.py <username> <password> <start_date> \
                <end_date> <output_dir>

The start_date and end_date parameters are ISO-8601 date strings (i.e.
year-month-day). An example invocation is as follows:

    python polarflowexport.py me@me.com mypassword 2015-08-01 2015-08-30 \
                        /tmp/tcxfiles

Licensed under the Apache Software License v2, see:
    http://www.apache.org/licenses/LICENSE-2.0
"""

from http.cookiejar import CookieJar
from pathlib import Path
from typing import Optional, List
from urllib.parse import urlencode

import dateutil.parser
import json
import logging
import time
from html.parser import HTMLParser
from urllib.request import BaseHandler, build_opener, HTTPCookieProcessor

from polar_flow_export.factories.calendar_events import CalendarEventFactory


class ThrottlingHandler(BaseHandler):
    """A throttling handler which ensures that requests to a given host
    are always spaced out by at least a certain number of (floating point)
    seconds.
    """

    def __init__(self, throttle_seconds=1.0):
        self._throttleSeconds = throttle_seconds
        self._requestTimeDict = dict()

    def default_open(self, request):
        host_name = request.host
        last_request_time = self._requestTimeDict.get(host_name, 0)
        time_since_last = time.time() - last_request_time
        
        if time_since_last < self._throttleSeconds:
            time.sleep(self._throttleSeconds - time_since_last)
        self._requestTimeDict[host_name] = time.time()


class AjaxLoginParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.csrf_token = None

    @classmethod
    def has_attr(cls, attrs: list[tuple[str, str | None]], name: str, value: str) -> bool:
        for a_name, a_value in attrs:
            if a_name == name and a_value == value:
                return True
        return False

    @classmethod
    def get_attr(cls, attrs: list[tuple[str, str | None]], name: str) -> Optional[str]:
        for a_name, a_value in attrs:
            if a_name == name:
                return a_value
        return None

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag == "input":
            if self.has_attr(attrs, name="name", value="csrfToken"):
                self.csrf_token = self.get_attr(attrs, name="value")


class PolarFlowExporter(object):

    def __init__(self, email: str, password: str):
        self._username = email
        self._password = password
        self._logger = logging.getLogger(self.__class__.__name__)

        self._url_opener = build_opener(ThrottlingHandler(0.5), HTTPCookieProcessor(CookieJar()))
        self._url_opener.addheaders = [('User-Agent', 'https://github.com/gabrielreid/polar-flow-export')]
        self._logged_in = False

    def _execute_request(self, path: str, post_params=None) -> bytes:

        url = "https://flow.polar.com%s" % path

        self._logger.debug(f"Requesting '{url}'")

        if post_params is not None:
            post_data = urlencode(post_params).encode("utf-8")
        else:
            post_data = None

        try:
            response = self._url_opener.open(url, post_data)
            data = response.read()
        except Exception as e:
            self._logger.error(f"Error fetching {url}: {e}")
            raise e
        response.close()
        return data  

    @classmethod
    def get_epoch_time_ms(cls) -> int:
        return round(time.time() * 1000)

    @classmethod
    def _ajax_login_url(cls) -> str:
        """When getting the URL login box a Get request is made to
        https://flow.polar.com/ajaxLogin?_=<epoch_ms>"""
        return f"/ajaxLogin?_={cls.get_epoch_time_ms()}"

    def _get_csrf_token(self) -> str:
        ajax_login = self._execute_request(self._ajax_login_url())
        parser = AjaxLoginParser()
        parser.feed(ajax_login.decode("utf-8"))
        if parser.csrf_token is None:
            raise RuntimeError("Could not get csrf token, perhaps a change on the polar flow site?")
        return parser.csrf_token

    def _login(self):
        self._logger.info("Logging in user %s", self._username)
        # https://flow.polar.com/ajaxLogin?_=1694353061121
        #                                    1694353879
        csrf_token = self._get_csrf_token()
        # Start a new session
        self._execute_request(
            path='/login',
            post_params=dict(
                returnUrl='https://flow.polar.com/',
                email=self._username,
                password=self._password,
                csrfToken=csrf_token
            )
        )
        self._logged_in = True 
        self._logger.info("Successfully logged in")

    def get_files(self, from_date: str, to_date: str, output_dir: Path) -> List[str]:
        """Returns an iterator of TcxFile objects.

        @param from_date an ISO-8601 date string
        @param to_date an ISO-8601 date string
        @param output_dir
        """
        paths = []
        self._logger.info("Fetching files from %s to %s", from_date, to_date)
        if not self._logged_in:
            self._login()

        from_date = dateutil.parser.parse(from_date)
        to_date = dateutil.parser.parse(to_date)

        from_spec = "%s.%s.%s" % (from_date.day, from_date.month, from_date.year)

        to_spec = "%s.%s.%s" % (to_date.day, to_date.month, to_date.year)

        path = f"/training/getCalendarEvents?start={from_spec}&end={to_spec}"
        activity_refs = json.loads(self._execute_request(path))

        for activity_ref in activity_refs:
            assert isinstance(activity_ref, dict)
            event = CalendarEventFactory().make(activity_ref)
            paths.extend(event.store(parent_dir=output_dir, url_opener=self._execute_request))
        return paths


def export_data(email: str, password: str, from_date: str, to_date: str, output_dir: Path) -> None:
    logging.basicConfig(level=logging.INFO)
    exporter = PolarFlowExporter(email, password)
    files = exporter.get_files(from_date, to_date, Path(output_dir))
    if files:
        print(f"Created files {', '.join(files)}")
    print("Export complete")
