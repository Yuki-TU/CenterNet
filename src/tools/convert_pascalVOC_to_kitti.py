import xml.etree.ElementTree as ET
import os

DATA_PATH = '../../data/pano/'

ann_dir = DATA_PATH + 'Annotations/'
image_set_path = DATA_PATH + 'Image_set/'
results_dir = os.path.join(DATA_PATH, 'Annotations_kitti')
splits = ['train', 'val']

if not os.path.exists(results_dir):
    os.mkdir(results_dir)

for split in splits:
    image_set = open(image_set_path + '{}.txt'.format(split), 'r')
    for img_id in image_set:
        img_id = img_id.strip()
        #img_id = img_id.lstrip('00')   #先頭の'00'を取り除く
        ann_path = ann_dir + '{}.xml'.format(img_id)
        out_path = os.path.join(results_dir, '{}.txt'.format(img_id))
        tree = ET.parse(ann_path)
        root = tree.getroot()
        f = open(out_path, 'w')
        for tmp in root.iter('object'):
            class_name = tmp.find('name').text
            xmlbox = tmp.find('bndbox')
            f.write('{} 0.0 0 0.00 {:.2f} {:.2f} {:.2f} {:.2f} 0.00 0.00 0.00 0.00 0.00 0.00 0.00'.format(class_name,
                                                                                                          float(
                                                                                                              xmlbox.find(
                                                                                                                  'xmin').text),
                                                                                                          float(
                                                                                                              xmlbox.find(
                                                                                                                  'ymin').text),
                                                                                                          float(
                                                                                                              xmlbox.find(
                                                                                                                  'xmax').text),
                                                                                                          float(
                                                                                                              xmlbox.find(
                                                                                                                  'ymax').text)))
            f.write('\n')
        f.close()
        print('{}.txt'.format(img_id))
