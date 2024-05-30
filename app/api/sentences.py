from typing import Any, List, AnyStr

from fastapi import APIRouter, Request

from app.models.doc_vec import SentencesReq
import os
import io

from gensim.models import CoherenceModel, Doc2Vec, LdaModel
import gensim.corpora as corpora
from gensim.utils import simple_preprocess
from gensim.test.utils import datapath

def get_path(model):
    return os.path.join(os.path.dirname(__file__), "models", model)

DOC2VEC_MODEL_PATH = get_path('doc2vec_model.model')
LDA_MODEL_PATH = get_path('model_v2')
DICTIONARY_PATH = get_path('model_v2.id2word')

model_doc2vec = Doc2Vec.load(DOC2VEC_MODEL_PATH)

lda_model = LdaModel.load(LDA_MODEL_PATH)

dictionary = corpora.Dictionary.load(DICTIONARY_PATH)

num_topics = lda_model.num_topics

topic_descriptions = {i: ' '.join([word for word, _ in lda_model.show_topic(i, topn=5)]) for i in range(num_topics)}

sentences_router = APIRouter()


def predict_lda_topic(text):
    bow_vector = dictionary.doc2bow(simple_preprocess(text))
    topics = lda_model.get_document_topics(bow_vector)
    return max(topics, key=lambda item: item[1])[0]


@sentences_router.post("/sentences")
async def predict(request: Request, payload: SentencesReq) -> Any:
    """
    DocVec sentences classify API
    """
    grouped_sentences = {}

    sentences = payload.sentences
    for sentence in sentences:
        topic = predict_lda_topic(sentence)
        if topic not in grouped_sentences:
            grouped_sentences[topic] = {'theme': topic_descriptions[topic], 'sentences': []}
        grouped_sentences[topic]['sentences'].append(sentence)

    return grouped_sentences
