# Cyber Attack Predictor

A project for analyzing and predicting web application attacks using machine learning models and reference datasets. We have approximately $1.000.000$ access logs with the goal of predicting whether or not an attack has occurred using the analyzed ML models.

## Project Structure

- `data/`: Directory for datasets.
  - `data/target`: Access Log of Real Web
  - `data/test_dataset`: Datasets for performing comparisons between models
- `labs/`: Jupyter notebooks for access log and CSIC 2010 analysis. (FIX)
- `notebooks/`: Notebooks for WAF analysis and data processing. (FIX)
- `src/`: Source code, including API and preprocessing modules.
- `sota/`: Contains an app, requirements, and sample data for comparative analysis of State-of-the-Art.

## Installation

1. Clone the repository.
2. Create a virtual environment: `python -m venv ".env"`
3. Activate it: `.env\Scripts\activate` (Windows) or `source .env/bin/activate` (Linux/Mac).
4. Install dependencies: `pip install -r requirements.txt` (and `pip install -r sota/requirements.txt` if needed).

## Usage

- Run notebooks in `labs/` or `notebooks/` for analysis (e.g., using Jupyter).
- Use `sota/app.py` for State-of-the-Art comparisons.
- Process data with scripts in `src/preprocessing/`.

## Reference Datasets

Datasets for performing comparisons between models:

- [HttpParamsDataset: Repository](https://github.com/Morzeux/HttpParamsDataset)
- [CSIC 2010 Web Application Attacks](https://www.kaggle.com/datasets/ispangler/csic-2010-web-application-attacks/data)
- [Web Application Attack Payload Dataset](https://www.kaggle.com/datasets/mreowie/web-application-attack-payload-dataset/data)
- [Web Server Access Logs: A sample of web server logs file](https://www.kaggle.com/datasets/eliasdabbas/web-server-access-logs/data)
