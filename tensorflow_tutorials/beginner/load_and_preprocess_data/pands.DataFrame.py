from __future__ import absolute_import, division, print_function, unicode_literals

import pandas as pd
import tensorflow as tf

csv_file = tf.keras.utils.get_file('heart.csv', 'https://storage.googleapis.com/applied-dl/heart.csv')
df = pd.read_csv(csv_file)
print('type(df) =', type(df))
print('df.head() =', df.head())
print('df.dtypes() =', df.dtypes)
df['thal'] = pd.Categorical(df['thal'])
df['thal'] = df.thal.cat.codes

print('-'*80)
print('df.head() =', df.head())
print('df.dtypes() =', df.dtypes)

print('-'*80)
target = df.pop('target') # df has been changed from now on to not contain target
print('df.head() =', df.head())
dataset = tf.data.Dataset.from_tensor_slices((df.values, target.values))

for feat, targ in dataset.take(5):
  print ('Features: {}, Target: {}'.format(feat, targ))

print("tf.constant(df['thal']) =", tf.constant(df['thal']))
print('len(df) =', len(df))
train_dataset = dataset.shuffle(len(df)).batch(1)

def get_compiled_model():
  model = tf.keras.Sequential([
    tf.keras.layers.Dense(10, activation='relu'),
    tf.keras.layers.Dense(10, activation='relu'),
    tf.keras.layers.Dense(1, activation='sigmoid')
  ])

  model.compile(optimizer='adam',
                loss='binary_crossentropy',
                metrics=['accuracy'])
  return model

model = get_compiled_model()
model.fit(train_dataset, epochs=15)

print('-'*80)
inputs = {key: tf.keras.layers.Input(shape=(), name=key) for key in df.keys()}
print('inputs =', inputs)
print('len(inputs) =', len(inputs))
x = tf.stack(list(inputs.values()), axis=-1)
print('inputs.values() =', inputs.values())
print('x =', x)
x = tf.keras.layers.Dense(10, activation='relu')(x)
print('x =', x)
output = tf.keras.layers.Dense(1, activation='sigmoid')(x)
print('output =', output)

model_func = tf.keras.Model(inputs=inputs, outputs=output)

model_func.compile(optimizer='adam',
                   loss='binary_crossentropy',
                   metrics=['accuracy'])

print("df.to_dict('list') =", df.to_dict('list'))
print('type(df.values) =', type(df.values))
print('df.values.shape =', df.values.shape)
print("df.values =", df.values)

dict_slices = tf.data.Dataset.from_tensor_slices((df.to_dict('list'), target.values)).batch(16)
print("printing dict_slices:")
for dict_slice in dict_slices.take(1):
  print('dict_slice =', dict_slice)

model_func.fit(dict_slices, epochs=15)
