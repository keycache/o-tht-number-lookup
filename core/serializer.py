from typing import Any, Dict, Tuple

from rest_framework.request import Request
from rest_framework.serializers import ModelSerializer, Field
from rest_framework.exceptions import ValidationError


class BaseSerializer(ModelSerializer):
    def __init__(self, *args, **kwargs):
        self.context_source = kwargs.pop("context_source", None)
        super().__init__(*args, **kwargs)

    @property
    def request(self) -> Request:
        return self.context["request"]


class ChoicesField(Field):
    def __init__(self, choices, **kwargs):
        self._choices = choices
        self.choices = ','.join([c.value for c in choices])
        super(ChoicesField, self).__init__(**kwargs)

    def to_representation(self, obj):
        return self._choices[obj]

    def to_internal_value(self, data):
        try:
            return getattr(self._choices, data)
        except AttributeError as ae:
            raise ValidationError(
                detail={"message": f"{data} not a valid choice({self.choices})", "error": str(ae)}
            )