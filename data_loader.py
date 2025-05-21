import pandas as pd

def load_data(file_name):
    df = pd.read_csv(file_name)
    df_sample = df.sample(frac=0.001)
    return df_sample