from django.shortcuts import render
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response

from core.views import BaseAPIView

from .controller import phone_number_controller


class PhoneNumberView(BaseAPIView):
    def get(self, request: Request) -> Response:
        phone_number = phone_number_controller.get_phone_number(
            **request.query_params
        )
        return Response(data=phone_number, status=status.HTTP_200_OK)
