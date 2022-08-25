import tensorflow as tf
import os

def get_sentence_from_txt(pth, vorb=None, delimiter=" "):
    '''读取txt形成dataset格式
        pth： 文件位置, 内容形如：
        -  909 129 146 149 408 3041 3643 6329 4046 180 8322 1696 1982 8 686 5846 96 1872 77 8 576 5838
        -  word sdf sdf 需要通过vorb进行id化
    '''
    dataset = tf.data.TextLineDataset(pth)
    dataset = dataset.map(lambda string: tf.string_split([string], delimiter).values)
    dataset = dataset.map(lambda tokens: (tokens if vorb == None else vorb.lookup(tokens), tf.size(tokens)))

    #dataset = dataset.batch(1)
    #iterator = dataset.make_initializable_iterator()
    # Query the output of the iterator for input to the model
    #(s,l) = iterator.get_next()
    #sess.run(iterator.initializer)
    #sess.run([s,l])
    return dataset


def input_from_pair_numpy(inputs, targets, params):
    assert len([len(s) for s in inputs]) == 1,  'inputs must be same length'
    assert len([len(s) for s in targets]) == 1, 'targets must be same length'
    input_tensor = tf.data.Dataset.from_tensor_slices(tf.convert_to_tensor(inputs)) #
    target_tensor = tf.data.Dataset.from_tensor_slices(tf.convert_to_tensor(targets))
    dataset = tf.data.Dataset.zip((input_tensor, target_tensor))
    dataset = dataset.batch(params.batch_size)
    iterator = dataset.make_initializable_iterator()
    return iterator.get_next()



def convert_libsvm_2_dense_tfrecords(input_filename, output_filename):
    '''
    :param input_filename:  # 0 5:1 6:1 17:1 21:1 35:1 40:1 53:1 63:1 71:1 73:1 74:1 76:1 80:1 83:1
    :param output_filename:
    :return:
    '''
    current_path = os.getcwd()
    input_file = os.path.join(current_path, input_filename)
    output_file = os.path.join(current_path, output_filename)
    print("Start to convert {} to {}".format(input_file, output_file))

    writer = tf.python_io.TFRecordWriter(output_file)

    for line in open(input_file, "r"):
        data = line.split(" ")
        label = float(data[0])
        ids = []
        values = []
        for fea in data[1:]:
            id, value = fea.split(":")
            ids.append(int(id))
            values.append(float(value))

        # Write each example one by one
        example = tf.train.Example(features=tf.train.Features(feature={
            "label": tf.train.Feature(float_list=tf.train.FloatList(value=[label])),
            "ids": tf.train.Feature(int64_list=tf.train.Int64List(value=ids)),
            "values": tf.train.Feature(float_list=tf.train.FloatList(value=values))
        }))

        writer.write(example.SerializeToString())

    writer.close()
    print("Successfully convert {} to {}".format(input_file, output_file))


def print_libsvm_records(input_file, max_print_number=100):
    print_number = 1
    for serialized_example in tf.python_io.tf_record_iterator(input_file):
        # Get serialized example from file
        example = tf.train.Example()
        example.ParseFromString(serialized_example)

        # Read data in specified format
        label = example.features.feature["label"].float_list.value
        ids = example.features.feature["ids"].int64_list.value
        values = example.features.feature["values"].float_list.value
        print("Number: {}, label: {}, features: {}".format(print_number, label,
                                                           " ".join([str(id) + ":" + str(value) for id, value in zip(ids, values)])))

        # Return when reaching max print number
        if print_number > max_print_number:
            exit()
        else:
            print_number += 1