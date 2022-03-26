FROM python:3.9

RUN mkdir /app
RUN apt-get update
WORKDIR /app
RUN pip install pytest==7.0.0
RUN pip install xmltodict==0.12.0
RUN pip install Flask==2.0.3
RUN pip install flask
ADD app.py /app
ADD pytest_app.py /app
ADD ISS.OEM_J2K_EPH.xml /app
ADD XMLsightingData_citiesINT02.xml /app

ENTRYPOINT ["python"]
CMD ["app.py"]