import cx_Oracle
from modules import functions 
import inspect

# An Oracle class of operations inheriting from GeneralFunctions
class DbOracle(functions.GeneralFunctions):
    # Connection to the Oracle database    
    def db_connect(self,host_name, db_port, db_service_name, db_user, db_password):
        try:
            dsn_tns = cx_Oracle.makedsn(host_name, db_port, db_service_name)
            conn=cx_Oracle.connect(user=db_user, password=db_password, dsn=dsn_tns)
            c = conn.cursor()
        except:
            c = ""
            self.print_error("Failed to connect to the database in db_connect. Base:", db_service_name)
        return c
    
    # Sending a query to the database
    def get_query_result(self, con ,query, number_of_columns):
        try:
            con.execute('alter session set NLS_COMP=LINGUISTIC')
            con.execute('alter session set NLS_SORT=BINARY_CI')
            con.execute(query)
            for row in con:
                return row[:number_of_columns]         
        except:
            self.print_error("Select failed in get_query_result: ", query)
            return '0'
            pass

    def get_count_connection_per_hour_from_db(self, con):
        try:
            con.execute(""" 
                            SELECT
                            to_char(TRUNC(s.begin_interval_time,'HH24'),'YYYY-MM-DD HH24:MI:SS') snap_begin,
                            sum(r.current_utilization) sessions
                            FROM
                            dba_hist_resource_limit r,
                            dba_hist_snapshot s
                            WHERE ( TRUNC(s.begin_interval_time,'HH24'),s.snap_id ) IN
                            (
                            SELECT TRUNC(sn.begin_interval_time,'HH24'),MAX(rl.snap_id)
                            FROM dba_hist_resource_limit rl,dba_hist_snapshot sn
                            WHERE TRUNC(sn.begin_interval_time) >= TRUNC(sysdate-7)
                            AND rl.snap_id = sn.snap_id
                            AND rl.resource_name = 'sessions'
                            AND rl.instance_number = sn.instance_number
                            AND ( TRUNC(sn.begin_interval_time,'HH24'),rl.CURRENT_UTILIZATION ) IN
                            (
                            SELECT TRUNC(s.begin_interval_time,'HH24'),MAX(r.CURRENT_UTILIZATION) "no_of_sess"
                            FROM dba_hist_resource_limit r,dba_hist_snapshot s
                            WHERE r.snap_id = s.snap_id
                            AND TRUNC(s.begin_interval_time) >= TRUNC(sysdate-7)
                            AND r.instance_number=s.instance_number
                            AND r.resource_name = 'sessions'
                            GROUP BY TRUNC(s.begin_interval_time,'HH24')
                            )
                            GROUP BY TRUNC(sn.begin_interval_time,'HH24'),CURRENT_UTILIZATION
                            )
                            AND r.snap_id = s.snap_id
                            AND r.instance_number = s.instance_number
                            AND r.resource_name = 'sessions'
                            GROUP BY
                            to_char(TRUNC(s.begin_interval_time,'HH24'),'YYYY-MM-DD HH24:MI:SS')
                            ORDER BY snap_begin 
                        """)
            
            records = con.fetchall()
            return records
            
        except:
            self.print_error("Select failed in get_count_connection_per_hour_from_db")
    
     
