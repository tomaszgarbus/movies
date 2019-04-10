import gensim
from omdb_download import get_and_cache_movie_json
from visualize_json import VisualizeJson
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt

if __name__ == '__main__':
    movie_json = get_and_cache_movie_json("Star Wars Episode V")
    print(movie_json)

    model = gensim.models.KeyedVectors.load_word2vec_format('./data/GoogleNews-vectors-negative300.bin', binary=True)
    json_viz = VisualizeJson(model)
    pairs = json_viz.get_number_context_pairs(movie_json)
    trans = TSNE().fit_transform(list(map(lambda a: a[1], pairs)))
    fig, ax = plt.subplots()
    ax.scatter(trans[:,0], trans[:,1])
    for i, txt in enumerate(trans):
        ax.annotate(pairs[i][0], trans[i])
    plt.show()
