import json
import xml.etree.ElementTree as ET

DATA_PATH = '../../data/pano/'


def _bbox_to_coco_bbox(bbox):
    return [(bbox[0]), (bbox[1]),
            (bbox[2] - bbox[0]), (bbox[3] - bbox[1])]


cats = ['car', 'cyclist', 'pedestrian']
cat_ids = {cat: i + 1 for i, cat in enumerate(cats)}

cat_info = []
for i, cat in enumerate(cats):
    cat_info.append({'name': cat, 'id': i + 1})

image_set_path = DATA_PATH + 'Image_set/'
ann_dir = DATA_PATH + 'Annotations/'
splits = ['train', 'val']

for split in splits:
    # train, validationを分ける
    ret = {'images': [], 'annotations': [], "categories": cat_info}
    image_set = open(image_set_path + '{}.txt'.format(split), 'r')
    image_to_id = {}
    for line in image_set:
        # train, validationのそれぞれの画像に対して
        if line[-1] == '\n':
            line = line[:-1]
        image_id = int(line)
        image_info = {'file_name': '{}.jpg'.format(line),
                      'id': int(image_id)}
        ret['images'].append(image_info)
        if split == 'test':
            continue
        ann_path = ann_dir + '{}.xml'.format(line)
        tree = ET.parse(ann_path)
        root = tree.getroot()
        for tmp in root.iter('object'):
            # 各アノテーションに対して
            cat_id = cat_ids[tmp.find('name').text]
            xmlbox = tmp.find('bndbox')
            bbox = [float(xmlbox.find('xmin').text), float(xmlbox.find('ymin').text), float(xmlbox.find('xmax').text),
                    float(xmlbox.find('ymax').text)]
            ann = {'image_id': image_id,
                   'id': int(len(ret['annotations']) + 1),
                   'category_id': cat_id,
                   'bbox': _bbox_to_coco_bbox(bbox)}
            ret['annotations'].append(ann)
    print("{}: ".format(split), len(image_set))

    print("# images: ", len(ret['images']))
    print("# annotations: ", len(ret['annotations']))

    out_path = '{}annotations/pano_{}.json'.format(DATA_PATH, split)
    json.dump(ret, open(out_path, 'w'))
