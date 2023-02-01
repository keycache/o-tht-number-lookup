from django.test import TestCase
from django.urls import reverse

from ..constants import (
    AREA_CODE,
    COUNTRY_CODE,
    ERROR,
    LOCAL_PHONE_NUMBER,
    MSG_INV_FORMAT,
    MSG_INV_PHONE_NUMBER,
    MSG_REQ_MISSING,
    PHONE_NUMBER,
)
from ..controller import phone_number_controller


class TestPhoneNumberController(TestCase):
    def test_success_get_phone_number(self):
        test_data = (
            (("+12125690123", "US", "212", "5690123"), ("2125690123", "US")),
            (("+12125690123", "US", "212", "5690123"), ("+12125690123", "")),
        )
        for result, input in test_data:
            out = phone_number_controller.get_phone_number(
                **{PHONE_NUMBER: [input[0]], COUNTRY_CODE: [input[1]]}
            )
        self.assertEqual(
            out,
            {
                PHONE_NUMBER: result[0],
                COUNTRY_CODE: result[1],
                AREA_CODE: result[2],
                LOCAL_PHONE_NUMBER: result[3],
            },
        )

    def test_error_get_phone_number(self):
        test_data = (
            ({COUNTRY_CODE: MSG_REQ_MISSING}, ("2125690123", "")),
            ({PHONE_NUMBER: MSG_INV_PHONE_NUMBER}, ("+2125690123", "")),
            ({PHONE_NUMBER: MSG_INV_PHONE_NUMBER}, ("12125690123", "")),
            ({PHONE_NUMBER: MSG_INV_FORMAT}, ("*2125690123", "US")),
            ({PHONE_NUMBER: MSG_INV_FORMAT}, ("2  125690123", "US")),
        )
        for result, input in test_data:
            out = phone_number_controller.get_phone_number(
                **{PHONE_NUMBER: [input[0]], COUNTRY_CODE: [input[1]]}
            )
        self.assertEqual(
            out,
            {PHONE_NUMBER: input[0], ERROR: result},
        )


class TestPhoneNumberView(TestCase):
    def test_get(self):
        test_data = (
            (("+12125690123", "US", "212", "5690123"), ("2125690123", "US")),
            (("+12125690123", "US", "212", "5690123"), ("+12125690123", "")),
        )
        for result, input in test_data:
            response = self.client.get(
                reverse("phonenumber:phone-numbers"),
                {PHONE_NUMBER: input[0], COUNTRY_CODE: input[1]},
                HTTP_ACCEPT="application/json",
            )

        self.assertEqual(
            response.json(),
            {
                PHONE_NUMBER: result[0],
                COUNTRY_CODE: result[1],
                AREA_CODE: result[2],
                LOCAL_PHONE_NUMBER: result[3],
            },
        )
