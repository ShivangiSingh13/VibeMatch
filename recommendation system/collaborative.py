"""
Collaborative filtering recommendation module.
"""
import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

def recommend_collaborative(user_id, user_item_matrix, item_lookup, type_):
    """User-based collaborative filtering: recommend top 5 items for a user."""
    if user_id not in user_item_matrix.index:
        return []
    user_vector = user_item_matrix.loc[user_id].values.reshape(1, -1)
    similarity = cosine_similarity(user_vector, user_item_matrix.values)[0]
    similar_users = np.argsort(similarity)[::-1][1:6]
    recommended = set()
    for idx in similar_users:
        items = user_item_matrix.iloc[idx]
        recommended.update(items[items > 0].index)
    already = set(user_item_matrix.loc[user_id][user_item_matrix.loc[user_id] > 0].index)
    recs = list(recommended - already)
    return [item_lookup[i] for i in recs[:5]]
