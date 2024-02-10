# Blended Bytes

Blended Bytes is a news summarization and delivery system that combines the power of Airflow, llama-indexer, and Golang to provide users with a personalized daily news digest.

## Overview

Blended Bytes is designed to fetch top news articles from the last 24 hours, process them using a pretrained Language Model (LLM) through llama-indexer, and generate concise summaries using prompt engineering. The summarized content is then delivered daily to subscribers through a Golang-based backend email service. The project also includes a user-friendly frontend interface for easy signup and subscription management.

## Features

- **Airflow DAG Integration**: Retrieve and store top news articles in a PostgreSQL database using an Airflow DAG.

- **LLM Fine-Tuning**: Employ pretrained Language Models through llama-indexer to fine-tune indexed news articles.

- **Prompt Engineering**: Utilize prompt engineering techniques to instruct the LLM in generating summaries of the past day's events.

- **Golang Backend**: Build a robust backend in Golang to power the email service for delivering daily news summaries.

- **Frontend Interface**: Develop a user-friendly frontend allowing users to easily sign up, manage subscriptions, and receive daily news emails.

## Getting Started

### Prerequisites

- PostgreSQL
- Airflow
- llama-indexer
- Golang

### Installation

1. Clone the repository: `git clone https://github.com/yourusername/blended-bytes.git`
2. Install dependencies: `pip install -r requirements.txt`
3. Configure Airflow, llama-indexer, and set up the Golang backend.
4. Run the Airflow DAG for data retrieval.

## Usage

1. Run the Airflow DAG to fetch and store news articles.
2. Trigger the llama-indexer for fine-tuning.
3. Execute the Golang backend to initiate the email service.
4. Access the frontend interface to sign up and manage subscriptions.
