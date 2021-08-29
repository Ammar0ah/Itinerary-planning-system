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

    with open('lda_15_cv.pkl','rb') as f:
        model =  pickle.load(f)[1]


    text = "My husband and I wanted to get away but didnt have time in our schedule " \
           "this year to plan an extensive vacation as we usually do. We hesitated booking an 'all inclusive' " \
           "package as thats not our cup of tea. We did stay in an EXCELLENCE room status which I would highly suggest. " \
           "Now that I know what I know I would not go back unless I could book that level of a room. Sorry we just aren't " \
           "the 'carnival cruise' rowdy couple and do not like that atmosphere. The wait staff at this resort is nothing short of Amazing." \
           " They work so hard to please you and make your stay perfect. At the Excellence Pool by building 8, Martha and Antonio were just THE BEST." \
           " We were there for 10 days and only went off property once to Isla and I wouldnt even do that again. Really no reason to leave the resort. " \
           "Just keep in mind there IS a dress code for the restaurants and many of the require pants for men. They DO go by that and wont let you in if you " \
           "arent dressed appropriately. Luckily the hubs and I love to dress up so that wasnt a problem but I overhead people complaining about it. " \
           "I think most places in the states have a dress code but we arent used to them getting followed. They really should send an email after" \
           " booking stating this information and how critical it is. Maybe they did and I didnt read it but we were fine and had enough clothing that worked." \
           " The food was good for all inclusive food. We are kind of foodies so not the level we would choose but again for what it was for it was really good" \
           ". We also had a couple spa days. We have been to many spas in many places but this one was by far the best my husband and I both have had. " \
           "I wouldnt hesitate booking another getaway here to relax and get pampered"
    tags = get_review_asbects(text,model,cv)
    print(tags)