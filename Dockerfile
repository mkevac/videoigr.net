FROM python
COPY requirements.txt /src/requirements.txt
RUN pip install -r /src/requirements.txt
COPY main.py /src/main.py
CMD ["python", "/src/main.py"]