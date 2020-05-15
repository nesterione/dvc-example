import sys
import os
import json 

from sklearn.metrics import classification_report
import pickle

if len(sys.argv) != 4:
    sys.stderr.write('Arguments error. Usage:\n')
    sys.stderr.write('\tpython evaluate.py model features output\n')
    sys.exit(1)

model_file = sys.argv[1]
matrix_file = os.path.join(sys.argv[2], 'test.pkl')
metrics_file = sys.argv[3]

with open(model_file, 'rb') as fd:
    model = pickle.load(fd)

with open(matrix_file, 'rb') as fd:
    matrix = pickle.load(fd)

labels = matrix[:, 0].toarray()
x = matrix[:, 1:]

predictions = model.predict(x)


report = classification_report(labels, predictions, target_names=['negative', 'positive'], output_dict=True)
with open(metrics_file, 'w') as fd:
    fd.write(json.dumps(report, indent=2))