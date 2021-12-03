# fastapi-healthcheck-sqlalchemy

A module built on top of fastapi_healthcheck to check the status of your SQLAlchemy connection.  This requires a Table given to the health check so it can run a count of rows against it.  As long as it returns a value, the connection is alive.

## Install

`pip install fastapi-healthcheck-sqlalchemy` or `poetry add fastapi-healthcheck-sqlalchemy`

## How to use

This module just exposes the service layer that will be used to parse your middleware connection to your database.  

```python
from fastapi import FastAPI
from fastapi_sqlalchemy import DBSessionMiddleware
from fastapi_healthcheck import HealthCheckFactory, healthCheckRoute
from fastapi_healthcheck_sqlalchemy import HealthCheckSQLAlchemy


app = FastAPI()

# Bring SQLAlchemy online first.
app.add_middleware(DBSessionMiddleware, db_url=cs.value)

_healthChecks = HealthCheckFactory()
_healthChecks.add(
    HealthCheckSQLAlchemy(
        # The name of the object for your reference
        alias='postgres db',  

        # The Table that we will run a count method against.
        table=SmtpContactsSqlModel, 

        tags=('postgres', 'db', 'sql01')
    )
)

app.add_api_route('/health', endpoint=healthCheckRoute(factory=_healthChecks))
```
