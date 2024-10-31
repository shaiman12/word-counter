# URL Word Counter
Done by Shai Aarons

A Flask-based web application that counts and displays words from any given website URL.

## Features

- Submit any website URL to count its words
- Asynchronous job processing with Redis Queue
- MongoDB for job storage and results
- Docker containerization for easy deployment
- Handles dynamic JavaScript-rendered content using Selenium and Beautiful Soup
- Displays word count results and individual words
- Error handling and job status tracking

## Prerequisites

- Docker and Docker Compose

## Installation & Setup

Build and Start your docker containers:
```
docker-compose -f docker/docker-compose.yml up --build

```
Access the application at `http://localhost:5001`

## Usage
1. Enter a website URL in the input field
2. Click "Count Words" to submit the job
3. Monitor the job status in the results table below the search bar - a refresh of the page is necessary
4. Once completed, click "View Words" to see the individual words found

## Areas for improvement
- Using a more robust async job package like Celery
- Polling on the index page so that the user does not have to refresh the page 
- 