from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd
import pickle
import text_treatment

mass_data_reviews = pd.read_csv('imdb-reviews-pt-br.csv')
# pd.set_option('expand_frame_repr', False)
# pd.set_option('display.max_columns', 999)

classification = mass_data_reviews['sentiment'].replace(['neg', 'pos'], [0, 1])
mass_data_reviews['classification'] = classification

processed_phrase = list()

for opinion in mass_data_reviews.text_pt:
    processed_phrase.append(text_treatment.treat_all(opinion))
mass_data_reviews["treated_text"] = processed_phrase

def train_intelligence(dataframe, text_column, classification_column):
    vectorizer = TfidfVectorizer(lowercase=False)
    bag_of_words = vectorizer.fit_transform(dataframe[text_column])

    train, test, class_train, class_test = train_test_split(bag_of_words, dataframe[classification_column],
                                                            random_state=42, test_size=0.25)

    logistic_regression = LogisticRegression()
    logistic_regression.fit(train, class_train)

    pesos = pd.DataFrame(
        logistic_regression.coef_[0].T,
        index=vectorizer.get_feature_names()
    )
    print(pesos.nlargest(10, 0))
    print(pesos.nsmallest(10, 0))

    filename = 'anton_brain.sav'
    pickle.dump(logistic_regression, open(filename, 'wb'))

    filename = 'anton_vectorizer.sav'
    pickle.dump(vectorizer, open(filename, 'wb'))

    return round(logistic_regression.score(test, class_test) * 100, 2)


print(train_intelligence(mass_data_reviews, 'treated_text', 'classification'))


