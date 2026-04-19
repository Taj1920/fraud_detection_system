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
    #select required columns
    selected_cols = ['hour', 'day','category', 'amt',
            'gender', 'state',
        'distance','city_pop', 'age', 'is_fraud']
    
    df = df.loc[:,selected_cols]
    return df