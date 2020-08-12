FROM python:3.7.8-stretch
ADD . /code
WORKDIR /code
#RUN python -m pip install -U matplotlib==3.2.0rc1 \
RUN pip install -r requirements.txt
CMD ["python", "app.py"]