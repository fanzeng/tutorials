from __future__ import absolute_import, division, print_function, unicode_literals

import numpy as np
import tensorflow as tf
mnist_url = 'https://storage.googleapis.com/tensorflow/tf-keras-datasets/mnist.npz'

mnist_path = tf.keras.utils.get_file('mnist.npz', mnist_url)
with np.load(mnist_path) as data:
    train_examples = data['x_train']
    train_labels = data['y_train']
    test_examples = data['x_test']
    test_labels = data['y_test']

train_dataset = tf.data.Dataset.from_tensor_slices((train_examples, train_labels))
test_dataset = tf.data.Dataset.from_tensor_slices((test_examples, test_labels))

batch_size = 64
shuffle_buffer_size = 100

train_dataset = train_dataset.shuffle(shuffle_buffer_size).batch(batch_size)
test_dataset = test_dataset.batch(batch_size)

model = tf.keras.Sequential([
    tf.keras.layers.Flatten(input_shape=(28, 28)),
    tf.keras.layers.Dense(128, activation='relu'),
    tf.keras.layers.Dense(10, activation='softmax')
])

model.compile(
    optimizer=tf.keras.optimizers.RMSprop(),
    loss=tf.keras.losses.SparseCategoricalCrossentropy(),
    metrics=[tf.keras.metrics.SparseCategoricalAccuracy()]
)

model.fit(train_dataset, epochs=10)
model.evaluate(test_dataset)
