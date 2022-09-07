import os
import sys
import tqdm
import json

import cv2
from rembg.bg import remove
from PIL import Image, ImageFile
from utils import filter_all

# import argparse

ImageFile.LOAD_TRUNCATED_IMAGES = True


def remove_bg(filepath, out_filepath=None):
	image = Image.open(filepath)
	result = remove(image)
	if filepath[-3:] == 'png':
		img = result.convert("RGBA")
	else:
		img = result.convert("RGB")
	if out_filepath:
		img.save(out_filepath)
	else:
		img.save(filepath)


# basedir = "data/83220144"
basedir = "data/Rough/85620019"
video_name = '85620019.mp4'

video = cv2.VideoCapture(os.path.join(basedir, video_name))

os.makedirs(os.path.join(basedir, 'images'), exist_ok=True)
os.makedirs(os.path.join(basedir, 'images_jpg'), exist_ok=True)

print("Starting dir: ", basedir)

print("Step 1: Extracting frames")
i = 0
width, height = None, None
while video.isOpened():
	ret, frame = video.read()
	if not ret:
		break

	if not width and not height:
		width, height = frame.shape[:2]

	_ = cv2.imwrite(os.path.join(basedir, 'images/' + f'r_{i}.png'), frame, )
	_ = cv2.imwrite(os.path.join(basedir, 'images_jpg/' + f'r_{i}.jpg'), frame, )

	i += 1
	if i>100:
		raise Exception("More than 100 frames found. Will break, since needs adjusting")

print("Step 2: Texturizing background [DEACTIVATED]")
# filter_all(os.path.join(basedir, 'images'))

print("Step 3: Removing background")
for j in tqdm.tqdm(range(i)):
	remove_bg(os.path.join(basedir, 'images/' + f'r_{j}.png'))
	# remove_bg(os.path.join(basedir, 'images_filtered/' + f'r_{j}.png'))
	# remove_bg(os.path.join(basedir, 'images_jpg/' + f'r_{j}.jpg'))

print("Step 4: Copying transforms.json")
with open("data/transforms_template.json", 'r') as fin:
	template = json.load(fin)
	template['scale'] = round(template['scale'] * (998 / height), 3)
	# template['w'] = width
	# template['h'] = height

with open(os.path.join(basedir, 'transforms.json'), 'w') as fin:
	json.dump(template, fin, indent=4)

print("DONE")
