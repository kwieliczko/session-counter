import cx_Oracle

from modules import functions


class DbOracle(functions.GeneralFunctions):
    def db_connect(self, host_name, db_port, db_service_name, db_user, db_password):
        dsn = cx_Oracle.makedsn(host_name, int(db_port), service_name=db_service_name)
        return cx_Oracle.connect(user=db_user, password=db_password, dsn=dsn)

    def get_query_result(self, connection, query, number_of_columns, parameters=None):
        with connection.cursor() as cursor:
            cursor.execute(query, parameters or {})
            row = cursor.fetchone()
            return row[:number_of_columns] if row is not None else None

    def get_connection_settings(self, connection, db_name):
        query = """
            SELECT id, host_name, db_port, db_service_name, db_user, db_password
            FROM connecting_string
            WHERE UPPER(db_service_name) = UPPER(:db_name)
        """
        with connection.cursor() as cursor:
            cursor.execute(query, {"db_name": db_name})
            row = cursor.fetchone()
            if row is not None and cursor.fetchone() is not None:
                raise ValueError("Multiple databases have the same service name: " + db_name)
            return row

    def get_count_connection_per_hour_from_db(self, connection):
        query = """
            SELECT TO_CHAR(TRUNC(s.begin_interval_time, 'HH24'), 'YYYY-MM-DD HH24:MI:SS') snap_begin,
                   SUM(r.current_utilization) sessions
            FROM dba_hist_resource_limit r, dba_hist_snapshot s
            WHERE (TRUNC(s.begin_interval_time, 'HH24'), s.snap_id) IN (
                SELECT TRUNC(sn.begin_interval_time, 'HH24'), MAX(rl.snap_id)
                FROM dba_hist_resource_limit rl, dba_hist_snapshot sn
                WHERE TRUNC(sn.begin_interval_time) >= TRUNC(SYSDATE - :days_back)
                  AND rl.snap_id = sn.snap_id
                  AND rl.resource_name = :resource_name
                  AND rl.instance_number = sn.instance_number
                  AND (TRUNC(sn.begin_interval_time, 'HH24'), rl.current_utilization) IN (
                      SELECT TRUNC(s.begin_interval_time, 'HH24'), MAX(r.current_utilization)
                      FROM dba_hist_resource_limit r, dba_hist_snapshot s
                      WHERE r.snap_id = s.snap_id
                        AND TRUNC(s.begin_interval_time) >= TRUNC(SYSDATE - :days_back)
                        AND r.instance_number = s.instance_number
                        AND r.resource_name = :resource_name
                      GROUP BY TRUNC(s.begin_interval_time, 'HH24')
                  )
                GROUP BY TRUNC(sn.begin_interval_time, 'HH24'), current_utilization
            )
              AND r.snap_id = s.snap_id
              AND r.instance_number = s.instance_number
              AND r.resource_name = :resource_name
            GROUP BY TO_CHAR(TRUNC(s.begin_interval_time, 'HH24'), 'YYYY-MM-DD HH24:MI:SS')
            ORDER BY snap_begin
        """
        with connection.cursor() as cursor:
            cursor.execute(query, {"days_back": 7, "resource_name": "sessions"})
            return cursor.fetchall()
