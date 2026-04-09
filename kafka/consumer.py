import json
import pandas as pd
import numpy as np
import requests
from kafka import KafkaConsumer
from config import KAFKA_BROKER,TOPIC_NAME,GROUP_ID

#kafka consumer
consumer = KafkaConsumer(
    TOPIC_NAME,
    bootstrap_servers = KAFKA_BROKER,
    group_id = GROUP_ID,
    value_deserializer = lambda x: json.loads(x.decode("utf-8"))
)

#feature engineering
def feature_engineering(data):
    df = pd.DataFrame(data,index=[0])
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

#feature selection
def feature_extraction(df):
    #select required columns
    selected_cols = ['hour', 'day','category', 'amt',
            'gender', 'state',
        'distance','city_pop', 'age']
    
    df = df.loc[:,selected_cols]
    return df


for message in consumer:
    data = message.value
    df = feature_engineering(data)
    df = feature_extraction(df)
    try:
        response = requests.post("http://127.0.0.1:8000/predict_fraud",json = df.to_dict(orient="records")[0])
        print(response.json())
    except:
        print("something went wrong")
    