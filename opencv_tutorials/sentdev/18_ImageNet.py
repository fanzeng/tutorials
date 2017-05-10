import urllib
import urllib2
import socket
import cv2
import numpy as np
import  os

def store_raw_images():
    # neg_images_link = 'http://image-net.org/api/text/imagenet.synset.geturls?wnid=n00523513'
    neg_images_link = 'http://image-net.org/api/text/imagenet.synset.geturls?wnid=n07942152'
    neg_image_urls = urllib2.urlopen(neg_images_link).read().decode()
    if not os.path.exists('neg'):
        os.makedirs('neg')
    pic_num = 903
    for i in neg_image_urls.split('\n'):

        try:
            print(i)
            nameWithPath = 'neg/' + str(pic_num) + '.jpg'
            urllib.urlretrieve(i, nameWithPath)
            img = cv2.imread(nameWithPath, cv2.IMREAD_GRAYSCALE)
            resized_image = cv2.resize(img, (100, 100))
            cv2.imwrite(nameWithPath, resized_image)
            pic_num += 1
        except Exception as e:
            print str(e)

socket.setdefaulttimeout(10)
store_raw_images()
