#!/usr/bin/env python

import argparse
import json
import os
import os.path as osp
import warnings
import re
import numpy as np
import PIL.Image
import yaml

import utils
def pascal_palette():
  palette = {0 :(  0,   0,   0) ,
             1 :(128,   0,   0) ,
             2 :(  0, 128,   0) ,
             3 :(128, 128,   0) ,
             4 :(  0,   0, 128) ,
             5 :(128,   0, 128) ,
             6 :(  0, 128, 128) ,
             7 :(128, 128, 128) ,
             8 :( 64,   0,   0) ,
             9 :(192,   0,   0) ,
             10 :( 64, 128,   0) ,
             11 :(192, 128,   0) ,
             12:( 64,   0, 128) ,
             13:(192,   0, 128) ,
            14: ( 64, 128, 128) ,
            15: (192, 128, 128) ,
             16:(  0,  64,   0) ,
             17:(128,  64,   0) ,
             18:(  0, 192,   0) ,
             19:(128, 192,   0) ,
            20: (  0,  64, 128) }

  return palette
def extract_classes(segm):
    cl = np.unique(segm)#cls
    n_cl = len(cl)
    return cl, n_cl
def changeToDataset(json_dir,out_dir=None):


    # parser = argparse.ArgumentParser()
    # parser.add_argument('json_file')
    # parser.add_argument('-o', '--out', default=19949)
    # args = parser.parse_args()
    cls_dict = {}
    i=0
    for fileName in os.listdir(json_dir):
        if re.match(".*[.]json$",fileName):
            json_file = osp.join(json_dir,fileName)
            print (json_file)

            if out_dir is None:
                out_dir = osp.join(osp.dirname(json_file), "output")
            # else:
                # print 'Existed out_dir = ',out_dir

            if not osp.exists(out_dir):
                os.mkdir(out_dir)

            out_dir_label = os.path.join(out_dir, 'label')
            if not osp.exists(out_dir_label):
                os.mkdir(out_dir_label)

            out_dir_viz = os.path.join(out_dir,'viz')
            if not osp.exists(out_dir_viz):
                os.mkdir(out_dir_viz)

            # print ("out_dir_label = ",out_dir_label)
            print(osp.join(out_dir, fileName))

            data = json.load(open(json_file))
            img = utils.img_b64_to_array(data['imageData'])
            pred_image, lbl_names,clsDict = utils.labelme_shapes_to_label(img.shape, data['shapes'])
            for k in clsDict:
                if k not in cls_dict.values():
                    cls_dict[i]=k
                    i+=1
            # print(cls_dict)
            # cls_dict = {0: 'background', 1: 'aeroplane', 2: 'bicycle', 3: 'bird', 4: 'boat', 5: 'bottle', 6: 'bus',
            #             7: 'car', 8: 'cat',9: 'chair', 10: 'cow', 11: 'diningtable', 12: 'dog', 13: 'horse', 14: 'motorbike', 15: 'person',
            #             16: 'plant', 17: 'sheep', 18: 'sofa', 19: 'train', 20: 'tv'}
            cl, n_cl = extract_classes(pred_image)
            captions = ['%d: %s' % (cl_index, cls_dict[cl_index]) for cl_index in cl]
            print("captions=",captions)
            # print("max(pred_image)=",np.max(pred_image))
            lbl_viz = utils.draw_label(pred_image, img, captions)

            #New Name
            NewName = fileName.split('.')[0]
            # print (osp.join(out_dir,NewName+ '.png'))
            # PIL.Image.fromarray(img).save(osp.join(out_dir,NewName+ '_img.png'))
            PIL.Image.fromarray(pred_image).save(osp.join(out_dir_label, NewName+ '.png'))
            PIL.Image.fromarray(lbl_viz).save(osp.join(out_dir_viz, NewName+ '_label_viz.png'))

            with open(osp.join(out_dir, 'label_names.txt'), 'w') as f:
                for lbl_name in lbl_names:
                    f.write(lbl_name + '\n')

            # warnings.warn('info.yaml is being replaced by label_names.txt')
            info = dict(label_names=lbl_names)
            with open(osp.join(out_dir, 'info.yaml'), 'w') as f:
                yaml.safe_dump(info, f, default_flow_style=False)

            # print('Saved to: %s' % out_dir)


if __name__ == '__main__':
    json_dir = r'D:\Bill_Test\train'
    # out_dir = r'D:\Bill_Test\train'
    changeToDataset(json_dir)
