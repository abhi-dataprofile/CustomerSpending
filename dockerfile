FROM python:3.9
WORKDIR /app
#RUN apt-get update && apt-get install -y ffmpeg

COPY app/streamlit /app/streamlit

COPY requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir -r /app/requirements.txt
RUN pip install streamlit

#EXPOSE 8501
EXPOSE 8080

CMD ["streamlit", "run", "streamlit/streamlit_main.py", "--server.port", "8080", "--server.address", "0.0.0.0"]