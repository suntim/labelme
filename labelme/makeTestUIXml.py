#_*_coding:utf-8_*_
#!/usr/bin/env python
#__author__ = 'Alex_XT'

from lxml import etree
import os
import re

def head_info(image_name,save_dir,im_h,im_w,im_depth=1):
    data = etree.Element("annotation")
    data.set('verified', 'no')
    # 1 folder
    interface_folder = etree.SubElement(data, 'folder')
    interface_folder.text = 'testXT'
    # 2 filename
    filename_txt = image_name
    filename = etree.SubElement(data, 'filename')
    filename.text = filename_txt
    # 3 path
    pathNode = etree.SubElement(data, 'path')
    pathNode.text = os.path.join(save_dir , filename_txt + '.jpg')
    # 4 source
    source = etree.SubElement(data, 'source')
    database = etree.SubElement(source, 'database')
    database.text = 'Unknown'
    # 5 img size
    imgsize = etree.SubElement(data, 'size')
    img_width = etree.SubElement(imgsize, 'width')
    img_width.text = str(im_w)
    img_height = etree.SubElement(imgsize, 'height')
    img_height.text = str(im_h)
    img_depth = etree.SubElement(imgsize, 'depth')
    img_depth.text = str(im_depth)
    # 6 segmented
    segmented = etree.SubElement(data, 'segmented')
    segmented.text = '0'
    return data


def object_info(data, objName, pointXY):
    object = etree.SubElement(data, 'object')
    object_name = etree.SubElement(object, 'name')
    object_name.text = objName
    pose = etree.SubElement(object, 'pose')
    pose.text = 'HikPolygonRoiParameter'
    truncated = etree.SubElement(object, 'truncated')
    truncated.text = '0'
    difficult = etree.SubElement(object, 'difficult')
    difficult.text = '0'
    bndbox = etree.SubElement(object, 'bndbox')
    length = int(len(pointXY)/2)
    for i in range(length):
        X = etree.SubElement(bndbox, 'X')
        X.text = str(int(pointXY[2*i]))
        Y = etree.SubElement(bndbox, 'Y')
        Y.text = str(int(pointXY[2*i+1]))



