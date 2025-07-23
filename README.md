# VLR-Rating-Predictor

A machine learning project that predicts player ratings in Valorant using data scraped from [VLR.gg](https://www.vlr.gg/).

## Overview

This project uses historical Valorant match data to train a machine learning model that predicts player ratings based on in-game performance statistics.

> **Note:**  
> The `scraper.py` script is **outdated as of April 2025** due to changes in the VLR.gg website structure.  
> All necessary data scraping and cleaning has already been completed.  
> Simply run the model and prediction scripts using the provided CSV files in the root directory.

## Features

- Pre-cleaned CSV data ready for training and testing
- Machine learning model for rating prediction
- Simple training and prediction scripts within model.py
- Lightweight and easy to run

## Getting Started

### Prerequisites

- Python 3.8+
- Install dependencies:

```bash
pip install -r requirements.txt
```

## Usage
Simply running model.py will generate the csv file with all predictions
```bash
python model.py
```
