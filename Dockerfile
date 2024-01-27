FROM apache/airflow:2.8.1-python3.11

ADD requirements.txt .
RUN pip install -r requirements.txt

USER root
RUN apt-get update \
  && apt-get install -y --no-install-recommends \
    vim \
  && apt-get autoremove -yqq --purge \
  && apt-get clean \
  && apt-get install wget -y \
  && rm -rf /var/lib/apt/lists/*

USER airflow
