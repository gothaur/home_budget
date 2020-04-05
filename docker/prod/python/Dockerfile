FROM python:3.6-slim
MAINTAINER gothaur@localhost

#COPY ./home_budget /home_budget
COPY /home_budget /home_budget

WORKDIR /home_budget

RUN pip install -r requirements/prod.txt

#COPY ./docker/prod/python/entrypoint.sh /entrypoint.sh
COPY /docker/prod/python/entrypoint.sh /entrypoint.sh

RUN chmod u+x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]

#CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]