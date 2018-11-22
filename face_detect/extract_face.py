#coding:utf-8
from __future__ import print_function
# import sys
import numpy
# sys.path.append('..')
from PIL import Image
import time
import fitz
import re
import os
from face_detect.face_detect_tools import face_detect

def pdf2pic(path, pic_path):
    checkXO = r"/Type(?= */XObject)"       # finds "/Type/XObject"
    checkIM = r"/Subtype(?= */Image)"      # finds "/Subtype/Image"

    t0 = time.clock()
    doc = fitz.open(path)
    imgcount = 0
    lenXREF = doc._getXrefLength()         # number of objects - do not use entry 0!

    # display some file info
    print("file: %s, pages: %s, objects: %s" % (path, len(doc), lenXREF-1))

    for i in range(1, lenXREF):            # scan through all objects
        text = doc._getObjectString(i)     # string defining the object
        isXObject = re.search(checkXO, text)    # tests for XObject
        isImage   = re.search(checkIM, text)    # tests for Image
        if not isXObject or not isImage:   # not an image object if not both True
            continue

        imgcount += 1
        # 根据索引生成图像
        pix = fitz.Pixmap(doc, i)
        # 根据pdf的路径生成图片的名称
        new_name = path.replace('\\', '_') + "_img{}.png".format(imgcount)
        new_name = new_name.replace(':', '')

        pix = fitz.Pixmap(fitz.csRGB, pix)

        print(pix.width, pix.height)

        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        img.show()

        if face_detect.detect(img):
            pix.writePNG(os.path.join(pic_path, new_name))

        pix = None

    t1 = time.clock()
    print("run time", round(t1-t0, 2))
    print("extracted images", imgcount)

if __name__=='__main__':
    # pdf路径
    path = '/Users/hulk/Workspace/PycharmProjects/data_process/face_detect/resume-test-24.pdf'
    pic_path = '/Users/hulk/Downloads/test'
    m = pdf2pic(path, pic_path)

