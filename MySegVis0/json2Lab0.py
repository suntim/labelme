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

from labelme import utils


def changeToDataset(json_dir,out_dir=None):


    # parser = argparse.ArgumentParser()
    # parser.add_argument('json_file')
    # parser.add_argument('-o', '--out', default=None)
    # args = parser.parse_args()


    for fileName in os.listdir(json_dir):
        if re.match(".*[.]json$",fileName):
            json_file = osp.join(json_dir,fileName)
            print json_file

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

            print "out_dir_label = ",out_dir_label

            data = json.load(open(json_file))
            img = utils.img_b64_to_array(data['imageData'])
            lbl, lbl_names = utils.labelme_shapes_to_label(img.shape, data['shapes'])
            #print 0: background 1: sto
            # for l, name in enumerate(lbl_names):
            #     print '%d: %s' % (l, name)
            captions = ['%d: %s' % (l, name) for l, name in enumerate(lbl_names)]
            lbl_viz = utils.draw_label(lbl, img, captions)

            #New Name
            NewName = fileName.split('.')[0]
            print osp.join(out_dir,NewName+ '.png')
            # PIL.Image.fromarray(img).save(osp.join(out_dir,NewName+ '_img.png'))
            PIL.Image.fromarray(lbl).save(osp.join(out_dir_label, NewName+ '.png'))
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
