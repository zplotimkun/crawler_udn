FROM python:3.6

WORKDIR /app
COPY . .

ENV RUNFILE crawler_udn.py
RUN pip install -r requirements.txt

CMD ["sh", "-c", "python -u $RUNFILE"]
