#!/usr/bin/env python
#new code here
import os
import sys

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings.local")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
