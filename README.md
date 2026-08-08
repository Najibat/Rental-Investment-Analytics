# Rental-Investment-Analytics
AI NOW Bootcamp Project on Data Engineering Pipelines


# Urban Nest: Short-Term Rental Analytics & Acquisition Pipeline

An end-to-end data engineering and analytics solution designed to evaluate short-term rental investment opportunities in Albany, New York for **Urban Nest**. 

This project ingests multi-month market snapshot data directly from an AWS S3 Data Lake, cleans and standardises the raw records, and executes a structured business intelligence analysis using Python and Pandas.



## 📌 Project Overview

Urban Nest is expanding its portfolio into the Albany short-term rental market. To minimise market entry risk and maximize yield, this project addresses 8 core strategic business questions:

1. **Top Neighbourhood Revenue:** Identifying high-yield locations based on estimated monthly revenue.
2. **Room Type Dynamics:** Quantifying the pricing and occupancy trade-offs between entire homes, private rooms, and shared spaces.
3. **Market Oversaturation:** Pinpointing neighbourhoods displaying high listing density alongside depressed occupancy.
4. **Property Performance:** Determining optimal property formats for acquisition.
5. **Supply vs. Demand:** Mapping listing density against guest demand indicators (review velocity).
6. **Target Acquisitions:** Recommending priority neighbourhoods for initial property purchases.
7. **Operational Drivers:** Evaluating the performance impact of host portfolio scale and minimum stay requirements.
8. **Pricing Benchmarks:** Establishing dynamic pricing matrices to guide initial listing rates.

---

## 🛠 Tech Stack & Tools

* **Language:** Python 3.12+
* **Cloud Infrastructure:** AWS S3 (Data Lake Ingestion via `boto3`)
* **Data Processing & Analytics:** Pandas, NumPy
* **Environment & Workflow:** Jupyter Notebook (`analysis.ipynb`), VS Code, `python-dotenv`

---

## 📁 Repository Structure

```text
Rental-Investment-Analytics/
│
├── data/                       # Local storage for ingested S3 CSV files
├── .gitignore                  # Excludes .env, virtual environments, and logs
├── config.py                   # AWS S3 client setup & logging configuration
├── ingest.py                   # S3 automated ingestion script
├── analysis.ipynb              # Data cleaning & business analysis notebook
├── requirements.txt            # Project dependencies
└── README.md                   # Project documentation

```

---

## ⚙️ Data Pipeline & Ingestion Architecture

### 1. S3 Data Ingestion (`config.py` & `ingest.py`)

* Securely connects to AWS S3 using environment-stored IAM credentials.
* Fetches multi-month snapshot listings CSV files (`january`, `february`, `june`).
* Enforces structural schema checks, tags source provenance metadata, and outputs standardized CSVs into the local `data/` directory.

### 2. Cleaning & Preprocessing (`analysis.ipynb`)

* **Column Normalisation:** Converts headers to snake_case and removes non-alphanumeric noise.
* **Type Casting:** Strips currency formatting (`$`, `,`) and casts numeric metrics (`price`, `availability_365`, `reviews_per_month`).
* **Deduplication:** Filters out redundant listing records across snapshot windows.
* **Feature Engineering:** Calculates key metrics including `est_occupancy_rate` and `est_monthly_revenue`.

---

## 🚀 Getting Started

### Prerequisites

* Python 3.10+ installed
* An active AWS IAM user with read access to the S3 bucket

### Setup Instructions

1. **Clone the Repository:**
```bash
git clone [https://github.com/Najibat/Rental-Investment-Analytics.git](https://github.com/Najibat/Rental-Investment-Analytics.git)
cd Rental-Investment-Analytics

```


2. **Set Up Virtual Environment & Dependencies:**
```bash
python -m venv myvenv
# On Windows:
myvenv\Scripts\activate
# On Mac/Linux:
source myvenv/bin/activate

pip install -r requirements.txt

```


3. **Configure Environment Variables:**
Create a `.env` file in the root directory:
```env
AWS_ACCESS_ID=YOUR_AWS_ACCESS_KEY
AWS_SECRET_ACCESS_KEY=YOUR_AWS_SECRET_KEY
AWS_DEFAULT_REGION=eu-central-1

```


4. **Run Ingestion Pipeline:**
```bash
python ingest.py

```


5. **Run Analysis:**
Open `analysis.ipynb` in VS Code or Jupyter Notebook and execute all cells sequentially.

```

---

### How to Push This to GitHub:

1. In VS Code, click the **New File** icon in the project root, name it `README.md`, and paste the text above.
2. Run these commands in your terminal:
   ```bash
   git add README.md
   git commit -m "Add comprehensive README documentation"
   git push origin main

```