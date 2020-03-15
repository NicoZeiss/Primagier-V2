import os
from django.core.management.base import BaseCommand, CommandError
from django.core import management


class Command(BaseCommand):
    """The command launch coverage analysis, and make a report in the shell"""
    help = "Run tests and product report"

	
    def handle(self, *args, **options):
        """Here is the command"""
        # os.system("coverage run --omit */env/* manage.py test")	
        # os.system("coverage report")
