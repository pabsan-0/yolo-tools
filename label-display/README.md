# Yolo video assembler

Tools for YOLO image labelling.

- `labeller.py`: Copies source images drawing bboxes onto them. Renames images to zero-padded increasingly big integers.
- `linker.py`: Creates links to source original images. Renames links to zero-padded increasingly big integers.
- `videomaker.sh`: Gst pipeline to gather all images in directory (cwd) to a single mp4 file. If used on the output of the above scripts, the videos will have the same frames, yet only one of them drawn detections. Then, you may use:
    - `mixer.sh`: Mixes two mp4 videos into one, side by side.
    - `mixer-transp.sh`: Mixes two mp4 videos into one, one on top of the other.\

```
mkdir out
python3 labeller.py  # <- hardcode paths in script
```
```
mkdir links
python3 linker.py  # <- hardcode paths in script
```
```
cd links
bash ../videomaker.sh
cd ..
mv out.mp4 out_originals.mp4

cd out
bash ../videomaker.sh
cd ..
mv out.mp4 out_labelled.mp4

bash mixer.sh
bash mixer-labelled.sh
```

