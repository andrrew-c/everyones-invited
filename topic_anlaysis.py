import os
import pandas as pd
import re

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import LatentDirichletAllocation

import matplotlib.pyplot as plt

os.listdir()
file = 'testimonials-2021-04-07.txt'

# read in file
df = pd.read_csv(file, sep='|')

# Bigrams only
ngram = (3,3)

# number of topics
ntopics = 5

def preProcessDF(df):

    dfcopy = df.copy()
    # Remove any row 

    # Change text to string
    #df.text = df.text.astype('str')

    # Remove any lines which only contains numbers
    dfcopy = dfcopy[dfcopy.text.apply(lambda x: True if re.search(r'[A-Z]', str(x), re.I) else False)]

    # Replace any quotes at start or end of string
    dfcopy.text = dfcopy.text.apply(lambda x: re.sub(r'^"|"$', '', str(x)))
    return dfcopy


def plot_top_words(model, feature_names, n_top_words, title, num_rows):

    """ Credit: https://scikit-learn.org/stable/auto_examples/applications/plot_topics_extraction_with_nmf_lda.html#sphx-glr-auto-examples-applications-plot-topics-extraction-with-nmf-lda-py"""
    fig, axes = plt.subplots(num_rows, 5, figsize=(30, 15), sharex=True)
    axes = axes.flatten()
    for topic_idx, topic in enumerate(model.components_):
        top_features_ind = topic.argsort()[:-n_top_words - 1:-1]
        top_features = [feature_names[i] for i in top_features_ind]
        weights = topic[top_features_ind]

        ax = axes[topic_idx]
        ax.barh(top_features, weights, height=0.7)
        ax.set_title(f'Topic {topic_idx +1}',
                     fontdict={'fontsize': 12})
        ax.invert_yaxis()
        ax.tick_params(axis='both', which='major', labelsize=10)
        for i in 'top right left'.split():
            ax.spines[i].set_visible(False)
        fig.suptitle(title, fontsize=12)

    plt.subplots_adjust(top=0.90, bottom=0.05, wspace=0.90, hspace=0.3)
    plt.show()

# Some tidying of data
df =preProcessDF(df)

# Turn text into matrix
vect = TfidfVectorizer(ngram_range=ngram, max_df=0.7, stop_words='english')

# Fit text into matrix
X = vect.fit_transform(df.text)
names =vect.get_feature_names()

# Init lda model
lda = LatentDirichletAllocation(n_components=ntopics, random_state=0)

print("Fit model")
lda.fit(X)

# Plot top words
print("Plot chart")
plot_top_words(lda, names, 10, "Everyones Invited", 1)


