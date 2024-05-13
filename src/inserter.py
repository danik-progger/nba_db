import pandas as pd

from pg_client import PgClient


def insert(table_name, table_content):
    client = PgClient()
    client.connect()
    if len(table_content) > 0:
        df_columns = list(table_content)
        columns = ",".join(df_columns)

        values = "VALUES\n"
        for i in range(0, len(table_content)):
            values += "("
            for col in df_columns:
                values += f"{table_content[col][i]}, "
            values = values[:-2] + "),\n"
        values = values[:-2] + ";\n"

        insert_query = f"""
        INSERT INTO basketball.{table_name} ({columns}) {values}"""
        print(insert_query)
        with client.connection.cursor() as cursor:
            cursor.execute(insert_query)

    client.disconnect()


if __name__ == "__main__":
    insert('fans', pd.read_csv('../data/fans.csv'))
    insert('tickets', pd.read_csv('../data/tickets.csv'))
