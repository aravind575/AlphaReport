# AlphaReport Microservice

AlphaReport is a microservice built to consume AlphaVantage APIs and provide functionalities for generating and managing financial reports for various companies. The microservice is developed using Django and hosted on AWS.

## Features

- Company Search: Search for a company using any search string and retrieve relevant information.
- Report Generation: Initiate the generation of a PDF report for a chosen company's balance sheet and news sentiment analysis.
- Report Status: Check the status of a generated report and download the corresponding PDF.

## Tech Stack

- Programming Language: Python
- Framework: Django
- Database: Sqlite3
- Cloud Hosting: AWS
- Testing Framework: Pytest
- Version Control: GitHub

## Getting Started

Requirements:

Python, Virtualenv/Venv, Docker

Follow these steps to set up and run the AlphaReport microservice locally:

1. Clone the repository:

   ```bash
   git clone https://github.com/aravind575/AlphaReport.git
   cd AlphaReport

2. Build the Docker image (Dockerfile):

   ```bash
   docker build -t alpha-report .

3. Run the Docker container:
   
   ```bash
   docker run -d -it -p 8000:8000 alpha-report

4. Access the microservice:
   Open your web browser and navigate to http://localhost:8000 to access the AlphaReport microservice.
   Navigate to http://localhost:8000/api/schema/swagger-ui for documentation
   
   
5. Configuration   
   
   The following environment variables are required for configuring the AlphaReport microservice. You can create a .env file in the project root directory and set these variables: 

   ```bash  
   DJANGO_SECRET_KEY: Django secret key for security purposes.
   ALPHA_API_KEY: API key for accessing the AlphaVantage APIs.
   ALPHA_SEARCH_URL: URL for the AlphaVantage company search API.
   ALPHA_SEARCH_FUNCTION: Function name for company search API.
   ALPHA_BALANCE_SHEET_URL: URL for the AlphaVantage balance sheet API.
   ALPHA_BALANCE_SHEET_FUNCTION: Function name for balance sheet API.
   ALPHA_NEWS_URL: URL for the AlphaVantage news API.
   ALPHA_NEWS_FUNCTION: Function name for news API.

6. Running Tests   
   
   Unittests for each view covering multiple cases are written using pytest module, stored in "api/test_suite".
   To run tests for the AlphaReport microservice, execute the following command:   
   
   ```bash
   pytest