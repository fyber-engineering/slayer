FROM python:3.6

ADD slayer /slayer
RUN pip install -r /slayer/requirements.txt

WORKDIR /slayer
ENV PYTHONPATH '/slayer/'

CMD ["python" , "/slayer/prometheus.py"]