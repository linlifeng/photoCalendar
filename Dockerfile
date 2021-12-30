FROM python

RUN mkdir -p /home/app
COPY app.py /home/app/
COPY requirements.txt /home/app/
COPY static /home/app/static
COPY templates /home/app/templates
RUN pip install -r /home/app/requirements.txt 

CMD ["python", "/home/app/app.py"]
