FROM python

RUN mkdir -p /home/app
COPY requirements.txt /home/app/
RUN pip install -r /home/app/requirements.txt 

COPY static /home/app/static
COPY templates /home/app/templates
COPY app.py /home/app/

CMD ["python", "/home/app/app.py"]
