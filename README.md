# yolo-tools
Automation of tasks I'm tired of doing over and over again + notes

<br>

## Automate yolo config files  <sup><sub>makecfg.py</sub></sup>

This script automates the craft of cfg files for custom object detection as described in the Darknet repository (last revised for yolov4).
Modded from https://github.com/xaerincl/cfg_yolo to make it more ME-readable.
Feed a default config file for your network and have this script automate parameters for your number of classes.

```
$ python3 makecfg.py -i yolov4.cfg -c 1
```

See also:
- AlexeyAB changelist for custom object detection: [darknet](https://github.com/AlexeyAB/darknet#how-to-train-to-detect-your-custom-objects)
- Verify changes with `diff yolor_p6.cfg yolor_p6_custom.cfg`

<br>  

## COCO validation  <sup><sub>valcoco.py</sub></sup>

A wrapper around `pycocotools` to quickly get your model validated into a sweet MS COCO table.

```
$ valcoco.py groundtruth.json results.json
```

<br>

## Time series label overview <sup><sub>labels_time_series.py</sub></sup>

This script will help you label datasets from videos by plotting a time-series of your labels.
Should items in consecutive frames be nearby, you can easily identify bald, unlabelled spots.
Use with darket labels (one txt file per image). You need to hardcode some lines to properly parse your label filenames.

```
$ vim labels_time_series.py   # Do your hardcoding
***
$ python3 labels_time_series.py
```

                          
<br>

## Count instances by size <sup><sub>coco-count-by-size.py</sub></sup>

This script computes how many items in the a split belong to each
coco size group. You must pass your data in coco json.

```
$ python3 coco-count-by-size.py test.json
```

See also:
- [coco json format](https://cocodataset.org/#format-data)
- [coco object sizes](https://cocodataset.org/#detection-eval)

<br>

## Convert your dataset from YAML to JSON <sup><sub>yaml2json.py</sub></sup>

Converts COCO dataset annotations from yaml-yolo to MSCOCO-JSON format and 
prints them to stdout. This script returns image_ids in string integer format. 
In this context, YAML is yolov5-like flex dataset with Darknet labels i.e. there is a Yaml file pointing to the txt files location.

```
$ yaml2json.py dataset.yaml train > dataset.json
```

<br>

## Video concatenation of your detected images 

Tools for YOLO image labelling. Documented in the [label-display](label-display) directory. Here's an overlook.

- `labeller.py`: Copies source images drawing bboxes onto them.
- `linker.py`: Creates links to source original images. 
- `videomaker.sh`: Gst pipeline to gather all images in directory (cwd) to a single mp4 file. If used on the output of the above scripts, the videos will have the same frames, yet only one of them drawn detections.

<br>
