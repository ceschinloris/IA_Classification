import numpy as np
import sklearn.datasets
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.linear_model import SGDClassifier
from sklearn.pipeline import Pipeline

categories = ['pos', 'neg']

text_train = sklearn.datasets.load_files("train",
                                         description=None,
                                         categories=categories,
                                         load_content=True,
                                         shuffle=True,
                                         encoding='utf8',
                                         decode_error='strict',
                                         random_state=42)

text_test = sklearn.datasets.load_files("test",
                                        description=None,
                                        categories=categories,
                                        load_content=True,
                                        shuffle=True,
                                        encoding='utf8',
                                        decode_error='strict',
                                        random_state=42)

text_clf = Pipeline([('vect', CountVectorizer()),
                     ('tfidf', TfidfTransformer()),
                     ('clf', SGDClassifier(loss='hinge', penalty='l2', alpha=1e-3,
                                           n_iter=5, random_state=42)),
                     ])

text_clf = text_clf.fit(text_train.data, text_train.target)
predicted = text_clf.predict(text_train)

docs_test = text_test.data
predicted = text_clf.predict(docs_test)
print(np.mean(predicted == text_test.target))
print(sklearn.metrics.classification_report(text_test.target, predicted, target_names=text_test.target_names))
