from visualize_json import VisualizeJson
from word_vectors_model.bert_pretrained import BertPretrained
from word_vectors_model.google_news_w2v import GoogleNewsW2V
from experiments import *

if __name__ == '__main__':
    # model = gensim.models.KeyedVectors.load_word2vec_format(PRETRAINED_W2V_PATH, binary=True)
    # print("w2v model loaded successfully")

    model_bert = BertPretrained()
    model_w2v = GoogleNewsW2V(None)
    json_vis_bert = VisualizeJson(model_bert)
    json_vis_w2v = VisualizeJson(model_w2v)
    # compare_omdb_with_wiki()

