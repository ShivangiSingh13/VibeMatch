"""
Content-based recommendation module for movies and songs.
"""
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def create_similarity_matrix(df, use_tfidf=False):
    if use_tfidf:
        vectorizer = TfidfVectorizer(max_features=5000, stop_words='english')
    else:
        vectorizer = CountVectorizer(max_features=5000, stop_words='english')
    vectors = vectorizer.fit_transform(df['tags']).toarray()
    similarity = cosine_similarity(vectors)
    return similarity, vectorizer

def recommend_content(item_name, df, similarity, type_):
    """Recommend top 5 similar items (movie or song) based on content."""
    if item_name not in df['title'].values:
        return []
    df = df.reset_index(drop=True)
    idx = df[df['title'] == item_name].index[0]
    distances = list(enumerate(similarity[idx]))
    recs = sorted(distances, key=lambda x: x[1], reverse=True)[1:6]
    return [df.iloc[i[0]]['title'] for i in recs]
