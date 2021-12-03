from fastapi_healthcheck.service import HealthCheckBase
from fastapi_healthcheck.enum import HealthCheckStatusEnum
from fastapi_healthcheck.domain import HealthCheckInterface
from typing import List
from fastapi_sqlalchemy import db

class HealthCheckSQLAlchemy(HealthCheckBase, HealthCheckInterface):
    _connectionUri: str
    _table: object
    _tags: List[str]
    _message: str

    def __init__(self, table: object, alias: str, tags: List[str]) -> None:
        self._alias = alias
        self._table = table
        self._tags = tags

    def __checkHealth__(self) -> HealthCheckStatusEnum:
        res: HealthCheckStatusEnum = HealthCheckStatusEnum.UNHEALTHY
        with db():
            try:
                r = -1
                r = db.session.query(self._table).count()
                if r != -1:
                    res = HealthCheckStatusEnum.HEALTHY
            except Exception as e:
                pass
        return res  