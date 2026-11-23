
from pathlib import Path

# Project root directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Data directories
DATA_DIR = BASE_DIR / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"

# Model directories
MODEL_DIR = BASE_DIR / "models"
VECTOR_DB_DIR = BASE_DIR / "vector_db"

# Documentation directory
DOCS_DIR = BASE_DIR / "docs"

# Dataset paths
FAQ_FILE = RAW_DATA_DIR / "faqs.json"
TICKET_FILE = RAW_DATA_DIR / "support_tickets.csv"

# Processed dataset paths
CLEANED_FAQ_FILE = PROCESSED_DATA_DIR / "cleaned_faqs.json"
CLEANED_TICKET_FILE = PROCESSED_DATA_DIR / "cleaned_tickets.csv"

# Embedding model
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

# Retrieval configuration
TOP_K_RESULTS = 3
SIMILARITY_THRESHOLD = 0.45

# Application configuration
APP_NAME = "AI Chatbot for Internship Support"
APP_VERSION = "1.0.0"
