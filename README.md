# Toronto Crime Indicators Analytics Tool

A Python-based analytics tool for exploring and visualizing Toronto crime indicators data.

## Project Overview

This project analyzes the Toronto Crime Indicators dataset to generate meaningful insights about crime patterns, trends, neighbourhood activity, offence distributions, police division activity, premises types, and geographic hotspots.

The solution is developed using Agile Software Development practices across two sprints.

## Main Features

- Load Toronto Crime Indicators CSV dataset
- Clean invalid and incomplete records
- Analyze crimes by hour of day
- Analyze crimes by neighbourhood
- Analyze offence type distributions
- Analyze crime trends over time
- Analyze police division activity
- Analyze premises type distribution
- Identify geographic crime hotspots
- Display insights in an interactive Streamlit dashboard
- Include automated tests using pytest

## Technologies

- Python
- Pandas
- NumPy
- Matplotlib
- Plotly
- Streamlit
- Pytest
- GitHub
- Taiga

## Initial Project Structure

toronto-crime-indicators-analytics-tool/

├── src/
├── tests/
├── app.py
├── requirements.txt
├── README.md
└── .gitignore

## How to Run

Install dependencies:

pip install -r requirements.txt

Run the Streamlit dashboard:

streamlit run app.py

Run tests:

pytest

## Agile Workflow

The project follows an Agile workflow using:

Product Backlog in Taiga
Two development sprints
Feature branches
Pull requests
Code reviews
TDD for selected user stories
Refactoring tasks
Sprint metrics such as burndown and velocity

## Team Collaboration

Each team member contributes through feature branches, commits, pull requests, and code reviews. Commits and pull requests are tagged with the corresponding Taiga story IDs.