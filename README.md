# PortfolioMonitor

PortfolioMonitor is a Python-based application designed to help you track and manage your investment portfolio. This project was built as a capstone project for CSCA 5028.

## Features
- Ability to add holdings to your portfolio
- Some advanced metrics for your portfolio like vitality and sharpe ratio
- Price history table for each holding to dive into how they've changed over time

## Getting Started

### Prerequisites
- Docker installed on your machine

### Building the Docker Image
To build the Docker image for PortfolioMonitor, run the following command in the project directory:

```sh
docker build -t portfoliomonitor .
```

### Running the Docker Container
Once the image is built, you can run the container using:

```sh
docker run -p 5001:5001 portfoliomonitor
```

This will start the PortfolioMonitor application, and it will be accessible at `http://localhost:5001`.


## Grading
If you're having issues getting it running, feel free to reach out to me (Patrick.Holmgren@colorado.edu) to see if we can't figure it out together!