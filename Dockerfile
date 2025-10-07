FROM tensorflow/tensorflow:2.15.0-gpu-jupyter

WORKDIR /workspace

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8888
