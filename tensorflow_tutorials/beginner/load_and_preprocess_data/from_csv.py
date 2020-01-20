from __future__ import absolute_import, division, print_function, unicode_literals
import functools

import numpy as np
import tensorflow as tf

train_data_url = "https://storage.googleapis.com/tf-datasets/titanic/train.csv"
test_data_url = "https://storage.googleapis.com/tf-datasets/titanic/eval.csv"

train_file_path = tf.keras.utils.get_file('train.csv', train_data_url)
test_file_path = tf.keras.utils.get_file('eval.csv', test_data_url)

np.set_printoptions(precision=3, suppress=True)

label_column = 'survived'

def get_dataset(file_path, **kwargs):
    return tf.data.experimental.make_csv_dataset(
        file_path,
        batch_size=5,
        label_name=label_column,
        na_value='?',
        num_epochs=1,
        ignore_errors=True,
        **kwargs
    )

raw_train_data = get_dataset(train_file_path)
raw_test_data = get_dataset(test_file_path)

def show_batch(dataset):
    print('show_batch: ')
    for batch, label in dataset.take(1):
        for key, value in batch.items():
            print('{:20s}: {}'.format(key, value.numpy()))


show_batch(raw_train_data)

print('-'*80)
csv_columns = ['survived', 'sex', 'age', 'n_siblings_spouses', 'parch', 'fare', 'class', 'deck', 'embark_town', 'alone']
temp_dataset = get_dataset(train_file_path, column_names=csv_columns)
show_batch(temp_dataset)

print('-'*80)
select_columns = ['survived', 'age', 'n_siblings_spouses', 'class', 'deck', 'alone']
temp_dataset = get_dataset(train_file_path, select_columns=select_columns)
show_batch(temp_dataset)

print('-'*80)
select_columns = ['survived', 'age', 'n_siblings_spouses', 'parch', 'fare']
defaults = [0, 0.0, 0.0, 0.0, 0.0]
temp_dataset = get_dataset(
    train_file_path,
    select_columns=select_columns,
    column_defaults=defaults)
show_batch(temp_dataset)

print('-'*80)
example_batch, labels_batch = next(iter(temp_dataset))
def pack(features, label):
    return tf.stack(list(features.values()), axis=-1), label

packed_dataset = temp_dataset.map(pack)
for features, labels in packed_dataset.take(1):
    print(features.numpy())
    print()
    print(labels.numpy())

print('-'*80)
print('PackNumericFeatures')
class PackNumericFeatures(object):
    def __init__(self, names):
        self.names = names

    def __call__(self, features, labels):
        numeric_features = [features.pop(name) for name in self.names]
        numeric_features = [tf.cast(feat, tf.float32) for feat in numeric_features]
        numeric_features = tf.stack(numeric_features, axis=-1)
        features['numeric'] = numeric_features
        return features, labels

numeric_features = ['age', 'n_siblings_spouses', 'parch', 'fare']
print('numeric_features =', numeric_features)

packed_train_data = raw_train_data.map(PackNumericFeatures(numeric_features))

packed_test_data = raw_test_data.map(PackNumericFeatures(numeric_features))

show_batch(packed_train_data)
example_batch, labels_batch = next(iter(packed_train_data))

print('-'*80)
import pandas as pd
desc = pd.read_csv(train_file_path)[numeric_features].describe()
print('desc =', desc)

print('-'*80)
mean = np.array(desc.T['mean'])
std = np.array(desc.T['std'])


def normalize_numeric_data(data, mean, std):
    return (data-mean)/std

normalizer = functools.partial(normalize_numeric_data, mean=mean, std=std)
numeric_column = tf.feature_column.numeric_column(
    'numeric', normalizer_fn=normalizer, shape=[len(numeric_features)]
)
print('numeric_column =', numeric_column)
numeric_columns = [numeric_column]
print('numeric_columns =', numeric_columns)

numeric_layer = tf.keras.layers.DenseFeatures(numeric_columns)

print('numeric_layer(example_batch).numpy() =', numeric_layer(example_batch).numpy())
print('mean =', mean)
print('std =', std)
print("example_batch['numeric'] =", example_batch['numeric'])

print('-'*80)
categories = {
    'sex': ['male', 'female'],
    'class' : ['First', 'Second', 'Third'],
    'deck' : ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J'],
    'embark_town' : ['Cherbourg', 'Southhampton', 'Queenstown'],
    'alone' : ['y', 'n']
}
categorical_columns = []
for feature, vocab in categories.items():
    cat_col = tf.feature_column.categorical_column_with_vocabulary_list(
        key=feature, vocabulary_list=vocab
    )
    categorical_columns.append(tf.feature_column.indicator_column(cat_col))
print('categorical_columns =', categorical_columns)

categorical_layer = tf.keras.layers.DenseFeatures(categorical_columns)
print(
    'categorical_layer(example_batch).numpy() =',
    categorical_layer(example_batch).numpy(),
    'shape =',
    categorical_layer(example_batch).numpy().shape
)

preprocessing_layer = tf.keras.layers.DenseFeatures(categorical_columns + numeric_columns)
print(
    'preprocessing_layer(example_batch).numpy() =',
    preprocessing_layer(example_batch).numpy(),
    'shape =',
    preprocessing_layer(example_batch).numpy().shape
)

model = tf.keras.Sequential([
    preprocessing_layer,
    tf.keras.layers.Dense(128, activation='relu'),
    tf.keras.layers.Dense(128, activation='relu'),
    tf.keras.layers.Dense(1, activation='sigmoid'),
])

model.compile(
    loss='binary_crossentropy',
    optimizer='adam',
    metrics=['accuracy']
)

train_data = packed_train_data.shuffle(500)
test_data = packed_test_data
model.fit(train_data, epochs=20)
test_loss, test_accuracy = model.evaluate(test_data)
print('\n\nTest Loss {}, Test Accuracy {}'.format(test_loss, test_accuracy))

predictions = model.predict(test_data)

for prediction, survived in zip(predictions[:10], list(test_data)[0][1][:10]):
    print("Predicted survival: {:.2%}".format(prediction[0]),
        " | Actual outcome: ",
        ("survived" if bool(survived) else "not survived")
    )
