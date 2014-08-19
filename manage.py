#!/usr/bin/env python
import os
import sys


if __name__ == "__main__":
    environment = os.environ.get('ENVIRONMENT', 'LOCAL')
    if environment == 'LOCAL':
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'radio.settings.local')
    elif environment == 'LIVE':
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'radio.settings.live')

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
