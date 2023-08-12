# base image  
FROM python:3.10.12  
# setup environment variable  
ENV DockerHOME=/home/app/webapp  

# set work directory  
RUN mkdir -p $DockerHOME  

# where your code lives  
WORKDIR $DockerHOME  

# set environment variables  
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1  

ENV POSTGRES_HOST  '95.173.108.164'
ENV POSTGRES_USER  'conxai'
ENV POSTGRES_PWD  'conxaipass'
ENV POSTGRES_PORT  21134
ENV POSTGRES_DB  'blurringdashboard'

ENV S3_NAME  "dev-blurring-processed-images"

# install dependencies  
RUN pip install --upgrade pip

# copy whole project to your docker home directory. 
COPY . $DockerHOME  

RUN pip install -r requirements.txt

# port where the Django app runs  
EXPOSE 8000  

# ADD entrypoint.sh /entrypoint.sh
# RUN chmod a+x /entrypoint.sh
# ENTRYPOINT ["/entrypoint.sh"]

CMD python manage.py migrate && gunicorn AlphaReport.wsgi:application -w 4 --threads 8 --bind 0.0.0.0:8000
# CMD python manage.py migrate && python manage.py runserver 0.0.0.0:8000
