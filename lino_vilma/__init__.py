# -*- coding: UTF-8 -*-
# Copyright 2014-2017 Luc Saffre
# License: BSD (see file COPYING for details)
"""This is the main module of Lino Vilma.

.. autosummary::
   :toctree:

   lib


"""

from os.path import join, dirname
fn = join(dirname(__file__), 'setup_info.py')
exec(compile(open(fn, "rb").read(), fn, 'exec'))

__version__ = SETUP_INFO['version']

intersphinx_urls = dict(docs="http://vilma.lino-framework.org")
srcref_url = 'https://github.com/lino-framework/vilma/blob/master/%s'
