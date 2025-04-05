# Perfume Recommender System

This project is an assignment for the Intermediate Database and Datawarehouse course, as well as for the Unsupervised Learning course. The goal is to build a recommendation system that suggests perfumes based on unsupervised learning techniques while leveraging data warehousing concepts.

## Project Overview

- **Assignment Context:**  
  This project is designed to demonstrate your skills in designing and implementing ETL processes, managing databases (OLTP/OLAP), and applying unsupervised learning techniques for recommendation.

- **Key Components:**
  - **ETL Processes:**  
    The [`etl/`](etl/) folder contains scripts and configurations for extracting, transforming, and loading data.
  - **Data Warehousing:**  
    The [postgres_data](postgres_data/) directory holds schemas and data dedicated to both OLTP and Data Warehouse (DWH) environments.
  - **Unsupervised Learning:**  
    The recommendation engine utilizes unsupervised learning algorithms to generate perfume suggestions.
  - **Airflow DAGs:**  
    The [`dags/`](dags/) folder contains Python DAGs (e.g., [`test_dag.py`](dags/test_dag.py)) for scheduling ETL workflows.
  - **Visualization & Dashboards:**  
    Tools such as Metabase and Superset are integrated (see folders [`metabase_data/`](metabase_data/) and [`superset_data/`](superset_data/)) for data visualization and dashboarding.
  - **Docker Compose:**  
    The [docker-compose.yaml](docker-compose.yaml) file is set up to orchestrate the various services.

## Prerequisites

- **Docker & Docker Compose:**  
  Ensure you have Docker installed to run the services.
- **Python 3.12+:**  
  Required for running Airflow DAGs and ETL scripts.
- **Database Tools:**  
  Tools such as pgAdmin may be used to manage PostgreSQL databases.

## Setup Instructions

1. **Clone the Repository:**
   ```sh
   git clone <repository-url>
   cd perfume-recommender-system
   ```

2. **Run Docker Compose:**
   ```sh
   docker-compose up -d
   ```
   This will start all the necessary containers for PostgreSQL, Airflow, Superset, Metabase, and Redis.

3. **Configure Airflow:**
   - Review and update the DAG files in the [`dags/`](dags/) folder if needed.
   - Access the Airflow UI (usually available at http://localhost:8080).

4. **ETL & Data Loading:**
   - Execute ETL scripts located in the [`etl/`](etl/) folder to process and load data into the DWH.

5. **Testing the Recommendation System:**
   - Run the recommendation engine script (ensure that the relevant unsupervised learning libraries are installed).
   - Use sample data to generate perfume recommendations.

## Project Structure

```
├── .gitignore
├── docker-compose.yaml
├── README.md
├── airflow_logs/
├── dags/
│   ├── test_dag.py
│   └── __pycache__/
├── etl/
├── metabase_data/
├── pgadmin_data/
│   ├── pgadmin4.db
│   ├── azurecredentialcache/
│   └── sessions/
├── postgres_data/
│   ├── dwh/
│   ├── oltp/
│   └── oltp_data/
├── vector/
├── redis_data/
│   └── dump.rdb
└── superset_data/
    └── superset.db
```

## License

This project is provided for academic purposes and does not include a production license.