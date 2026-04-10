FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt && pip install --no-cache-dir Pillow>=10.0.0 aiohttp-socks
COPY . .
CMD ["python", "bot.py"]