import logging
import os
import pandas as pd
import numpy as np

logger = logging.getLogger(__name__)


# Функция, формирующая словари с документами и их эмбеддингами
def prepare_docs(root: str):
    doc_path = os.path.join(root, 'docs')
    emb_path = os.path.join(root, 'embeddings')
    doc_list = os.listdir(doc_path)
    emb_list = os.listdir(emb_path)
    docs = {}
    embeddings = {}
    try:
        for doc in doc_list:
            docs[doc[:3]] = pd.read_csv(os.path.join(doc_path, doc))
    except Exception as e:
        logger.error("Error reading a doc: %s", e)
        raise e
    try:
        for emb in emb_list:
            embeddings[emb[:3]] = np.load(os.path.join(emb_path, emb))
    except Exception as e:
        logger.error("Error reading a emb: %s", e)
        raise e

    return docs, embeddings