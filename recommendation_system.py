import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

# -------------------
# Data setup
# -------------------
ratings_dict = {
    'The Matrix': [5, 4, 1, 0, 0],
    'John Wick': [4, 5, 1, 0, 0],
    'Inception': [5, 5, 0, 1, 0],
    'The Notebook': [0, 0, 5, 4, 4],
    'Titanic': [0, 0, 4, 5, 5],
}

users = ['Alice', 'Bob', 'Carol', 'Dave', 'Eve']

df = pd.DataFrame(ratings_dict, index=users)

# -------------------
# Compute user similarity
# -------------------
user_similarity = cosine_similarity(df.fillna(0))
user_sim_df = pd.DataFrame(user_similarity, index=users, columns=users)

# -------------------
# Recommendation function
# -------------------
def recommend_movies(user_name, df=df, user_sim_df=user_sim_df):
    if user_name not in df.index:
        print(f"User '{user_name}' not found.")
        return []
    
    # Find the most similar user (excluding self)
    sim_scores = user_sim_df.loc[user_name].drop(user_name)
    most_similar_user = sim_scores.idxmax()
    print(f"\nMost similar user to {user_name} is {most_similar_user} (similarity: {sim_scores[most_similar_user]:.2f})")
    
    # Get movies this similar user likes that the target hasn't rated yet
    target_user_ratings = df.loc[user_name]
    similar_user_ratings = df.loc[most_similar_user]
    
    recommendations = similar_user_ratings[(similar_user_ratings >= 3) & (target_user_ratings == 0)]
    
    if recommendations.empty:
        print(f"No high-rated movies to recommend from {most_similar_user}'s preferences.")
        return []
    
    print(f"Movies {most_similar_user} likes (≥3) that {user_name} hasn't rated yet: {list(recommendations.index)}")
    return list(recommendations.index)

# -------------------
# Example usage
# -------------------
target_user = 'Alice'
print(f"\nRecommendations for {target_user}:")
recommended_movies = recommend_movies(target_user)

for movie in recommended_movies:
    print(f"- {movie}")
