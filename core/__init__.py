from django_petra.core import initialize

from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv(), override=True)

initialize()
