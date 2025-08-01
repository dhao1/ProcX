import pandas as pd

def load_ocel(file_path: str) -> pd.DataFrame:
    if file_path.endswith('.jsonocel'):
        import json
        with open(file_path, 'r') as f:
            data = json.load(f)
        df = pd.DataFrame(data['events'])
    elif file_path.endswith('.csv'):
        df = pd.read_csv(file_path)
    else:
        raise ValueError("Unsupported file type.")
    return df
