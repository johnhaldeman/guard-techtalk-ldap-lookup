# (C) Copyright IBM Corp. 2018
# The source code for this program is not published or
# otherwise divested of its trade secrets, irrespective of
# what has been deposited with the US Copyright Office.

import __builtin__

import gpylib

__author__ = 'IBM'
__version__ = '0.10+16e08c9a2f65f0ffc1fdb9049b8e5c2e0cffd2cd'

__builtin__.get_app_base_url = gpylib.get_app_base_url
__builtin__.g_url_for = gpylib.g_url_for
