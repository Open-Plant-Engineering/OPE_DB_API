# OPE_DB_API
Core backend API service for Open Plant Engineering, acting as the backbone of the platform and providing PostgreSQL-backed data access for all engineering workflows.

Conda Environment Creation for Testing:

```
conda env create -f env/environment.yml -p ope-db-api-env
conda activate ope-db-api-env
```

Remove Conda Environment:

```
conda remove -p ope-db-api-env
```

For Testing/ Using api, CLTR+Shift+P > Python: Select Interpreter > ope-db-api-env
```
uvicorn OPE_DB_API.main:app --reload

# For Closing Press CLTR+C
```