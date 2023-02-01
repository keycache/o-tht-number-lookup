# o-tht-number-lookup

Python implementation of a phone number lookup API

Provides an `api` - `GET` - `vi/phone-numbers` to validate a phone number.
This api supports couple of parameters

- `phoneNumber` - accepts a phone number with country code. In that case `country code is not mandatory`
- `countryCode` - Required if its not supplied in `phoneNumber`

## Implementation

- Leveraged `django` and `django-rest-framework`
- Implemented using the `model-view-controller` paradigm.
- `controller` holds the logic for validation and payload construction
- `view` is just a pass through layer to extract the necessary `query params` from the `GET` request
- `test` cases for `view` and `controller`
- dockerized the application fpr a consistent dev testing/deployment experience

## How to run the `app`

- Checkout the code
- run `make server-run-local` if your os supports `make`
- Else, if you have docker support run the commands from the project root directory

  > docker build -t o-number-lookup:latest -f ./Dockerfile .

  > docker run -p 8006:8006 --name c-o-number-lookup --rm o-number-lookup:latest

- The api will be available at `localhost:8006/v1/phone-numbers/`. Some examples
  - Invalid
    - `localhost:8006/v1/phone-numbers/?phoneNumber=%2B2125690123`
    - `localhost:8006/v1/phone-numbers/?phoneNumber=2125690123`
  - Valid
    - `localhost:8006/v1/phone-numbers/?countryCode=US&phoneNumber=2125690123`
    - `localhost:8006/v1/phone-numbers/?phoneNumber=%2B12125690123`

## How to run the `test cases`

> python manage.py test modules.phonenumber.tests.test_all
