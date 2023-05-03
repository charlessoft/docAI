# -*- coding: utf-8 -*-
import datetime
import logging
import json

from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore

try:
    from sqlalchemy import (
        create_engine,
        Table,
        Column,
        MetaData,
        Unicode,
        select,
        DateTime,
    )

except ImportError:  # pragma: nocover
    raise ImportError("SQLAlchemyJobStore requires SQLAlchemy installed")

logger = logging.getLogger()


class ResultJobStore(SQLAlchemyJobStore):
    def __init__(
        self,
        url=None,
        engine=None,
        tablename="jobs_result",
        metadata=None,
        tableschema=None,
        engine_options=None,
    ):
        from apscheduler.util import maybe_ref

        metadata = maybe_ref(metadata) or MetaData()

        if engine:
            self.engine = maybe_ref(engine)
        elif url:
            self.engine = create_engine(url, **(engine_options or {}))
        else:
            raise ValueError('Need either "engine" or "url" defined')

        # 191 = max key length in MySQL for InnoDB/utf8mb4 tables,
        # 25 = precision that translates to an 8-byte float
        self.jobs_t = Table(
            tablename,
            metadata,
            # id = db.Column(db.UUID, primary_key=True, default=uuid.uuid4, nullable=False)
            Column("job_id", Unicode(191, _warn_on_bytestring=False), primary_key=True),
            Column("job_status", Unicode(191), nullable=False),
            Column(
                "create_time", DateTime(), default=datetime.datetime.now, nullable=False
            ),
            Column(
                "update_time",
                DateTime(),
                onupdate=datetime.datetime.now,
                default=datetime.datetime.now,
                nullable=False,
            ),
            Column("job_result", Unicode(512), nullable=False, default=""),
            schema=tableschema,
        )
        self.jobs_t.create(self.engine, True)

    def lookup_job(self, job_id):
        selectable = select(
            [
                self.jobs_t.c.job_id,
                self.jobs_t.c.create_time,
                self.jobs_t.c.update_time,
                self.jobs_t.c.job_status,
                self.jobs_t.c.job_result,
            ]
        ).where(self.jobs_t.c.job_id == job_id)
        job_result = self.engine.execute(selectable).first()
        return job_result if job_result else None

    def update_job_status(self, job_id, result):
        lookup = self.lookup_job(job_id)
        if lookup:
            update = (
                self.jobs_t.update()
                .values(**{"job_status": result["job_status"]})
                .where(self.jobs_t.c.job_id == job_id)
            )
            ret = self.engine.execute(update)
            return ret.rowcount
        else:
            self.add_job_status(result)
            return 1

    def add_job_status(self, job_id, result):
        insert = self.jobs_t.insert().values(
            **{"job_id": job_id, "job_status": result["job_status"]}
        )
        try:
            self.engine.execute(insert)
        # except IntegrityError:
        #     raise ConflictingIdError(result['job_id'])
        except Exception as e:
            logger.error(e)
            return False

    def update_job_result(self, job_id, result):

        lookup = self.lookup_job(job_id)
        if lookup:
            update = (
                self.jobs_t.update()
                .values(**{"job_result": json.dumps(result["job_result"])})
                .where(self.jobs_t.c.job_id == job_id)
            )
            ret = self.engine.execute(update)
            return ret.rowcount
        else:
            self.add_job_result(result)
            return 1
        # if ret.rowcount == 0:
        #     raise JobLookupError(id)

    def add_job_result(self, job_id, result):
        insert = self.jobs_t.insert().values(
            **{"job_id": job_id, "job_result": json.dumps(result["job_result"])}
        )
        try:
            self.engine.execute(insert)
        # except IntegrityError:
        #     raise ConflictingIdError(result['job_id'])
        except Exception as e:
            print(e)
