
# System Architecture

## 1. Overview

The application follows a modular architecture
consisting of data processing, NLP, retrieval,
backend and frontend components.

## 2. Data Sources

The chatbot uses two knowledge sources:

1. FAQ documents containing common internship questions
   and their answers.
2. Historical support tickets containing previous
   intern queries and their resolutions.

## 3. Data Processing Layer

The preprocessing module cleans text, removes
unnecessary formatting and prepares the datasets
for NLP processing.

## 4. NLP Layer

Sentence Transformers converts questions and
knowledge-base entries into numerical embeddings.

These embeddings represent the semantic meaning
of the text.

## 5. Retrieval Layer

FAISS stores and searches the generated embeddings.

When an intern submits a question, the system
searches for the most semantically similar entries.

## 6. Response Layer

The response engine selects relevant information
from retrieved entries.

If no sufficiently relevant result is found,
the chatbot provides a fallback response.

## 7. Backend

FastAPI manages incoming requests and communicates
with the chatbot processing modules.

## 8. Frontend

Streamlit provides an interactive interface where
interns can submit questions and receive responses.

## 9. Testing

Pytest will be used to test preprocessing,
retrieval and chatbot functionality.

## 10. Architecture Flow

Intern Query
    |
    v
Streamlit Interface
    |
    v
FastAPI Backend
    |
    v
Query Processing
    |
    v
Sentence Transformer
    |
    v
FAISS Similarity Search
    |
    v
Response Engine
    |
    v
Chatbot Answer
