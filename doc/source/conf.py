#!/usr/bin/env python

# Copyright (C) 2013 PolyBeacon, Inc.
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

import os
import sys


sys.path.insert(0, os.path.abspath('../..'))

extensions = ['sphinx.ext.autodoc']
templates_path = ['_templates']
source_suffix = '.rst'
master_doc = 'index'
project = u'payloadvoice'
copyright = u'2014, Paul Belanger'
pygments_style = 'sphinx'
html_theme = 'default'
htmlhelp_basename = 'payloadvoiceedoc'

latex_elements = {
}

latex_documents = [
    ('index', 'payloadvoice.tex', u'Payload Voice Documentation',
     u'Paul Belanger', 'manual'),
]

texinfo_documents = [
    ('index', 'payloadvoice', u'Payload Voice Documentation',
     u'Paul Belanger', 'payloadvoice', 'One line description of project.',
     'Miscellaneous'),
]
