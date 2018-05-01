import base64
import json
import os.path
import sys
import makeTestUIXml
from lxml import etree


PY2 = sys.version_info[0] == 2


class LabelFileError(Exception):
    pass


class LabelFile(object):

    suffix = '.json'

    def __init__(self, filename=None):
        self.shapes = ()
        self.imagePath = None
        self.imageData = None
        if filename is not None:
            self.load(filename)
        self.filename = filename

    def load(self, filename):
        keys = ['imageData', 'imagePath', 'lineColor', 'fillColor', 'shapes']
        try:
            with open(filename, 'rb' if PY2 else 'r') as f:
                data = json.load(f)
            if data['imageData'] is not None:
                imageData = base64.b64decode(data['imageData'])
            else:
                # relative path from label file to relative path from cwd
                imagePath = os.path.join(os.path.dirname(filename),
                                         data['imagePath'])
                with open(imagePath, 'rb') as f:
                    imageData = f.read()
            imagePath = data['imagePath']
            lineColor = data['lineColor']
            fillColor = data['fillColor']
            shapes = (
                (s['label'], s['points'], s['line_color'], s['fill_color'])
                for s in data['shapes']
            )
        except Exception as e:
            raise LabelFileError(e)

        otherData = {}
        for key, value in data.items():
            if key not in keys:
                otherData[key] = value

        # Only replace data after everything is loaded.
        self.shapes = shapes
        self.imagePath = imagePath
        self.imageData = imageData
        self.lineColor = lineColor
        self.fillColor = fillColor
        self.filename = filename
        self.otherData = otherData

    def save(self, filename, shapes, imagePath, imageData=None,imgHeight=None,imgWith=None,
             lineColor=None, fillColor=None, otherData=None):
        if imageData is not None:
            imageData = base64.b64encode(imageData).decode('utf-8')
        if otherData is None:
            otherData = {}
        data = dict(
            shapes=shapes,
            lineColor=lineColor,
            fillColor=fillColor,
            imagePath=imagePath,
            imageData=imageData,
        )
        for key, value in otherData.items():
            data[key] = value
        try:
            with open(filename, 'wb' if PY2 else 'w') as f:
                json.dump(data, f, ensure_ascii=True, indent=2)
            self.filename = filename

            with open(os.path.splitext(filename)[0]+".txt", 'wb' if PY2 else 'w') as f2txt:
                for shape in data['shapes']:
                    point = []
                    for p in shape['points']:
                        point.append(p[0])
                        point.append(p[1])
                    f2txt.writelines('points: '+str(point)+' label: '+str(shape['label']))
                    f2txt.writelines("\n")
                f2txt.writelines("imageData.shape = h{},w{}".format(imgHeight,imgWith))

            Save_TestUIXml_dir = os.path.dirname(filename)
            Xmldata = makeTestUIXml.head_info(imagePath.split('.')[0], Save_TestUIXml_dir,
                                              imgHeight, imgWith, im_depth=3);
            for shape in data['shapes']:
                point = []
                for p in shape['points']:
                    point.append(p[0])
                    point.append(p[1])
                makeTestUIXml.object_info(Xmldata, objName=shape['label'],pointXY = point)
            # 8 write xml
            dataxml = etree.tostring(Xmldata, pretty_print=True, encoding="UTF-8", method="xml",
                                     xml_declaration=True, standalone=None)
            with open(os.path.join(Save_TestUIXml_dir, (imagePath.split('.')[0] + '.xml')), 'wb') as fp:
                fp.write(dataxml)



        except Exception as e:
            raise LabelFileError(e)

    @staticmethod
    def isLabelFile(filename):
        return os.path.splitext(filename)[1].lower() == LabelFile.suffix
