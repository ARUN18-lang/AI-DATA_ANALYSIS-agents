from .load_data import get_details_from_sqlite_db
from .create_data import create_sqlite_db_from_csv
import json 
import pandas as pd

"""SQL DATA"""
def get_json_from_sqlite_db(csv_file_path):
    db_path = create_sqlite_db_from_csv(csv_file_path)
    details = get_details_from_sqlite_db(db_path)
    json_data = json.dumps(details, indent=4)
    return json_data

def get_db_path(csv_file_path):
    db_path = create_sqlite_db_from_csv(csv_file_path)
    return db_path

"""CSV DATA"""
def summarizer(file_path):
    df = pd.read_csv(file_path)

    buffer = []
    buffer.append("## Dataset Overview")
    buffer.append(f"- Shape: {df.shape} (rows × columns)")
    
    dtype_counts = df.dtypes.value_counts().to_dict()
    buffer.append("\n## Data Types")
    for dtype, count in dtype_counts.items():
        buffer.append(f"- {dtype}: {count} columns")
    
    buffer.append("\n## Descriptive Statistics")
    buffer.append(df.describe(include='all').to_markdown())
    
    missing = df.isna().sum()
    buffer.append("\n## Missing Values")
    buffer.append(missing[missing > 0].to_markdown() if missing.any() else "No missing values found")
    
    buffer.append("\n## Unique Value Counts")
    for col in df.select_dtypes(include=['object', 'category']):
        buffer.append(f"- {col}: {df[col].nunique()} unique values")
    
    buffer.append("\n## Data Sample")
    buffer.append(df.head(3).to_markdown())
    
    return "\n".join(buffer)


#csv_file = r'C:\Users\arun5\Desktop\Spend_analyzer\src\Data\transaction_data_250.csv'
#print(get_json_from_sqlite_db(csv_file))