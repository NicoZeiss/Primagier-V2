from django.core.management.base import BaseCommand, CommandError
from django.core import management
import os



class Command(BaseCommand):
	help = "Run tests and product report"

	# The command launch coverage analysis, and make a report in the shell
	def handle(self, *args, **options):
		os.system("coverage run --omit */env/* manage.py test")	
		os.system("coverage report")
