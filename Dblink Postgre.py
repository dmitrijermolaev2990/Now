import psycopg2
from psycopg2.extras import RealDictCursor
from typing import List, Dict, Any, Optional


class DBLink:
    def __init__(self, conn_string: str):
        """
        Инициализация подключения к удаленной базе данных.

        Args:
            conn_string (str): Строка подключения к базе данных в формате
                              'dbname=prod_x5_adapter user=d.ermolaev_1 password=mwWXln0I5-dCKVeKYSf host=prod-svc-db1.msk.ventrago.dev port=5432'
        """
        self.conn_string = conn_string
        self.conn = None
        self.cursor = None

    def connect(self) -> None:
        """Устанавливает соединение с базой данных."""
        try:
            self.conn = psycopg2.connect(self.conn_string)
            self.cursor = self.conn.cursor(cursor_factory=RealDictCursor)
        except psycopg2.Error as e:
            raise Exception(f"Ошибка подключения к базе данных: {e}")

    def execute_query(self, query: str, params: tuple = None) -> List[Dict[str, Any]]:
        """
        Выполняет SQL-запрос на удаленной базе данных и возвращает результаты.

        Args:
            query (str): SQL-запрос для выполнения.
            params (tuple, optional): Параметры для безопасного выполнения запроса.

        Returns:
            List[Dict[str, Any]]: Список словарей с результатами запроса.
        """
        if not self.conn or self.conn.closed:
            self.connect()

        try:
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)
            # Проверяем, возвращает ли запрос данные
            if self.cursor.description:
                return self.cursor.fetchall()
            return []
        except psycopg2.Error as e:
            raise Exception(f"Ошибка выполнения запроса: {e}")

    def close(self) -> None:
        """Закрывает соединение и курсор."""
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()


def dblink_query(conn_string: str, query: str, params: tuple = None) -> List[Dict[str, Any]]:
    """
    Упрощенный интерфейс для выполнения запроса, аналогичный dblink.

    Args:
        conn_string (str): Строка подключения к удаленной базе данных.
        query (str): SQL-запрос для выполнения.
        params (tuple, optional): Параметры для запроса.

    Returns:
        List[Dict[str, Any]]: Результаты запроса в виде списка словарей.
    """
    db_link = DBLink(conn_string)
    try:
        results = db_link.execute_query(query, params)
        return results
    finally:
        db_link.close()


# Пример использования
if __name__ == "__main__":
    # Пример строки подключения
    remote_conn_string = "dbname=postgres user=postgres password=dmitrij host=localhost port=5432"

    # Пример запроса
    query = "SELECT* FROM payment_transaction WHERE executor_work_activity_id =396090172"
    params = (25,)

    try:
        # Выполняем запрос
        results = dblink_query(remote_conn_string, query, params)

        # Выводим результаты
        for row in results:
            print(row)
    except Exception as e:
        print(f"Ошибка: {e}")