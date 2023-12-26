from rest_framework.response import Response
from django.db import connection
from django.db.utils import OperationalError
from auth.vault import *
from django.http import HttpResponse


class AccessDenied:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.

        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response

    def process_exception(self, request, exception):
        if isinstance(exception, OperationalError):
            # Handle the operational error here
            # For example, you can log the error or return a custom response'

            SECRETE_DB_SERVICE = client.secrets.database.get_static_credentials(
                name=env('VAULT_DB_ROLE'),
                mount_point=env('VAULT_DB_PATH')
            )

            return request

        return HttpResponse("Database is not available. Please try again later.")

    # def process_response(self, request, response):
    #     return response
