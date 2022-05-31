# yolo-tools
Automation of tasks I'm tired of doing over and over again + notes


### Custom detection with yolo cfg files
- AlexeyAB changelist for custom object detection: [darknet](https://github.com/AlexeyAB/darknet#how-to-train-to-detect-your-custom-objects)
- These are automated in `makecfg.py`: `python3 makecfg.py -i yolov4.cfg -c 1`
- Check with `diff yolor_p6.cfg yolor_p6_custom.cfg`
