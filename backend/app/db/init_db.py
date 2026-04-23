from backend.app.db.db import get_connection

def create_table():
    conn = get_connection()
    cursor = conn.cursor()

    query = """
    CREATE TABLE IF NOT EXISTS predictions (
        id INT AUTO_INCREMENT PRIMARY KEY,
        trans_num VARCHAR(50),
        prediction VARCHAR(20),
        fraud_probability FLOAT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """

    cursor.execute(query)
    conn.commit()

    print("Table created successfully")

if __name__ == "__main__":
    create_table()