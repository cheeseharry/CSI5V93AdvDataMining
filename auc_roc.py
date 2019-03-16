import numpy as np
from sklearn.metrics import roc_auc_score

#temp = np.array(list)
y_true = np.array([1, 1, 0, 0, 1, 1, 0])
y_scores = np.array([0.8, 0.7, 0.5, 0.5, 0.5, 0.5, 0.3])
print("y_true is ", y_true)
print("y_scores is ", y_scores)
print("AUC is", roc_auc_score(y_true, y_scores))