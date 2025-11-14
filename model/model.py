from sentence_transformers import SentenceTransformer
from sentence_transformers import util
import pandas as pd
import numpy as np

model = SentenceTransformer('sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2')

# Функция ищет по всем документам
def default_search(user_text: str, docs: dict, embeddings: dict):
    user_emb = model.encode(user_text)
    data = pd.DataFrame()
    for doc in docs:
        data = pd.concat([data, docs[doc]])
    all_embs = np.empty((384,))
    for emb in embeddings:
        all_embs = np.vstack([all_embs, embeddings[emb]])
    all_embs = np.float32(np.delete(all_embs, 0, axis=0))
    answers = []
    for emb in all_embs:
        result = round(util.pytorch_cos_sim(emb, user_emb).item()*100, 1)
        answers.append(result)
    data['similarity'] = answers
    data = data.sort_values('similarity', ascending=False).head(10)
    data = data.drop('similarity', axis=1)
    data = data.set_index('punkt').T.to_dict('list')
    return data

# Функция ищет по выбранному документу
def doc_search(user_text: str, doc: str, docs: dict, embeddings: dict):
    user_emb = model.encode(user_text)
    answers = []
    data = docs[doc]
    for emb in embeddings[doc]:
        result = round(util.pytorch_cos_sim(emb, user_emb).item()*100, 1)
        answers.append(result)
    data['similarity'] = answers
    data = data.sort_values('similarity', ascending=False).head(10)
    data = data.drop('similarity', axis=1)
    data = data.set_index('punkt').T.to_dict('list')
    return data