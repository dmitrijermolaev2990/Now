
from typing import List, Dict, Any, Optional
import psycopg2
from psycopg2.extras import RealDictCursor
from db_config import LOCAL_DB, REMOTE_DB, build_conn_string


class DBLink:
    def __init__(self, conn_string: str):
        self.conn = psycopg2.connect(conn_string)
        self.cursor = self.conn.cursor(cursor_factory=RealDictCursor)

    def execute_query(self, query: str, params: Optional[tuple] = None) -> List[Dict[str, Any]]:
        self.cursor.execute(query, params)
        data = self.cursor.fetchall()
        print(f"Результат запроса: {query} -> {data}")
        return data

    def close(self):
        self.cursor.close()
        self.conn.close()


def fetch_data(conn_string: str, query: str, params: tuple = None) -> List[Dict[str, Any]]:
    db_link = DBLink(conn_string)
    try:
        return db_link.execute_query(query, params)
    finally:
        db_link.close()


def join_data(local_conn_string: str, remote_conn_string: str, local_query: str, remote_query: str, join_key: str) -> List[Dict[str, Any]]:
    local_data = fetch_data(local_conn_string, local_query)
    remote_data = fetch_data(remote_conn_string, remote_query)

    result = []
    for local_row in local_data:
        for remote_row in remote_data:
            if str(local_row[join_key]).strip() == str(remote_row[join_key]).strip():
                combined_row = {**local_row, **remote_row}
                result.append(combined_row)

    return result


if __name__ == "__main__":
    local_conn_string = build_conn_string(LOCAL_DB)
    remote_conn_string = build_conn_string(REMOTE_DB)

    local_query = "SELECT * FROM agreement_vacancies WHERE x5_id = 103769421"
    remote_query = "SELECT id AS x5_id FROM x5_tasks WHERE id = 103769421"
    join_key = "x5_id"

    try:
        results = join_data(
            local_conn_string,
            remote_conn_string,
            local_query,
            remote_query,
            join_key
        )

        print("\nОбъединённые строки:")
        for row in results:
            print(row)

    except Exception as e:
        print(f"Произошла ошибка: {e}")
