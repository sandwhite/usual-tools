import tensorflow as tf
import numpy as np

# Adapted to support sampled_softmax loss function, which accepts activations
# instead of logits.
def sequence_loss_by_example(inputs, targets, weights, loss_function,
                             average_across_timesteps=True, name=None):
  """Sampled softmax loss for a sequence of inputs (per example).

  Args:
    inputs: List of 2D Tensors of shape [batch_size x hid_dim].
    targets: List of 1D batch-sized int32 Tensors of the same length as logits.
    weights: List of 1D batch-sized float-Tensors of the same length as logits.
    loss_function: Sampled softmax function (inputs, labels) -> loss
    average_across_timesteps: If set, divide the returned cost by the total
      label weight.
    name: Optional name for this operation, default: 'sequence_loss_by_example'.

  Returns:
    1D batch-sized float Tensor: The log-perplexity for each sequence.

  Raises:
    ValueError: If len(inputs) is different from len(targets) or len(weights).
  """
  if len(targets) != len(inputs) or len(weights) != len(inputs):
    raise ValueError('Lengths of logits, weights, and targets must be the same '
                     '%d, %d, %d.' % (len(inputs), len(weights), len(targets)))
  with tf.op_scope(inputs + targets + weights, name,
                   'sequence_loss_by_example'):
    log_perp_list = []
    for inp, target, weight in zip(inputs, targets, weights):
      crossent = loss_function(inp, target)
      log_perp_list.append(crossent * weight)
    log_perps = tf.add_n(log_perp_list)
    if average_across_timesteps:
      total_size = tf.add_n(weights)
      total_size += 1e-12  # Just to avoid division by 0 for all-0 weights.
      log_perps /= total_size
  return log_perps


def sampled_sequence_loss(inputs, targets, weights, loss_function,
                          average_across_timesteps=True,
                          average_across_batch=True, name=None):
  """Weighted cross-entropy loss for a sequence of logits, batch-collapsed.

  Args:
    inputs: List of 2D Tensors of shape [batch_size x hid_dim].
    targets: List of 1D batch-sized int32 Tensors of the same length as inputs.
    weights: List of 1D batch-sized float-Tensors of the same length as inputs.
    loss_function: Sampled softmax function (inputs, labels) -> loss
    average_across_timesteps: If set, divide the returned cost by the total
      label weight.
    average_across_batch: If set, divide the returned cost by the batch size.
    name: Optional name for this operation, defaults to 'sequence_loss'.

  Returns:
    A scalar float Tensor: The average log-perplexity per symbol (weighted).

  Raises:
    ValueError: If len(inputs) is different from len(targets) or len(weights).
  """
  with tf.op_scope(inputs + targets + weights, name, 'sampled_sequence_loss'):
    cost = tf.reduce_sum(sequence_loss_by_example(
        inputs, targets, weights, loss_function,
        average_across_timesteps=average_across_timesteps))
    if average_across_batch:
      batch_size = tf.shape(targets[0])[0]
      return cost / tf.cast(batch_size, tf.float32)
    else:
      return cost



def sigmoid_cross_entropy_with_probs(labels=None,probs=None,name=None):
    try:
        labels.get_shape().merge_with(probs.get_shape())
    except ValueError:
        raise ValueError("probs and labels must have the same shape (%s vs %s)" % (probs.get_shape(), labels.get_shape()))
    return  -tf.reduce_sum(labels * tf.log(probs,)+(1-labels)*tf.log(1-probs), name=name)

def tf_weighted_sigmoid_ce_with_logits(labels=None, logits=None, sample_weight=None):
    return tf.multiply(tf.nn.sigmoid_cross_entropy_with_logits(labels=labels, logits=logits), sample_weight)



def precision_at_k_user(sess, model, query_pos_test, query_pos_train, query_url_feature, k=5):
    p_list = []
    query_test_list = sorted(query_pos_test.keys())
    for query in query_test_list:
        pos_set = set(query_pos_test[query])
        pred_list = list(set(query_url_feature[query].keys()) - set(query_pos_train.get(query, [])))
        if len(pred_list) < k:
            continue

        pred_list_feature = [query_url_feature[query][url] for url in pred_list]
        pred_list_feature = np.asarray(pred_list_feature)
        pred_list_score = sess.run(model.pred_score, feed_dict={model.pred_data: pred_list_feature})
        pred_url_score = zip(pred_list, pred_list_score)
        pred_url_score = sorted(pred_url_score, key=lambda x: x[1], reverse=True)

        num = 0.0
        for i in range(0, k):
            (url, score) = pred_url_score[i]
            if url in pos_set:
                num += 1.0
        num /= (k * 1.0)

        p_list.append(num)

    return p_list

