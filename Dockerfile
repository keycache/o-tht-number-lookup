FROM python:3.10.6-slim


WORKDIR /user/src/api

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt ./

# install dependencies
RUN pip install --upgrade pip
RUN pip install -r ./requirements.txt

# copy the project
COPY . .

# setup clean db. Not needed now
# RUN python manage.py makemigrations
# RUN python manage.py migrate


EXPOSE 8006

CMD ["python", "manage.py", "runserver", "0.0.0.0:8006"]