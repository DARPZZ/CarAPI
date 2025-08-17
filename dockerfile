FROM python:3.9-slim

RUN apt-get update && apt-get install -y libgl1 libglib2.0-0 && rm -rf /var/lib/apt/lists/*



WORKDIR /usr/src/app


COPY requirements.txt ./
RUN pip install --no-cache-dir typing-extensions==4.12.2
RUN pip install --no-cache-dir torch==2.8.0 torchvision==0.23.0 --index-url https://download.pytorch.org/whl/cpu
RUN pip install --no-cache-dir -r requirements.txt


COPY . .

CMD ["python", "app.py"]
