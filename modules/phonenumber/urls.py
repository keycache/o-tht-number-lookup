from django.urls import path

from .views import PhoneNumberView

app_name = "phonenumber"

urlpatterns = [
    path("phone-numbers/", PhoneNumberView.as_view(), name="phone-numbers"),
]
