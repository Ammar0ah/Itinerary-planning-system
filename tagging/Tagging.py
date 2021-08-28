import pickle
import numpy as np

def get_n_topic_words(lda_model, n_top_words, topic_idx,vec):
    n_topic_words = []
    vocab = vec.get_feature_names()
    topic_words_idx = np.argsort(lda_model.components_[topic_idx])[::-1][:n_top_words]
    n_topic_words = [vocab[i] for i in topic_words_idx]
    return n_topic_words




def get_max_topics(probabilities, number_of_topics):
    probabilities = [[index, prob] for index, prob in enumerate(probabilities)]
    probabilities.sort(key=lambda k: k[1], reverse=True)
    probabilities = [i[0] for i in probabilities]
    return probabilities[:number_of_topics]


def get_review_asbects(review, lda_model,vec):
    transformed_review = vec.transform([review])
    prob = lda_model.transform(transformed_review)
    prob = prob.tolist()[0]
    best_topics = get_max_topics(prob, 3)
    aspects = []
    top_topic_words = []
    for topic in best_topics:
        x = get_n_topic_words(lda_model, 10, topic,vec)
        top_topic_words.extend(x)
    for word in top_topic_words:
        if word in review:
            aspects.append(word)
    return list(set(aspects))

if __name__ == '__main__':
    model = None
    cv = None
    with open('cv.pkl', 'rb') as f:
        cv = pickle.load(f)

    with open('lda.pkl','rb') as f:
        model =  pickle.load(f)[0]
    text = "We loved the location of this hotel The fact that it is set in a Park away from the busy centre of dam square was great The tram system was brilliant and easy to handle The hotel is lovely and the bed was comfy Staff were very friendly and helpful and familiarized themselves with us when they realized we travelled from Ireland.\
yet we did not like the fact that breakfast was not included although you could pay extra for this The room we stayed in was lacking in space a bit and the bathroom was very badly lit to use the mirror in there which meant getting ready for evening a bit tricky but only a small negative comment"
    tags = get_review_asbects(text,model,cv)
    print(tags)