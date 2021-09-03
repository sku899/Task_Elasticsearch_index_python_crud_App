FROM python:3.9.6
COPY . .
RUN pip install Flask requests
RUN pip install flask_wtf
RUN pip install wtforms
RUN pip install email_validator
RUN pip install elasticsearch
RUN pip install flask
#EXPOSE 5000
ENTRYPOINT ["python"]
CMD ["es_app.py"]



