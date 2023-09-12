FROM mcr.microsoft.com/appsvc/python:3.9_20201229.1

ENV PORT 5000
EXPOSE 5000

# install dependencies
COPY . .

RUN apt-get --allow-releaseinfo-change update && \
    apt-get install -y --no-install-recommends \
    tk \
    tcl \
    python3-tk

RUN pip install --no-cache-dir -r requirements.txt


# run the application
ENTRYPOINT ["python", "index.py"]