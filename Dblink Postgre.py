from typing import List, Dict, Any, Optional
import psycopg2
from psycopg2.extras import RealDictCursor


class DBLink:
    def __init__(self, conn_string: str):
        """Инициализация подключения к базе данных."""
        self.conn = psycopg2.connect(conn_string)
        self.cursor = self.conn.cursor(cursor_factory=RealDictCursor)

    def execute_query(self, query: str, params: Optional[tuple] = None) -> List[Dict[str, Any]]:
        """Выполнение SQL-запроса и возврат результата в виде списка словарей."""
        self.cursor.execute(query, params)
        data = self.cursor.fetchall()
        print(f"Результат запроса: {query} -> {data}")
        return data

    def close(self):
        """Закрытие курсора и соединения."""
        self.cursor.close()
        self.conn.close()


def fetch_data(conn_string: str, query: str, params: tuple = None) -> List[Dict[str, Any]]:
    """Получает данные из базы."""
    db_link = DBLink(conn_string)
    try:
        return db_link.execute_query(query, params)
    finally:
        db_link.close()


def join_data(local_conn_string: str, remote_conn_string: str, local_query: str, remote_query: str, join_key: str) -> List[Dict[str, Any]]:
    """
    Выполняет JOIN между данными из локальной и удаленной баз в памяти.
    """
    local_data = fetch_data(local_conn_string, local_query)
    remote_data = fetch_data(remote_conn_string, remote_query)

    result = []
    for local_row in local_data:
        for remote_row in remote_data:
            if str(local_row[join_key]).strip() == str(remote_row[join_key]).strip():
                combined_row = {**local_row, **remote_row}
                result.append(combined_row)

    return result


# Пример использования
if __name__ == "__main__":
    local_conn_string = "dbname=postgres user=postgres password=dmitrij host=localhost port=5432"
    remote_conn_string = "dbname=prod_x5_adapter user=d.ermolaev_1 password=mwWXln0I5-dCKVeKYSfQ host=prod-svc-db1.msk.ventrago.dev port=5432"

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
