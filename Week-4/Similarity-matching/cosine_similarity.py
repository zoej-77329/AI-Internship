
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

documents = [
    "Python Pandas NumPy data analysis",
    "Python statistics machine learning",
    "HTML CSS JavaScript web development",
    "Python neural networks deep learning"
]

# Convert documents into TF-IDF vectors
vectorizer = TfidfVectorizer()
vectors = vectorizer.fit_transform(documents)

# Calculate pairwise similarity
similarity_matrix = cosine_similarity(vectors)

print("Cosine Similarity Matrix:")
print(similarity_matrix.round(3))

# Compare first course with all other courses
print("\nSimilarity with First Course:")

for i, score in enumerate(similarity_matrix[0]):
    print(f"Course {i + 1}: {score:.3f}")
