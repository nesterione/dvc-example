from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd
import scipy.sparse as sparse
import pickle
import os
import sys
import errno
import numpy as np

train_input = os.path.join(sys.argv[1], 'train.csv')
test_input = os.path.join(sys.argv[1], 'test.csv')

train_output = os.path.join(sys.argv[2], 'train.pkl')
test_output = os.path.join(sys.argv[2], 'test.pkl')

vectorizer_output = sys.argv[3]

def mkdir_p(path):
    if not os.path.exists(path):
        os.makedirs(path)
    
mkdir_p(os.path.join('data', 'vectorized'))
mkdir_p(os.path.join('models'))

def save_matrix(df, matrix, output):
    label_matrix = sparse.csr_matrix(df.label.astype(np.int64)).T

    result = sparse.hstack([label_matrix, matrix], format='csr')

    msg = 'The output matrix {} size is {} and data type is {}\n'
    sys.stderr.write(msg.format(output, result.shape, result.dtype))

    with open(output, 'wb') as fd:
        pickle.dump(result, fd, pickle.HIGHEST_PROTOCOL)
    pass


tfidf = TfidfVectorizer()

train_df = pd.read_csv(train_input)
train_mx = tfidf.fit_transform(train_df['text'])
save_matrix(train_df, train_mx, train_output)

test_df = pd.read_csv(test_input)
test_mx = tfidf.transform(test_df['text'])
save_matrix(test_df, test_mx, test_output)

with open(vectorizer_output, 'wb') as fd:
    pickle.dump(tfidf, fd, pickle.HIGHEST_PROTOCOL)



#dvc run -f vectorize.dvc -d src/vectorize.py -d data_tmp/prepared -o data_tmp/vectorized -o models/vectorizer.pkl python src/vectorize.py data_tmp/prepared data_tmp/vectorized models/vectorizer.pkl