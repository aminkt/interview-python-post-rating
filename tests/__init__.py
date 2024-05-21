import os
import sys
import django

# Add the parent directory to the Python path to allow imports from the 'src' directory
sys.path.append('/app/src')

# Set the Django settings module for the test environment
os.environ['DJANGO_SETTINGS_MODULE'] = 'project.settings'

# Initialize Django
django.setup()