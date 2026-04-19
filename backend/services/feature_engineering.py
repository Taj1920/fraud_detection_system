import numpy as np
import pandas as pd


def engineer_features(df):
    #convert to datetime column
    df["trans_date_trans_time"] = pd.to_datetime(df["trans_date_trans_time"])
    df["dob"] = pd.to_datetime(df["dob"])

    #create age column
    df["age"] = df["trans_date_trans_time"].dt.year - df["dob"].dt.year

    #extract time features
    df["hour"] = df["trans_date_trans_time"].dt.hour
    df["day"] = df["trans_date_trans_time"].dt.day

    #Distance calculation
    df["distance"] = np.sqrt(
                            (df["lat"]-df["merch_lat"])**2 + 
                             (df["long"]-df["merch_long"])**2
                             )
    
    return df


def extract_features(df):
    #Remove unwanted columns
    unwanted_cols = ['trans_date_trans_time', 'cc_num', 'merchant',
        'first', 'last', 'street', 'city', 'zip',
       'lat', 'long', 'job', 'dob', 'trans_num', 'unix_time',
       'merch_lat', 'merch_long']
    df = df.drop(unwanted_cols,axis=1)
    return df


if __name__=="__main__":
    from pathlib import Path
    ROOT_DIR = Path(__file__).resolve().parents[2]
    test_path = ROOT_DIR / "data" / "fraudTest.csv"
    df = pd.read_csv(test_path,index_col=0)
    sam = df.sample()
    print("sam: ",sam)
    df = engineer_features(sam)
    df = extract_features(df)
    print("cleaned: ",df)