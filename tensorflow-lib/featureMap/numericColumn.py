import tensorflow as tf

price = {'price': [[1.], [2.], [3.], [4.]]}

column = tf.feature_column.numeric_column('price', normalizer_fn=lambda x:x+2)
tensor = tf.feature_column.input_layer(price,[column])

with tf.Session() as session:
    print(session.run([tensor]))