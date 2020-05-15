import sys
import random
import os
import pandas as pd
from sklearn.model_selection import train_test_split

if len(sys.argv) != 2:
    sys.stderr.write('Arguments error. Usage:\n')
    sys.stderr.write('\tpython prepare.py data\n')
    sys.exit(1)

# Test data set split ratio
split = 0.20
random.seed(20170426)

input = sys.argv[1]

output_train = os.path.join('data', 'prepared', 'train.csv')
output_test = os.path.join('data', 'prepared', 'test.csv')


def mkdir_p(path):
    if not os.path.exists(path):
        os.makedirs(path)
    
mkdir_p(os.path.join('data', 'prepared'))

input_df = pd.read_csv(input)  
X = input_df['review']
y = (input_df['sentiment'] == 'positive').astype(int)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

train_df = pd.DataFrame({'text': X_train, 'label': y_train})
train_df.to_csv(output_train, index=False)
test_df = pd.DataFrame({'text': X_test, 'label': y_test})
test_df.to_csv(output_test, index=False)
