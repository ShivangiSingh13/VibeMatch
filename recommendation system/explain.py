"""
Explanation module for recommendations.
"""
def explain_recommendation(input_item, recommended_item, df):
    try:
        if input_item in df['title'].values:
            user_row = df[df['title'] == input_item].iloc[0]
            rec_row = df[df['title'] == recommended_item].iloc[0]
            user_tags = set(user_row['tags'].split())
            rec_tags = set(rec_row['tags'].split())
            shared = list(user_tags & rec_tags)
            if shared:
                meaningful = [s for s in shared if len(s) > 3][:3]
                return f"Shared features: {', '.join(meaningful)}"
        return "Similar genre or style"
    except Exception:
        return "Recommended based on similarity"
