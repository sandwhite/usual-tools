import tensorflow as tf
import sys
import os

def get_feature_example(line):
    columns = line.strip().split(" ")
    label = int(columns[0])
    feats = columns[1:]

    user_feat_ids = []
    user_feat_vals = []
    ad_feat_ids = []
    ad_feat_vals = []
    ctx_feat_ids = []
    ctx_feat_vals = []

    for feat in feats:
        field, index, vals = feat.split(":")
        index = int(index)
        vals = float(vals)
        if field == "0":
            user_feat_ids.append(index)
            user_feat_vals.append(vals)
        if field == "1":
            ad_feat_ids.append(index)
            ad_feat_vals.append(vals)
        if field == "2":
            ctx_feat_ids.append(index)
            ctx_feat_vals.append(vals)

    example = tf.train.Example(
        features=tf.train.Features(feature={
            "label": tf.train.Feature(int64_list=tf.train.Int64List(value=[label])),
            'user_feat_ids': tf.train.Feature(int64_list=tf.train.Int64List(value=user_feat_ids)),
            'user_feat_vals': tf.train.Feature(float_list=tf.train.FloatList(value=user_feat_vals)),
            'ad_feat_ids': tf.train.Feature(int64_list=tf.train.Int64List(value=ad_feat_ids)),
            'ad_feat_vals': tf.train.Feature(float_list=tf.train.FloatList(value=ad_feat_vals)),
            'ctx_feat_ids': tf.train.Feature(int64_list=tf.train.Int64List(value=ctx_feat_ids)),
            'ctx_feat_vals': tf.train.Feature(float_list=tf.train.FloatList(value=ctx_feat_vals))
        }))
    return example


def trans_libsvm_format_2_tfrecords(libsvm_filenames, tfrecords_filename):
    writer = tf.python_io.TFRecordWriter(tfrecords_filename)
    for line in open(libsvm_filenames):
        try:
            example = get_feature_example(line)
            writer.write(example.SerializeToString())  # 序列化为字符串
        except:
            print(line)
    writer.close()


def parse_sparse_records(records):
  features = {"label": tf.FixedLenFeature([], tf.int64, default_value=0),
              "user_feat_ids": tf.VarLenFeature(tf.int64),
              "user_feat_vals": tf.VarLenFeature(tf.float32),
              "ad_feat_ids": tf.VarLenFeature(tf.int64),
              "ad_feat_vals": tf.VarLenFeature(tf.float32),
              "ctx_feat_ids": tf.VarLenFeature(tf.int64),
              "ctx_feat_vals": tf.VarLenFeature(tf.float32)
              }
  parsed_features = tf.parse_single_example(records, features)
  features = {"user_feat_ids": tf.sparse_tensor_to_dense(parsed_features['user_feat_ids']),
             "user_feat_vals": tf.sparse_tensor_to_dense(parsed_features['user_feat_vals']),
             "ad_feat_ids": tf.sparse_tensor_to_dense(parsed_features['ad_feat_ids']),
             "ad_feat_vals": tf.sparse_tensor_to_dense(parsed_features['ad_feat_vals']),
             "ctx_feat_ids": tf.sparse_tensor_to_dense(parsed_features['ctx_feat_ids']),
             "ctx_feat_vals": tf.sparse_tensor_to_dense(parsed_features['ctx_feat_vals'])
             }

  return features, parsed_features["label"]


def parse_sparse_libsvm_records(batch_serialized_example):
    features = tf.parse_single_example(batch_serialized_example,
                                features={
                                    "label": tf.FixedLenFeature([], tf.float32),
                                    "ids":   tf.VarLenFeature(tf.int64),
                                    "values": tf.VarLenFeature(tf.float32),
                                })
    return features


if __name__ == "__main__":
   if len(sys.argv) < 2:
      sys.exit(1)

   libsvm_file_path = sys.argv[1] #"data"
   tfrecord_file_path = sys.argv[2] #"tfrecord"

   print("libsvm_file_path:", libsvm_file_path)
   print("tfrecord_file_path:", tfrecord_file_path)

   if not os.path.exists(tfrecord_file_path):
      os.mkdir(tfrecord_file_path)

   for files in os.listdir(libsvm_file_path):
      print("prossing file: ", files)
      output_filename = tfrecord_file_path + "/" + files + ".tfrecord"
      if not os.path.exists(output_filename):
          trans_libsvm_format_2_tfrecords(libsvm_file_path + "/" + files, output_filename)
