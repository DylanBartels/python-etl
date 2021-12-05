Python ETL 
=========================================

Minimal examples of ETL scripts/flows/components in Python. All implementations use the same input data and data transformation. Starting point and lookup source for anything date-engineer related.

# Requirments

- docker
- make

# Usage

```
make [implementation]
```

## List of Implementations

- [object-storage](object-storage/main.py)
- [postgresql](postgresql/main.py)
- [spark](spark/main.py)
- dbt (soon)
- airflow (soon)
- prefect (soon)
- BigQuery (soon)

# Inspiration

Inspired by [algorithms](https://github.com/keon/algorithms), and intended to become the etl scripts/flows/components equivalent.
