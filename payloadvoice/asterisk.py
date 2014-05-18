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
Payload Voice ARI
"""

from ari import client
from ari import event
from fysom import Fysom
from oslo.config import cfg

from payloadvoice.openstack.common import log

ASTERISK_OPTS = [
    cfg.StrOpt(
        'uri', default='http://127.0.0.1:8088/ari',
        help='Complete Asterisk REST interface endpoint.'),
    cfg.StrOpt(
        'username', default='payload',
        help='Asterisk REST interface username.'),
    cfg.StrOpt(
        'password', default=None,
        help='Asterisk REST interface password.'),
]

ASTERISK_GROUP = cfg.OptGroup(
    name='asterisk', title='Options for Asterisk integration.')

CONF = cfg.CONF
CONF.register_group(ASTERISK_GROUP)
CONF.register_opts(ASTERISK_OPTS, ASTERISK_GROUP)

LOG = log.getLogger(__name__)


class Connection(object):

    def __init__(self, fsm):
        self._channels = dict()
        self.client = client.get_client(
            '1', ari_url=CONF.asterisk.uri,
            ari_username=CONF.asterisk.username,
            ari_password=CONF.asterisk.password)
        self.events = event.Event(
            url=CONF.asterisk.uri, username=CONF.asterisk.username,
            password=CONF.asterisk.password, app='demo')
        self.events.register_event('StasisStart', self._handle_stasis_start)
        self.events.register_event('StasisEnd', self._handle_stasis_stop)
        self.events.register_event(
            'ChannelStateChange', self._handle_channel_state_change)
        self.events.register_event(
            'ChannelEnteredBridge', self._handle_channel_entered_bridge)
        self.fsm = fsm

    def _handle_channel_entered_bridge(self, data):
        bridge = data['bridge']['id']
        channel = data['channel']['id']
        self._channels[channel].queue(channel=channel, bridge=bridge)

    def _handle_channel_state_change(self, data):
        channel = data['channel']['id']
        if data['channel']['state'] == 'Up':
            self._channels[channel].channel_up(channel=channel)

    def _handle_stasis_start(self, data):
        channel = data['channel']['id']
        self._channels[channel] = Fysom(self.fsm)
        self._channels[channel].start(channel=channel)

    def _handle_stasis_stop(self, data):
        channel = data['channel']['id']
        self._channels[channel].end(channel=channel)
        del self._channels[channel]
