import re
from typing import Any, Dict, Iterable

import phonenumbers
from phonenumbers.phonenumber import PhoneNumber
from phonenumbers.phonenumberutil import (
    NumberParseException,
    length_of_geographical_area_code,
    region_code_for_country_code,
)

from core.controller import BaseController

from .constants import (
    AREA_CODE,
    COUNTRY_CODE,
    ERROR,
    LOCAL_PHONE_NUMBER,
    MSG_INV_FORMAT,
    MSG_INV_PHONE_NUMBER,
    MSG_REQ_MISSING,
    PHONE_NUMBER,
)


class PhoneNumberWrapper:
    def __init__(self, phone_number: str, country_code: str = None) -> None:
        self.phone_number: str = phone_number
        self.country_code: str = country_code
        self.full_number: str = ""
        self.area_code: str = ""
        self.local_number: str = ""
        self.is_valid: bool = False
        self.errors = {}

    def __str__(self) -> str:
        return f"PNW -> {self.phone_number}:{self.country_code}"

    def _check_country_code(
        self, phone_number: str, country_code: str
    ) -> bool:
        """Check for the country code check"""
        return phone_number.startswith("+") or (
            not phone_number.startswith("+") and country_code
        )

    def _check_redundant_characters(self, phone_number: str) -> bool:
        """Check if there are any redundant characters
        Check if consecutive spaces
        Check if any chars other than + and numbers present
        """
        return re.search(r" {2,}", phone_number) or re.search(
            "[^0-9\+]", phone_number.replace(" ", "")
        )

    def check(self) -> bool:
        """Check if the phone number is valid"""
        if not self._check_country_code(self.phone_number, self.country_code):
            self.is_valid = False
            self.errors[COUNTRY_CODE] = MSG_REQ_MISSING
            return

        if self._check_redundant_characters(self.phone_number):
            self.is_valid = False
            self.errors[PHONE_NUMBER] = MSG_INV_FORMAT
            return

        try:
            ph: PhoneNumber = phonenumbers.parse(
                number=self.phone_number, region=self.country_code
            )
            if phonenumbers.is_valid_number(ph):
                self.is_valid = True
                self.full_number = self.get_full_number(phone_number=ph)
                self.country_code = self.get_country_code(phone_number=ph)
                self.area_code = self.get_area_code(phone_number=ph)
                self.local_number = self.get_local_number(phone_number=ph)
            else:
                self.is_valid = False
                self.errors[PHONE_NUMBER] = MSG_INV_PHONE_NUMBER
        except NumberParseException as npe:
            self.is_valid = False
            self.errors[PHONE_NUMBER] = MSG_INV_FORMAT
        return self.is_valid

    # Helper Methods
    def _get_area_code_length(self, phone_number: PhoneNumber) -> int:
        return length_of_geographical_area_code(phone_number)

    def get_local_number(self, phone_number: PhoneNumber) -> str:
        ac_len = self._get_area_code_length(phone_number=phone_number)
        nsn = phonenumbers.national_significant_number(phone_number)
        if ac_len > 0:
            return nsn[ac_len:]
        return nsn

    def get_area_code(self, phone_number: PhoneNumber) -> str:
        ac_len = self._get_area_code_length(phone_number=phone_number)
        if ac_len > 0:
            nsn = phonenumbers.national_significant_number(phone_number)
            return nsn[:ac_len]
        return ""

    def get_country_code(self, phone_number: PhoneNumber) -> str | None:
        return region_code_for_country_code(phone_number.country_code)

    def get_full_number(self, phone_number: PhoneNumber) -> str:
        return "".join(
            (
                "+",
                str(phone_number.country_code),
                str(phone_number.national_number),
            )
        )

    # Helper Methods

    def __bool__(self) -> bool:
        return self.is_valid


class PhoneNumberController(BaseController):
    def get_phone_number(self, *args, **kwargs) -> Dict[str, str]:
        phone_number = kwargs.get(PHONE_NUMBER)
        country_code = kwargs.get(COUNTRY_CODE)
        phone_number = phone_number and phone_number[0]
        country_code = country_code and country_code[0]

        phone_number = PhoneNumberWrapper(phone_number, country_code)

        if phone_number.check():
            result = {
                PHONE_NUMBER: phone_number.full_number,
                COUNTRY_CODE: phone_number.country_code,
                AREA_CODE: phone_number.area_code,
                LOCAL_PHONE_NUMBER: phone_number.local_number,
            }
        else:
            result = {
                PHONE_NUMBER: phone_number.phone_number,
                ERROR: phone_number.errors,
            }
        return result


phone_number_controller = PhoneNumberController()
