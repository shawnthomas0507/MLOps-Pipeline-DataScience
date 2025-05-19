# MLOps Pipeline for Data Science

## Overview

The MLOps-Pipeline-DataScience project is designed to streamline the process of deploying machine learning models into production. This repository contains a comprehensive pipeline that integrates various stages of the machine learning lifecycle, including data validation, model training, and deployment.

## Features

- **Continuous Integration and Delivery (CI/CD)**: Automated workflows for testing and deploying models.
- **Data Validation**: Ensures the integrity and quality of data before training.
- **Model Training**: Implements a training pipeline for building machine learning models.
- **Deployment**: Deploys models to a containerized environment using Docker and AWS ECR.


## Getting Started

### Prerequisites

- Python 3.x
- Docker
- AWS CLI configured with your credentials (This project uses AWS ECR (for docker image storage) and EC2 (for compute) )
 
### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/MLOps-Pipeline-DataScience.git
   cd MLOps-Pipeline-DataScience
   ```

2. Install the required Python packages:
   ```bash
   pip install -r requirements.txt
   ```

### Running the Application

1. Start the application:
   ```bash
   python app.py
   ```

2. Access the application at `http://localhost:8080/train` to trigger the training pipeline.

### CI/CD Workflows

The project uses GitHub Actions for CI/CD. The workflows defined in `.github/workflows/main.yaml` will automatically run on pushes to the `main` branch, ensuring that the code is tested and deployed seamlessly.

### Data Validation

The data validation process generates drift reports stored in the `Artifacts/` directory. These reports help monitor the performance of the model over time and ensure that it remains effective.
