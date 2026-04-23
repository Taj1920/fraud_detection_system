from backend.app.db.db import get_connection


def insert_prediction(data: dict):
    conn = get_connection()
    cursor = conn.cursor()

    query = """
    INSERT INTO predictions (trans_num, prediction, fraud_probability)
    VALUES (%s, %s, %s)
    """

    values = (
        data.get("trans_num"),
        data.get("prediction"),
        data.get("fraud_probability")
    )

    cursor.execute(query, values)
    conn.commit()

    cursor.close()
    conn.close()