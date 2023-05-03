import numpy as np


def calc_cos_similarity(text_embeddings, user_query_embedding, top_n=2):
    max_similarity = 0.7
    text_similarity = {}
    user_query_embedding = np.array(user_query_embedding)
    for text_name, texts_embedding in text_embeddings.items():
        texts_array = np.array(texts_embedding['embedding'])
        similarity = texts_array.dot(user_query_embedding) / (np.linalg.norm(texts_array) * np.linalg.norm(user_query_embedding))
        # if similarity > max_similarity:
        #     max_similarity = similarity
        if similarity > max_similarity:
            text_similarity[text_name] = similarity

    text_similarity = sorted(text_similarity.items(), key=lambda x: x[1], reverse=True)
    related_index = [item[0] for item in text_similarity[0:top_n]]
    return related_index
