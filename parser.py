import pandas as pd
from models import Assignment
from datetime import datetime

REQUIRED_COLS = ['date', 'attending_name', 'resident_name']

def parse_csv(path: str) -> list[Assignment]:
    df = pd.read_csv(path)
    for col in REQUIRED_COLS:
        if col not in df.columns:
            raise ValueError(f'Missing required column: {col}')
    # Coerce date
    df['date'] = pd.to_datetime(df['date']).dt.date
    out: list[Assignment] = []
    for _, row in df.iterrows():
        out.append(Assignment(
            date=row['date'],
            attending_name=str(row['attending_name']),
            resident_name=str(row['resident_name']),
            service=str(row['service']) if 'service' in df.columns and pd.notna(row.get('service')) else None,
            room=str(row['room']) if 'room' in df.columns and pd.notna(row.get('room')) else None,
        ))
    return out
