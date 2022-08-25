import tensorflow as tf

colors = {'colors': ['green','red','red','blue','blue','yellow','pink','indigo']}  

column = tf.feature_column.categorical_column_with_hash_bucket(
        key='colors',
        hash_bucket_size=10,
        dtype=tf.string
    )

indicator = tf.feature_column.indicator_column(column)
tensor = tf.feature_column.input_layer(colors, [indicator])

with tf.Session() as session:
    session.run(tf.global_variables_initializer())
    session.run(tf.tables_initializer())
    print(session.run([tensor]))