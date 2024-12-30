FROM python:3.11.0


RUN mkdir -p /home/python_c2copine
WORKDIR /home/python_c2copine

COPY ./main.py /home/python_c2copine/
COPY ./api/ /home/python_c2copine/api/
COPY requirements.txt /home/python_c2copine

RUN pip3 install --no-cache-dir -r requirements.txt

EXPOSE 9020

# for the case of WebSocket
# ENTRYPOINT ["python", "main.py"] 

CMD ["python", "main.py"] 

# for the case of no websocket
# CMD ["gunicorn", "--workers", "2", "--bind", ":9010", "main:app"]



# docker build -t python_c2copine .
# docker run --name python_c2copine -d -p 9020:9020 python_c2copine --always=restart

