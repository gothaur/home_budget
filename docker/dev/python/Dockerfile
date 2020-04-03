FROM python:3.6
MAINTAINER gothaur@localhost

COPY ./home_budget /home_budget

WORKDIR /home_budget

RUN pip install -r requirements/dev.txt

COPY ./docker/dev/python/entrypoint.sh /entrypoint.sh

RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]

#CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]