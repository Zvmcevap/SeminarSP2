FROM python:3.9

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY . /code/

RUN chmod +x pre_run.sh
RUN chmod +x run_localhost.sh

CMD ["./pre_start.sh"]
CMD ["./run_localhost.sh"]
