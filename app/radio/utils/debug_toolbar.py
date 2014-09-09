"""debug-toolbar related customizations
"""
# future imports
from __future__ import absolute_import
from __future__ import unicode_literals

# third-party imports
from django.conf import settings


def show_debug_toolbar(request):
    """Default function to determine whether to show the toolbar on a given page.
    """

    if request.is_ajax():
        return False

    return bool(settings.DEBUG)
