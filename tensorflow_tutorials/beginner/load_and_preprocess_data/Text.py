from __future__ import absolute_import, division, print_function, unicode_literals

import tensorflow as tf
print('tf.__version__ =', tf.__version__)

import tensorflow_datasets as tfds
import os

from tensorflow.compat.v1.keras.backend import set_session
config = tf.compat.v1.ConfigProto()
config.gpu_options.allow_growth = True  # dynamically grow the memory used on the GPU
config.log_device_placement = True  # to log device placement (on which device the operation ran)
sess = tf.compat.v1.Session(config=config)
set_session(sess)

diretory_url = 'https://storage.googleapis.com/download.tensorflow.org/data/illiad/'
file_names = ['cowper.txt', 'derby.txt', 'butler.txt']

for name in file_names:
    text_dir = tf.keras.utils.get_file(name, origin=diretory_url+name)

parent_dir = os.path.dirname(text_dir)
print('parent_dir =', parent_dir)

def labeler(example, index):
    return example, tf.cast(index, tf.int64)

labeled_data_sets = []
for i, file_name in enumerate(file_names):
    lines_dataset = tf.data.TextLineDataset(os.path.join(parent_dir, file_name))
    labeled_data_set = lines_dataset.map(lambda ex: labeler(ex, i))
    labeled_data_sets.append(labeled_data_set)

buffer_size = 50000
batch_size = 64
take_size = 5000

all_labeled_data = labeled_data_sets[0]
for labeled_data_set in labeled_data_sets[1:]:
    all_labeled_data = all_labeled_data.concatenate(labeled_data_set)

all_labeled_data = all_labeled_data.shuffle(
    buffer_size, reshuffle_each_iteration=False
)

print('type(all_labeled_data) =', type(all_labeled_data))
print('all_labeled_data.take(1) =', all_labeled_data.take(1))
for ex in all_labeled_data.take(5):
    print(ex)


tokenizer = tfds.features.text.Tokenizer()

vocabulary_set = set()
for text_tensor, _ in all_labeled_data:
    some_tokens = tokenizer.tokenize(text_tensor.numpy())
    vocabulary_set.update(some_tokens)

vocab_size = len(vocabulary_set)
print('len(vocabulary_set) =', len(vocabulary_set))
print('next(iter(vocabulary_set) =', next(iter(vocabulary_set))) # peek one element

encoder = tfds.features.text.TokenTextEncoder(vocabulary_set)
example_text = next(iter(all_labeled_data))[0].numpy()
print('example_text =', example_text)
encoded_example = encoder.encode(example_text)
print('encoded_example =', encoded_example)

def encode(text_tensor, label):
    encoded_text = encoder.encode(text_tensor.numpy())
    return encoded_text, label

def encode_map_fn(text, label):
    return tf.py_function(encode, inp=[text, label], Tout=(tf.int64, tf.int64))

all_encoded_data = all_labeled_data.map(encode_map_fn)

train_data = all_encoded_data.skip(take_size).shuffle(buffer_size)
train_data = train_data.padded_batch(batch_size, padded_shapes=([-1], []))
test_data = all_encoded_data.take(take_size)
test_data = test_data.padded_batch(batch_size, padded_shapes=([-1], []))

sample_text, sample_labels = next(iter(test_data))
print('sample_text[0] =', sample_text[0])
print('sample_labels[0] =', sample_labels[0])
vocab_size += 1

model = tf.keras.Sequential()
model.add(tf.keras.layers.Embedding(vocab_size, 64))
model.add(tf.keras.layers.Bidirectional(tf.keras.layers.LSTM(64)))
for units in [64, 64]:
    model.add(tf.keras.layers.Dense(units, activation='relu'))

model.add(tf.keras.layers.Dense(3, activation='softmax'))
model.summary()

model.compile(
    optimizer='adam',
    loss='sparse_categorical_crossentropy',
    metrics=['accuracy']
)
model.fit(train_data, epochs=3, validation_data=test_data)

eval_loss, eval_acc = model.evaluate(test_data)
print('\neval loss: {:.3f}, eval accuracy: {:.3f}'.format(eval_loss, eval_acc))
