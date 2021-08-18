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
    tags = get_review_asbects("The Shelborne is horrible with very outdated rooms! Our room had no furniture besides the bed, 1 chair, and a mini fridge. No table to place small items or a wallet on and no dressers, we were literally living out of our suitcases on the floor. Even the shower didn't have any shelves for personal bath items, again we had to place everything on the bathroom floor in the shower. It's one of the worst hotels I've stayed at in many years! Our room was not cleaned within an appropriate time frame so we were not getting new towels. When we asked for our room to be cleaned and to get new linens at the front desk we were told housekeeping had until 5pm to come clean the room. Most of the beach front rooms don't have a balcony to sit on, so you just have the window view only. If you're on one of the top floor it literally takes 10 minutes or longer just to get on the elevator and 1 elevator shut down for hours during our stay! We were so dissatisfied with the hotel & our room set up that we changed hotels mid trip!",
                              model,cv)
    print(tags)