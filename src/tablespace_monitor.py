from lib.common import *
import pandas as pd
from datetime import datetime

def monitor_tablespace():
    logger = setup_logging("tablespace")
    logger.info("Starting Tablespace Monitoring")

    # Real SQL Query for Tablespace Usage
    sql = """
    SELECT tablespace_name,
           ROUND(used_space/total_space*100, 2) AS used_pct,
           ROUND(total_space, 2) AS total_mb,
           ROUND(free_space, 2) AS free_mb
    FROM (
        SELECT tablespace_name,
               SUM(bytes)/1024/1024 AS total_space,
               SUM(used_bytes)/1024/1024 AS used_space,
               SUM(free_bytes)/1024/1024 AS free_space
        FROM (
            SELECT tablespace_name, bytes, 0 AS used_bytes, bytes AS free_bytes 
            FROM dba_free_space
            UNION ALL
            SELECT tablespace_name, bytes, bytes, 0 
            FROM dba_data_files
        )
        GROUP BY tablespace_name
    )
    WHERE used_space/total_space*100 > 75
    ORDER BY used_pct DESC
    """

    conn = get_connection("ORCL")   # Update SID as needed
    if conn:
        df = pd.read_sql(sql, conn)
        conn.close()

        if not df.empty:
            html = f"<h2>⚠️ High Tablespace Usage Alert - {datetime.now():%d-%b-%Y}</h2>" + df.to_html()
            send_email("CRITICAL: Tablespace Usage Alert", html)
            logger.warning(f"High usage tablespaces found: {len(df)}")
        else:
            logger.info("All tablespaces are healthy")

if __name__ == "__main__":
    monitor_tablespace()
