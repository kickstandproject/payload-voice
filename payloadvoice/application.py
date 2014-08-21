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
Payload Voice Application
"""

from tornado.ioloop import IOLoop

from payloadvoice import asterisk
from payloadvoice import messaging
from payloadvoice.openstack.common import context
from payloadvoice.openstack.common import log

LOG = log.getLogger(__name__)


class Application(asterisk.Connection):

    def __init__(self):
        state_machine = {
            'initial': 'ring',
            'events': [
                {'name': 'start', 'src': 'ring', 'dst': 'answer'},
                {'name': 'channel_up', 'src': 'answer', 'dst': 'hold'},
                {'name': 'queue', 'src': 'hold', 'dst': 'connect'},
                {'name': 'end', 'src': '*', 'dst': 'disconnect'},
            ],
            'callbacks': {
                'onchannel_up': self.on_channel_up,
                'onend': self.on_end,
                'onqueue': self.on_queue,
                'onstart': self.on_start,
            },
        }
        super(Application, self).__init__(state_machine)
        self.bridges = dict()

    def _send_notification(self, event, payload):
        notification = event.replace(' ', '_')
        notification = 'payloadvoice.%s' % notification
        notifier = messaging.get_notifier(
            publisher_id='payloadvoice.app')
        notifier.info(context.RequestContext(), notification, payload)

    def on_channel_up(self, e):
        self.bridge_create(e.channel)

    def on_queue(self, e):
        LOG.info("Channel '%s' entered bridge '%s'" % (e.channel, e.bridge))

    def on_end(self, e):
        LOG.info("Channel '%s' hungup" % e.channel)
        self.bridge_delete(e.channel)

    def on_start(self, e):
        LOG.info("Channel '%s' start" % e.channel)
        self.answer(e.channel)

    def start(self):
        IOLoop.instance().start()
