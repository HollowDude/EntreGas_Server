FROM python:3.9.6-slim
WORKDIR /EntreGas-Server
COPY . .
RUN pip install -r requirements.txt
CMD ["python", "app.py"]
