from visualize_json import VisualizeJson
from word_vectors_model.bert_pretrained import BertPretrained

if __name__ == '__main__':
    # model = gensim.models.KeyedVectors.load_word2vec_format(PRETRAINED_W2V_PATH, binary=True)
    # print("w2v model loaded successfully")

    model = BertPretrained()
    json_vis = VisualizeJson(model)
    # compare_omdb_with_wiki()

