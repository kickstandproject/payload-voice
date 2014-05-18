# vim: tabstop=4 shiftwidth=4 softtabstop=4

# Copyright (C) 2014 PolyBeacon, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Payload Voice Service
"""

import logging

from oslo.config import cfg

from payloadvoice import application
from payloadvoice.openstack.common import log
from payloadvoice import service

LOG = log.getLogger(__name__)


def main():
    service.prepare_service()
    app = application.Application()
    LOG.info("Configuration:")
    cfg.CONF.log_opt_values(LOG, logging.INFO)
    app.start()
