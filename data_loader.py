import pandas as pd

def load_data(file_obj):
    """
    Load CSV or Excel into a DataFrame. Handles both uploaded files and in-memory buffers.
    """
    try:
        # Try reading as CSV first
        file_obj.seek(0)
        df = pd.read_csv(file_obj)
        return _postprocess(df)
    except Exception:
        pass

    try:
        # Then try reading as Excel
        file_obj.seek(0)
        df = pd.read_excel(file_obj)
        return _postprocess(df)
    except Exception as e:
        raise ValueError(f"Unsupported or unreadable file format: {e}")

def _postprocess(df):
    """
    Common preprocessing steps
    """
    df.columns = df.columns.str.lower()
    if 'order_date' in df.columns:
        df['order_date'] = pd.to_datetime(df['order_date'], dayfirst=True, errors='coerce')
    return df
