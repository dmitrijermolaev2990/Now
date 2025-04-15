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


def fetch_data(db_url, table_name, period_column, start_year, end_year):
    engine = create_engine(db_url)
    query = f"""
        SELECT * FROM {table_name}
        WHERE EXTRACT(YEAR FROM {period_column}) BETWEEN {start_year} AND {end_year}
    """
    print(f"Извлекаем данные из {table_name} for the period {start_year}-{end_year} using {period_column}...")
    return pd.read_sql(text(query), engine)


def create_table(engine, table_name, df):
    dtype_mapping = {col: map_dtype(dtype) for col, dtype in df.dtypes.items()}
    df.head(0).to_sql(table_name, con=engine, if_exists='replace', index=False, dtype=dtype_mapping)
    print(f"Таблица {table_name} создана успешно.")


def insert_data(engine, table_name, df):
    df.to_sql(table_name, con=engine, if_exists='append', index=False)
    print(f"Данные вставлены {table_name}.")


def main():
    config = load_config()

    local_db_url = config['local_db']['url']
    local_engine = create_engine(local_db_url)

    # Обработка всех внешних БД
    for db_key, db_config in config['databases'].items():
        db_url = db_config['url']
        for table_config in db_config.get('tables', []):
            table_name = table_config['name']
            # поддержка разных названий поля
            period_column = table_config.get('created_on') or table_config.get('created_at')
            start_year = table_config['start_year']
            end_year = table_config['end_year']

            print(f"Processing table {table_name} with period column {period_column}")
            data = fetch_data(db_url, table_name, period_column, start_year, end_year)

            if not data.empty:
                create_table(local_engine, table_name, data)
                insert_data(local_engine, table_name, data)
            else:
                print(f"No data found for {table_name} in {start_year}-{end_year}.")

    print("Успех.")


if __name__ == '__main__':
    main()
