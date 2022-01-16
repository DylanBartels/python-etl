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
- [spark](spark/main.py)
- [prefect](prefect/main.py)
- dbt (soon)
- airflow (soon)

# Example

```
make spark
```
Will run a etl job through a containzerized spark cluster and put the result on minio. After the etl job is finished running on spark, the result can be seen in the minio console at http://127.0.0.1:8060/buckets/example/browse (user: dev & password: dev_pass)

# Inspiration

Inspired by [algorithms](https://github.com/keon/algorithms), and intended to become the etl scripts/flows/components equivalent.
