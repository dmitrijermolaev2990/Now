import yaml
import pandas as pd
from sqlalchemy import create_engine, text
from sqlalchemy.types import String, Integer, DateTime, Float, Boolean


def load_config(path='config.yaml'):
    with open(path, 'r') as file:
        return yaml.safe_load(file)


def map_dtype(dtype):
    if pd.api.types.is_integer_dtype(dtype):
        return Integer()
    elif pd.api.types.is_float_dtype(dtype):
        return Float()
    elif pd.api.types.is_bool_dtype(dtype):
        return Boolean()
    elif pd.api.types.is_datetime64_any_dtype(dtype):
        return DateTime()
    else:
        return String()


def fetch_data(db_url, table_name, period_column=None, start_year=None, end_year=None, full_load=False):
    engine = create_engine(db_url)

    if full_load:
        query = f"SELECT * FROM {table_name}"
    elif table_name == 'payment_transaction':
        query = f"""
            SELECT * FROM {table_name}
            WHERE EXTRACT(YEAR FROM {period_column}) BETWEEN {start_year} AND {end_year}
            AND (id <= 2147483647 AND amount <= 2147483647)
        """
    else:
        query = f"""
            SELECT * FROM {table_name}
            WHERE EXTRACT(YEAR FROM {period_column}) BETWEEN {start_year} AND {end_year}
        """

    print(f"Извлекаем данные из {table_name} с {'фильтрацией по годам' if not full_load else 'полной загрузкой'}...")
    return pd.read_sql(text(query), engine)


def create_table(engine, table_name, df):
    dtype_mapping = {col: map_dtype(dtype) for col, dtype in df.dtypes.items()}
    df.head(0).to_sql(table_name, con=engine, if_exists='replace', index=False, dtype=dtype_mapping)
    print(f"Таблица {table_name} создана успешно.")


def insert_data(engine, table_name, df):
    try:
        df.to_sql(table_name, con=engine, if_exists='append', index=False)
        print(f"Данные вставлены в {table_name}.")
    except Exception as e:
        print(f"Ошибка при вставке в таблицу {table_name}: {e}")


def main():
    config = load_config()

    local_db_url = config['local_db']['url']
    local_engine = create_engine(local_db_url)

    for db_key, db_config in config['databases'].items():
        db_url = db_config['url']
        for table_config in db_config.get('tables', []):
            table_name = table_config['name']
            full_load = table_config.get('full_load', False)
            period_column = table_config.get('created_on') or table_config.get('created_at')
            start_year = table_config.get('start_year')
            end_year = table_config.get('end_year')

            print(f"\nОбработка таблицы: {table_name}")
            data = fetch_data(
                db_url,
                table_name,
                period_column=period_column,
                start_year=start_year,
                end_year=end_year,
                full_load=full_load
            )

            if not data.empty:
                create_table(local_engine, table_name, data)
                insert_data(local_engine, table_name, data)
            else:
                print(f"Нет данных для таблицы {table_name}.")

    print("\nЗагрузка завершена успешно.")


if __name__ == '__main__':
    main()
