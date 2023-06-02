FROM python:3.9

ENV PIP_DISABLE_PIP_VERSION_CHECK 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /code

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY create_super_user.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/create_super_user.sh

COPY . .

CMD ["sh", "-c", "python manage.py migrate && ./create_super_user.sh && python manage.py runserver 0.0.0.0:8000"]
