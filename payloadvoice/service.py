# vim: tabstop=4 shiftwidth=4 softtabstop=4

# Copyright (C) 2012-2014 eNovance <licensing@enovance.com>
#
# Author: Julien Danjou <julien@danjou.info>
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import sys

from oslo.config import cfg

from payloadvoice import messaging
from payloadvoice.openstack.common import log

LOG = log.getLogger(__name__)


def prepare_service(argv=None):
    if argv is None:
        argv = sys.argv
    cfg.CONF(argv[1:], project='payloadvoice')
    log.setup('payloadvoice')
    messaging.setup()
