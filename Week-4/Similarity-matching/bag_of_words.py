
from sklearn.feature_extraction.text import CountVectorizer
import pandas as pd

documents = [
    "Python Machine Learning",
    "Python Data Analysis",
    "Machine Learning",
    "Deep Learning with Python"
]

# Create vectorizer
vectorizer = CountVectorizer()

# Convert text into numerical vectors
vectors = vectorizer.fit_transform(documents)

# Get vocabulary
print("Vocabulary:")
print(vectorizer.get_feature_names_out())

# Convert vectors into DataFrame
df = pd.DataFrame(
    vectors.toarray(),
    columns=vectorizer.get_feature_names_out()
)

print("\nBag of Words Matrix:")
print(df)
