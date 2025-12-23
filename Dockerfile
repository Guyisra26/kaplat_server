FROM  python:3.11-slim
WORKDIR /app
COPY . .
RUN pip install --no-cache-dir -r requirements.txt
RUN mkdir -p logs
EXPOSE 8496
CMD ["python", "server.py"]
