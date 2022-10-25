from typing import List

from fastapi_healthcheck.domain import HealthCheckInterface
from fastapi_healthcheck.enum import HealthCheckStatusEnum
from fastapi_healthcheck.service import HealthCheckBase
from fastapi_sqlalchemy import db
from sqlalchemy import text, exc


class HealthCheckSQLAlchemy(HealthCheckBase, HealthCheckInterface):
    _connectionUri: str
    _tags: List[str]
    _message: str

    def __init__(self, alias: str, tags: List[str]) -> None:
        self._alias = alias
        self._tags = tags

    def __checkHealth__(self) -> HealthCheckStatusEnum:
        res: HealthCheckStatusEnum = HealthCheckStatusEnum.UNHEALTHY
        with db():
            try:
                db.session.query("ping").from_statement(text("SELECT 1 as ping")).one()
                res = HealthCheckStatusEnum.HEALTHY
            except exc.DBAPIError:
                pass
        return res
