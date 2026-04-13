# -*- coding: utf-8 -*-
import xml.etree.ElementTree as ET
import os
from os import getcwd
import shutil

sets = ['train', 'val','test' ]
classes = ["stand","listen", "bow", "distraction","hands-up"]   # 改成自己的类别

abs_path = os.getcwd()
print(abs_path)

def convert(size, box):
    # print(size,"sffsdfsdf")
    dw = 1. / (size[0])
    dh = 1. / (size[1])
    x = (box[0] + box[1]) / 2.0 - 1
    y = (box[2] + box[3]) / 2.0 - 1
    w = box[1] - box[0]
    h = box[3] - box[2]
    x = x * dw
    w = w * dw
    y = y * dh
    h = h * dh
    return x, y, w, h

def convert_annotation(image_id):

    in_file = open(r'C:\Users\he\Desktop\VOCdevkit\VOC2007\Annotations/%s.xml' % (image_id), encoding='UTF-8')
    out_file = open(r'C:\Users\he\Desktop\VOCdevkit\VOC2007\labels/%s.txt' % (image_id), 'w')
    tree = ET.parse(in_file)
    root = tree.getroot()
    size = root.find('size')
    w = int(size.find('width').text)
    h = int(size.find('height').text)
    for obj in root.iter('object'):
        difficult = obj.find('difficult').text
        # difficult = obj.find('Difficult').text
        cls = obj.find('name').text
        if cls not in classes or int(difficult) == 1:
            continue
        cls_id = classes.index(cls)
        xmlbox = obj.find('bndbox')
        b = (float(xmlbox.find('xmin').text), float(xmlbox.find('xmax').text), float(xmlbox.find('ymin').text),
             float(xmlbox.find('ymax').text))
        b1, b2, b3, b4 = b
        # 标注越界修正
        if b2 > w:
            b2 = w
        if b4 > h:
            b4 = h
        b = (b1, b2, b3, b4)
        bb = convert((w, h), b)
        out_file.write(str(cls_id) + " " + " ".join([str(a) for a in bb]) + '\n')
wd = getcwd()

# 创建images和labels目录
labels_path = os.path.join(abs_path + '\\labels')
images_path = os.path.join(abs_path + '\\images')
labels_train_path = os.path.join(labels_path + '\\train')
labels_val_path = os.path.join(labels_path + '\\val')
images_train_path = os.path.join(images_path + '\\train')
images_val_path = os.path.join(images_path + '\\val')
if not os.path.exists(labels_path):
    os.makedirs(labels_path)
if not os.path.exists(images_path):
    os.makedirs(images_path)
if not os.path.exists(labels_train_path ):
    os.makedirs(labels_train_path)
if not os.path.exists(labels_val_path ):
    os.makedirs(labels_val_path)
if not os.path.exists(images_train_path ):
    os.makedirs(images_train_path)
if not os.path.exists(images_val_path ):
    os.makedirs(images_val_path)


for image_set in sets:
    image_ids = open(abs_path + '/ImageSets/Main/%s.txt' % (image_set)).read().strip().split()

    #   image_ids = open(abs_path + '/ImageSets/Main/%s.txt' % (image_set)).read().strip().split()

    list_file = open(abs_path + '/%s.txt' % (image_set), 'w')
    for image_id in image_ids:
        list_file.write(abs_path + '\\JPEGImages\\%s.jpg\n' % (image_id))
        # print(image_id,"tupian")
        convert_annotation(image_id)
    list_file.close()

for line in open('train.txt','r'):
    line = line.rstrip('\n')
    shutil.copy(line,images_train_path)

for line in open('val.txt','r'):
    line = line.rstrip('\n')
    shutil.copy(line,images_val_path)

for line in open(abs_path + '\\ImageSets\Main\\val.txt','r'):
    # print(line)
    line = line.rstrip('\n')
    shutil.move(labels_path + '\\' + line+'.txt',labels_val_path)

for line in open(abs_path + '\\ImageSets\Main\\train.txt','r'):
    # print(line)
    line = line.rstrip('\n')
    shutil.move(labels_path + '\\' + line+'.txt',labels_train_path)

