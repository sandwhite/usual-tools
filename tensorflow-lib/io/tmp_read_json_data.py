import tensorflow as tf
import pandas as pd
import numpy as np
import json

path = "data/small_logicfeat"
LABEL = "is_click"
CATE_FEATURE_COL = ["brand", "userProfileGameCateLst"]
NUMER_FEATURE_COL = ["show", "click"]
num_epochs = 2
BATCH_SIZE = 5
MAX_BUCKETS = 1000


def _json(line):
    data = json.loads(line.decode('utf-8'))
    # feat = dict({k: tf.constant(data[k]) for k in CATE_FEATURE_COL})
    feat = np.array([data[k] for k in CATE_FEATURE_COL])
    feat = dict(zip(CATE_FEATURE_COL, feat))
    #feat = [tf.string_to_hash_bucket_fast(data[k], MAX_BUCKETS) for k in CATE_FEATURE_COL]
    #feat = tf.stack(feat)
    #label = tf.constant(data[LABEL])
    label = data[LABEL]
    return feat, label


def parse_json(value):
    return tf.py_func(_json, [value], [tf.string, tf.string])


dataset = tf.data.TextLineDataset(path)
dataset = dataset.map(parse_json)
dataset = dataset.repeat(num_epochs)
batched_dataset = dataset.batch(BATCH_SIZE)
iterator = batched_dataset.make_one_shot_iterator()
feature, label = iterator.get_next()

with tf.Session() as sess:
    print(sess.run(feature))
    print(sess.run(label))
