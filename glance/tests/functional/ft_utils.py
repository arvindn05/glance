# Copyright 2018 Verizon Wireless
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import time

from oslo_serialization import jsonutils
import requests
from six.moves import http_client as http


def wait_for_status(request_path, request_headers, status='active',
                    max_sec=10, delay_sec=0.2, start_delay_sec=None):
    """
    Performs a time-bounded wait for the entity at the request_path to
    reach the requested status.

    :param request_path: path to use to make the request
    :param request_headers: headers to use when making the request
    :param status: the status to wait for (default: 'active')
    :param max_sec: the maximum number of seconds to wait (default: 10)
    :param delay_sec: seconds to sleep before the next request is
                      made (default: 0.2)
    :param start_delay_sec: seconds to wait before making the first
                            request (default: None)
    :raises Exception: if the entity fails to reach the status within
                       the requested time or if the server returns something
                       other than a 200 response
    """
    start_time = time.time()
    done_time = start_time + max_sec
    if start_delay_sec:
        time.sleep(start_delay_sec)
    while time.time() <= done_time:
        resp = requests.get(request_path, headers=request_headers)
        if resp.status_code != http.OK:
            raise Exception("Received {} response from server".format(
                resp.status_code))
        entity = jsonutils.loads(resp.text)
        if entity['status'] == status:
            return
        time.sleep(delay_sec)
    entity_id = request_path.rsplit('/', 1)[1]
    msg = "Entity {0} failed to reach status '{1}' within {2} sec"
    raise Exception(msg.format(entity_id, status, max_sec))
