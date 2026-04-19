# fraud_detection_system
## Folder Structure
```
fraud-detection-system/
│
├── backend/                          # FastAPI (API Layer)
│   ├── app/
│   │   ├── main.py                   # Entry point
│   │   │
│   │   ├── api/                      # API routes
│   │   │   ├── routes.py             # main endpoints
│   │   │   └── deps.py               # dependencies
│   │   │
│   │   ├── core/                     # Core configs
│   │   │   ├── config.py             # .env handling
│   │   │   ├── security.py
│   │   │   └── logger.py
│   │   │
│   │   ├── schemas/                  # Pydantic models
│   │   │   ├── transaction.py
│   │   │   └── response.py
│   │   │
│   │   ├── services/                 # Business logic
│   │   │   ├── inference_service.py  # main prediction flow
│   │   │   ├── feature_engineering.py
│   │   │   ├── preprocessing.py
│   │   │   ├── rules_engine.py
│   │   │   ├── ensemble.py
│   │   │   └── result_store.py       # store/fetch results
│   │   │
│   │   ├── kafka/                    # Kafka integration
│   │   │   ├── producer.py
│   │   │   ├── consumer.py
│   │   │   └── topics.py
│   │   │
│   │   └── db/                       # Optional DB layer
│   │       ├── db.py
│   │       └── models.py
│   │
│   ├── tests/                        # Unit tests
│   │   └── test_api.py
│   │
│   └── .env
│
├── frontend/                         # Streamlit UI
│   ├── app.py                        # main UI
│   │
│   ├── pages/                        # multi-page UI
│   │   ├── 1_upload.py
│   │   ├── 2_live_monitor.py
│   │   └── 3_analytics.py
│   │
│   ├── components/                   # reusable UI
│   │   ├── charts.py
│   │   └── tables.py
│   │
│   └── utils/
│       └── api_client.py             # calls FastAPI
│
├── models/                           # ML Layer (separate)
│   ├── training/
│   │   ├── train.py
│   │   ├── evaluate.py
│   │   ├── hyperparameter_tuning.py
│   │   └── pipeline.py
│   │
│   ├── artifacts/                    # Saved models
│   │   ├── xgboost.pkl
│   │   ├── random_forest.pkl
│   │   ├── scaler.pkl
│   │   └── encoder.pkl
│   │
│   └── registry/                     # Model versioning
│       └── model_registry.json
│
├── kafka/                            # Infra (optional separation)
│   ├── docker-compose.yml
│   └── setup_topics.sh
│
├── data/
│   ├── raw/
│   ├── processed/
│   └── sample_transactions.csv
│
├── notebooks/                        # Experimentation
│   ├── eda.ipynb
│   └── experiments.ipynb
│
├── logs/                             # Logs
│   ├── app.log
│   └── kafka.log
│
├── scripts/                          # Utility scripts
│   ├── run_producer.py
│   └── simulate_transactions.py
│
├── docker-compose.yml                
├── requirements.txt
└── README.md
```