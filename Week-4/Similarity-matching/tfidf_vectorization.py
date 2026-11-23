
from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd

documents = [
    "Python programming fundamentals",
    "Python Pandas NumPy data analysis",
    "Python statistics machine learning",
    "Python neural networks deep learning",
    "HTML CSS JavaScript web development",
    "Python OpenCV computer vision"
]

# Create TF-IDF vectorizer
vectorizer = TfidfVectorizer()

# Learn vocabulary and transform documents
tfidf_matrix = vectorizer.fit_transform(documents)

# Get vocabulary
features = vectorizer.get_feature_names_out()

# Convert into DataFrame
df = pd.DataFrame(
    tfidf_matrix.toarray(),
    columns=features
)

print("TF-IDF Vocabulary:")
print(features)

print("\nTF-IDF Matrix:")
print(df.round(3))

print("\nMatrix Shape:")
print(tfidf_matrix.shape)
