import sqlparse
import re
from typing import Dict, List, Any
from collections import defaultdict
from psycopg2.extras import RealDictCursor
import psycopg2


class DBLink:
    def __init__(self, conn_string):
        self.conn = psycopg2.connect(conn_string)
        self.cursor = self.conn.cursor(cursor_factory=RealDictCursor)

    def execute(self, query):
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def close(self):
        self.cursor.close()
        self.conn.close()


class SmartSQLJoiner:
    def __init__(self, conn_map: Dict[str, str]):
        self.conn_map = conn_map

    def parse_sql(self, sql: str):
        # 1. Парсим таблицы и алиасы
        tables = re.findall(r'(\w+)\.(\w+)\s+(\w+)', sql)
        # [('db1', 'table1', 't1'), ('db2', 'table2', 't2')]

        # 2. Парсим JOIN ON
        join_cond = re.search(r'ON\s+(\w+)\.(\w+)\s*=\s*(\w+)\.(\w+)', sql).groups()
        # ('t1', 'id', 't2', 'foreign_id')

        # 3. Парсим WHERE
        where_match = re.search(r'WHERE\s+(.*)', sql)
        where_clause = where_match.group(1) if where_match else None

        return tables, join_cond, where_clause

    def generate_subqueries(self, tables, where_clause):
        subqueries = {}
        for db, table, alias in tables:
            where = ''
            if where_clause and alias in where_clause:
                # Примитивно: вырезаем where, относящийся к этой таблице
                pattern = rf'{alias}\.\w+\s*=\s*[^ ]+'
                conditions = re.findall(pattern, where_clause)
                if conditions:
                    replaced = [re.sub(rf'{alias}\.', '', c) for c in conditions]
                    where = 'WHERE ' + ' AND '.join(replaced)

            subqueries[alias] = {
                'db': db,
                'query': f'SELECT * FROM {table} {where}'
            }
        return subqueries

    def join_in_memory(self, data1: List[Dict[str, Any]], key1: str, data2: List[Dict[str, Any]], key2: str):
        result = []
        for row1 in data1:
            for row2 in data2:
                if str(row1.get(key1)) == str(row2.get(key2)):
                    result.append({**row1, **row2})
        return result

    def execute(self, sql: str):
        tables, join_cond, where_clause = self.parse_sql(sql)
        subqueries = self.generate_subqueries(tables, where_clause)

        datasets = {}
        for alias, info in subqueries.items():
            db = info['db']
            conn_str = self.conn_map[db]
            db_link = DBLink(conn_str)
            try:
                datasets[alias] = db_link.execute(info['query'])
            finally:
                db_link.close()

        t1_alias, k1, t2_alias, k2 = join_cond
        return self.join_in_memory(datasets[t1_alias], k1, datasets[t2_alias], k2)
