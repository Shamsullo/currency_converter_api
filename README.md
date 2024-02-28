# Test task: Development of an API for currency conversion
[![codecov](https://codecov.io/gh/Shamsullo/currency_converter_api/main/graph/badge.svg)](https://codecov.io/gh/Shamsullo/currency_converter_api)
[![API CI-test](https://github.com/Shamsullo/currency_converter_api/actions/workflows/ci.yml/badge.svg)](https://github.com/Shamsullo/currency_converter_api/actions/workflows/ci.yml)

The documentation is structured to guide users through the installation process, understand the API endpoints, and perform currency conversions.

**Project Overview**

This project provides an API for currency conversion, leveraging FastAPI for the web framework, SQLAlchemy for the ORM, and Docker for containerization. Basically, It can fetch the current exchange rates, convert between different currencies, and view the last update of currency rates in the database.

**Installation and Running the Service**

1\. Clone the project from the GitHub repository

2\. create a .env where you need to fill environment variables. The example and the required fields are given in the .env.example

3\. run the project using docker: 

 ```bash
  docker-compose -f docker-compose.yml up --build -d
 ```
 the project will be available at http://localhost:8080
 NOTES: all the migrations will be applied automatically on the startup. But, to have the currency table filled one needs to call /v1/rates/update

**Documentation**

More detailed API documentation can be found here, of course after starting the project: 

 - http://localhost:8080/api/docs (Swagger)

 - http://localhost:8080/api/re-docs (Redocs)

For testing purposes, I have deployed the service to the temporary server and it can be found here: http://3.77.154.109:8080/api/docs#/

**Continuous Integration (CI)**

The project includes a CI script setup to:

 - Check the syntax using **flake8**

 - Run automated tests

 - Generate a code coverage report

 **Tests**
The API is covered with some basic test cases as an example using pytest. This command can run the test:
```bash
  docker-compose exec currency-converter-api pytest -v
```

***Link to test technical requirements***
 - https://docs.google.com/document/d/1lmiYMkJ2IIPz-V9Koc9pYQ-56x9OMU5Xwc32RH9wGn0/edit (Test task: Development of an API for currency conversion
 at Google Sheet)
