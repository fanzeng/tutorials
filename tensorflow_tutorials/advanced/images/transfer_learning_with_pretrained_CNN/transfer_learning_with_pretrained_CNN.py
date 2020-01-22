from __future__ import absolute_import, division, print_function, unicode_literals
import os
import numpy as np
import matplotlib.pyplot as plt

import tensorflow as tf
keras = tf.keras

import tensorflow_datasets as tfds

from tensorflow.compat.v1.keras.backend import set_session
config = tf.compat.v1.ConfigProto()
config.gpu_options.allow_growth = True  # dynamically grow the memory used on the GPU
config.log_device_placement = True  # to log device placement (on which device the operation ran)
sess = tf.compat.v1.Session(config=config)
set_session(sess)


tfds.disable_progress_bar()

split_weights = (8, 1, 1)
splits = tfds.Split.TRAIN.subsplit(weighted=split_weights)
(raw_train, raw_validation, raw_test), metadata = tfds.load(
    'cats_vs_dogs', split=list(splits),
    with_info=True, as_supervised=True
)

print('raw_train =', raw_train)
print('raw_validation =', raw_validation)
print('raw_test =', raw_test)

for image, label in raw_train.take(2):
    plt.figure()
    plt.imshow(image)
    plt.title(metadata.features['label'].int2str(label))
    # plt.show(block=False)


img_size = 160

def format_example(image, label):
    image = tf.cast(image, tf.float32)
    image = (image/127.5)-1
    image = tf.image.resize(image, (img_size, img_size))
    return image, label

train = raw_train.map(format_example)
validation = raw_validation.map(format_example)
test = raw_test.map(format_example)

batch_size = 32
shuffle_buffer_size = 1000

train_batches = train.shuffle(shuffle_buffer_size).batch(batch_size)
validation_batches = validation.batch(batch_size)
test_batches = test.batch(batch_size)

for image_batch, label_batch in train_batches.take(1):
    pass

print('image_batch.shape =', image_batch.shape)

image_shape = (img_size, img_size, 3)
base_model = keras.applications.MobileNetV2(
    input_shape=image_shape,
    include_top=False,
    weights='imagenet'
)

feature_batch = base_model(image_batch)
print('feature_batch.shape =', feature_batch.shape)

base_model.trainable = False
base_model.summary()

global_average_layer = keras.layers.GlobalAveragePooling2D()
feature_batch_average = global_average_layer(feature_batch)
print('feature_batch_average.shape =', feature_batch_average.shape)

prediction_layer = keras.layers.Dense(1)
prediction_batch = prediction_layer(feature_batch_average)
print('prediction_batch.shape =', prediction_batch.shape)

model = keras.Sequential([
    base_model,
    global_average_layer,
    prediction_layer
])

base_learning_rate = 0.0001

model.compile(
    optimizer=keras.optimizers.RMSprop(lr=base_learning_rate),
    loss=keras.losses.BinaryCrossentropy(from_logits=True),
    metrics=['accuracy']
)

model.summary()
print('len(model.trainable_variables =', len(model.trainable_variables))

num_train, num_val, num_test = (
    metadata.splits['train'].num_examples*weight/10
    for weight in split_weights
)

initial_epochs = 10
steps_per_epoch = round(num_train) // batch_size
validation_steps = 20

loss0, accuracy0 = model.evaluate(validation_batches, steps=validation_steps)
print('initial loss: {:.2f}'.format(loss0))
print('initial accuracy: {:.2f}'.format(accuracy0))

history = model.fit(
    train_batches,
    epochs=initial_epochs,
    validation_data=validation_batches
)

acc = history.history['accuracy']
val_acc = history.history['val_accuracy']

loss = history.history['loss']
val_loss = history.history['val_loss']

plt.figure(figsize=(8, 8))
plt.subplot(2, 1, 1)
plt.plot(acc, label='Training Accuracy')
plt.plot(val_acc, label='Validation Accuracy')
plt.legend(loc='lower right')
plt.ylabel('Accuracy')
plt.ylim([min(plt.ylim()),1])
plt.title('Training and Validation Accuracy')

plt.subplot(2, 1, 2)
plt.plot(loss, label='Training Loss')
plt.plot(val_loss, label='Validation Loss')
plt.legend(loc='upper right')
plt.ylabel('Cross Entropy')
plt.ylim([0,1.0])
plt.title('Training and Validation Loss')
plt.xlabel('epoch')
plt.show(block=False)

base_model.trainable = True
print('Number of layers in base model: ', len(base_model.layers))

fine_tune_at = 100
for layer in base_model.layers[:fine_tune_at]:
    layer.trainable = False

model.compile(
    loss=keras.losses.BinaryCrossentropy(from_logits=True),
    optimizer=keras.optimizers.RMSprop(lr=base_learning_rate/10),
    metrics=['accuracy']
)

model.summary()
print('len(model.trainable_variables) =', len(model.trainable_variables))

fine_tune_epochs = 10
total_epochs = initial_epochs + fine_tune_epochs

history_fine = model.fit(
    train_batches,
    epochs=total_epochs,
    initial_epoch=history.epoch[-1],
    validation_data=validation_batches
)

acc += history_fine.history['accuracy']
val_acc += history_fine.history['val_accuracy']

loss += history_fine.history['loss']
val_loss += history_fine.history['val_loss']
plt.figure(figsize=(8, 8))
plt.subplot(2, 1, 1)
plt.plot(acc, label='Training Accuracy')
plt.plot(val_acc, label='Validation Accuracy')
plt.ylim([0.8, 1])
plt.plot([initial_epochs-1,initial_epochs-1],
          plt.ylim(), label='Start Fine Tuning')
plt.legend(loc='lower right')
plt.title('Training and Validation Accuracy')

plt.subplot(2, 1, 2)
plt.plot(loss, label='Training Loss')
plt.plot(val_loss, label='Validation Loss')
plt.ylim([0, 1.0])
plt.plot([initial_epochs-1,initial_epochs-1],
         plt.ylim(), label='Start Fine Tuning')
plt.legend(loc='upper right')
plt.title('Training and Validation Loss')
plt.xlabel('epoch')
plt.show(block=False)
plt.close('all')