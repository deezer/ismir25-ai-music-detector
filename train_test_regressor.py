"""
Minimal file to train the regression on top of computed fakeprints.

To be adapted depending on your experiment (eg. loading a split file)

python train_test_regressor.py --synth fp_sonics.npy --real fp_fma.npy
"""

import numpy as np
from sklearn.linear_model import LogisticRegression
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--synth", help="synth dataset link", type=str, default="")
parser.add_argument("--real", help="real dataset link", type=str)
args = parser.parse_args()

synth_db = np.load(args.synth, allow_pickle=True).item()
real_db = np.load(args.real, allow_pickle=True).item()

## splits

def create_train_test_split(db, split_fact = 0.8, seed=123):
    np.random.seed(seed)
    keys = np.array(list(db.keys()))
    np.random.shuffle(keys)
    K = int(len(keys) * split_fact)
    return keys[:K], keys[K:]

# you can load a split file here instead, with the ids
train_real_k, test_real_k = create_train_test_split(real_db)
train_synth_k, test_synth_k = create_train_test_split(synth_db)


X_r_train = np.stack( [ real_db[k] for k in train_real_k ], 0 )
X_r_test = np.stack( [ real_db[k] for k in test_real_k ], 0 )
X_s_train = np.stack( [ synth_db[k] for k in train_synth_k ], 0 )
X_s_test = np.stack( [ synth_db[k] for k in test_synth_k ], 0 )

##

X = np.concatenate((X_r_train, X_s_train), 0)
Y = np.concatenate((np.zeros(len(X_r_train)), np.ones(len(X_s_train))), 0)

reg = LogisticRegression(class_weight="balanced")
reg.fit(X, Y)

real_acc_score = reg.score( X_r_test, np.zeros(len(X_r_test)) )
synth_acc_score = reg.score( X_s_test, np.ones(len(X_s_test)) )

print("Real class test acc: {:.3f}%, false positive: {:.3f}%".format(real_acc_score * 100, (1-real_acc_score) * 100 ) )
print("Synth class test acc: {:.3f}%, false negative: {:.3f}%".format(synth_acc_score * 100, (1-synth_acc_score) * 100  ) )

weights = {"W": reg.coef_, "B": reg.intercept_}  # save me