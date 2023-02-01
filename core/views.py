from django.shortcuts import render
from rest_framework.serializers import ModelSerializer
from rest_framework.views import APIView


class BaseAPIView(APIView):
    def get_serializer(self, *args, **kwargs) -> ModelSerializer:
        SerializerClass = self.serializer_class
        if not SerializerClass:
            raise NotImplementedError("Missing value for 'serializer_class'")
        return SerializerClass(
            context={"request": self.request}, *args, **kwargs
        )
