from __future__ import absolute_import, division, print_function, unicode_literals
import tensorflow as tf
AUTOTUNE = tf.data.experimental.AUTOTUNE
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import os
import glob

print('tf.__version__ =', tf.__version__)
data_dir = tf.keras.utils.get_file(
    origin='https://storage.googleapis.com/download.tensorflow.org/example_images/flower_photos.tgz',
    fname='flower_photos', untar=True
)

print('type(data_dir) =', type(data_dir))
print('data_dir =', data_dir)
image_count = len(list(glob.glob(os.path.join(data_dir, '*/*.jpg'))))
print('image_count =', image_count)
print("glob.glob(os.path.join(data_dir, '*'))=", glob.glob(os.path.join(data_dir, '*')))

class_names = np.array([
    os.path.basename(item)
    for item in glob.glob(os.path.join(data_dir, '*'))
    if os.path.basename(item) != 'LICENSE.txt'
])

print('class_names =', class_names)
roses = list(glob.glob(os.path.join(data_dir, 'roses/*')))
for image_path in roses[:3]:
    image = Image.open(str(image_path))
    image.show()

# loading using keras.preprocessing

image_generator = tf.keras.preprocessing.image.ImageDataGenerator(rescale=1./255)

batch_size = 32
img_height = 224
img_width = 224
steps_per_epoch = np.ceil(image_count / batch_size)

train_data_gen = image_generator.flow_from_directory(
    directory=str(data_dir),
    batch_size=batch_size,
    shuffle=True,
    target_size=(img_height, img_width),
    classes=class_names.tolist()
)

def show_patch(image_batch, label_batch):
    plt.figure(figsize=(10, 10))
    for n in range(25):
        ax = plt.subplot(5, 5, n+1)
        plt.imshow(image_batch[n])
        plt.title(class_names[label_batch[n]==1][0].title())
        plt.axis('off')

image_batch, label_batch = next(train_data_gen)
show_patch(image_batch, label_batch)

# loading using tf.data
list_ds = tf.data.Dataset.list_files(os.path.join(str(data_dir), '*/*'))
print('type(list_ds) =', type(list_ds))
for f in list_ds.take(5):
    print(f.numpy())

def get_label(file_path):
    parts = tf.strings.split(file_path, os.path.sep)
    return parts[-2] == class_names

def decode_img(img):
    img = tf.image.decode_jpeg(img, channels=3)
    img = tf.image.convert_image_dtype(img, tf.float32)
    return tf.image.resize(img, [img_width, img_height])

def process_path(file_path):
    label = get_label(file_path)
    img = tf.io.read_file(file_path)
    img = decode_img(img)
    return img, label

labeled_ds = list_ds.map(process_path, num_parallel_calls=AUTOTUNE)

for image, label in labeled_ds.take(1):
    print('image shape: ', image.numpy().shape)
    print('label: ', label.numpy())

def prepare_for_training(ds, cache=True, shuffle_buffer_size=1000):
    if cache:
        if isinstance(cache, str):
            ds = ds.cache(cache)
        else:
            ds = ds.cache()

    ds = ds.shuffle(buffer_size=shuffle_buffer_size)

    ds = ds.repeat()
    ds = ds.batch(batch_size)

    ds = ds.prefetch(buffer_size=AUTOTUNE)
    return ds

train_ds = prepare_for_training(labeled_ds)
image_batch, label_batch = next(iter(train_ds))

show_patch(image_batch.numpy(), label_batch.numpy())

import time
default_timeit_steps = 1000

def timeit(ds, steps=default_timeit_steps):
    start = time.time()
    it = iter(ds)
    for i in range(steps):
        batch = next(it)
        if i%10 == 0:
            print('.', end='')
    print()
    end = time.time()
    duration = end - start
    print('{} batches: {} s'.format(steps, duration))
    print('{:0.5f} images/s'.format(batch_size*steps/duration))

timeit(train_data_gen)
timeit(train_ds)

uncached_ds = prepare_for_training(labeled_ds, cache=False)
timeit(uncached_ds)

filecache_ds = prepare_for_training(labeled_ds, cache="./flowers.tfcache")
timeit(filecache_ds)

plt.show(block=False)
plt.close('all')
