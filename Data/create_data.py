import pandas as pd
from sqlalchemy import create_engine

def create_sqlite_db_from_csv(file_path):
  
    df = pd.read_csv(file_path)

    db_path = r'C:\Users\arun5\Desktop\Spend_analyzer\src\Data\spend-sqlite.db'
    engine = create_engine(f'sqlite:///{db_path}')

    df.to_sql('spend_data', con=engine, index=False, if_exists='replace')

    print(f"SQLite DB created at: {db_path}")

    return db_path



