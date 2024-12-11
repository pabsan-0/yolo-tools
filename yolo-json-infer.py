#! /usr/bin/env python3

from ultralytics import YOLO
import json
import argparse
import pprint
import sys
import os
import tqdm


ARGS = None
WDIR = f"/tmp/pabsan-0/{sys.argv[0].split('/')[-1]}/"


class CustomYoloInferrer:

    def __init__(self):

        self.src_json = self.__parse_json()

        (
            self.images,
            self.images_by_id,
            self.images_by_fname,
        ) = self.__digest_images()

        self.cls_remap_dict = self.__parse_cls_remapping()
        self.__save_new_json()

    def __parse_json(self):
        """Loads json as attribute"""
        with open(ARGS.labels, "r") as file:
            src_json = json.load(file)

        return src_json

    def __digest_images(self):
        """Builds a fname-indexed dict to get image ids"""
        images = []  # Will receive existing image label {}-fields
        images_by_id = {}  # Will receive path->id mapping
        images_by_fname = {}  # Will receive path->id mapping

        for image in self.src_json["images"]:

            fname = os.path.join(ARGS.parent_dir, image["file_name"])

            if os.path.exists(fname):
                images.append(image)
                images_by_id[image["id"]] = image
                images_by_fname[fname] = image
            else:
                print("File %s not found." % fname, file=sys.stderr)

        return images, images_by_id, images_by_fname

    def __parse_cls_remapping(self):
        """Builds a remap dict to convert class ids post-inference"""
        cls_remap_dict = {}
        if not ARGS.remap:
            return cls_remap_dict

        try:
            for pair in ARGS.remap.split(","):
                model_output, dumped_label = map(int, pair.split(":"))
                cls_remap_dict[model_output] = dumped_label
                print(
                    f"INFO: Remapping model's {model_output} to {dumped_label} in labelfile."
                )
        except ValueError as e:
            print(
                f"\nERROR: Invalid remapping specifier {ARGS.remap=}. Expected pairwise format '1:2,3:4'."
            )
            raise e

        return cls_remap_dict

    def __save_new_json(self):
        """Save JSON file pruning the non-existing images and their labels"""

        canvas = self.src_json.copy()

        canvas["images"] = self.images

        annotations = []
        for annot in self.src_json["annotations"]:
            if self.images_by_id.get(annot["image_id"], False) is not False:
                annot["bbox"] = self.xywh_to_xyxy(annot["bbox"])
                annotations.append(annot)

        canvas["annotations"] = annotations

        fname_dst = WDIR + "labels.json"
        os.makedirs(os.path.dirname(os.path.abspath(fname_dst)), exist_ok=True)
        with open(fname_dst, "w") as file:
            json.dump(canvas, file, indent=1)

    def path_to_id(self, fname):
        """Fetches the id of an image given its filename"""
        # TODO
        return self.images_by_fname[os.path.join(ARGS.parent_dir, fname)]["id"]

    def cls_remap(self, cls):
        """Return either remap field or original value"""
        return self.cls_remap_dict.get(cls, cls)

    def xywh_to_xyxy(self, bbox):
        """Label conversion from XYWH to XYXY (mscoco)"""
        x, y, w, h = bbox
        return [x, y, w + x, h + y]

    def yolo11_inference(self):
        """Infer all images from iterable attribute"""

        model = YOLO(ARGS.model)

        res_json = []
        for img in tqdm.tqdm(list(self.images_by_fname.keys())):

            # Need to go one image at a time to avoid RAM-clogging
            res = model.predict(img)

            # Following docs, there is apparently one results obj per detetection,
            # but this is not what we've saw when debugging, may depend on model
            # / version. Multiple results are coming as multidim tensors, but res
            # is always an iterable. Hence, we just get the first element and if
            # there is more than one, warn user to review this.
            assert len(res) == 1, "Messed up dimensions when parsing results."
            res = res[0]

            # Figure how many detections are there based on tensor lenght
            n_detections = len(res.boxes.cls.tolist())

            # Fetch each individually and append as json
            for ii in range(n_detections):
                res_json.append(
                    {
                        "image_id": self.path_to_id(res.path),
                        "category_id": self.cls_remap(int(res.boxes.cls.tolist()[ii])),
                        "bbox": [int(jj) for jj in res.boxes.xyxy.tolist()[ii]],
                        "score": res.boxes.conf.tolist()[ii],
                    }
                )

        fname_dst = WDIR + "results.json"
        with open(fname_dst, "w") as file:
            json.dump(res_json, file, indent=1)


if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description=(
            "YOLO-infers annotated JSON images and outputs filtered "
            "annotations and results file. Beware of labelling format. "
        )
    )
    parser.add_argument("labels", type=str, help="MS-COCO like .json label file")
    parser.add_argument("model", type=str, help="Yolo .pt trained model")
    parser.add_argument(
        "-r",
        "--remap",
        type=str,
        help=(
            "Remapping specifier to convert inferred object's IDs, "
            "bridging possibly different ids in the inferred data labels "
            "and a pre-trained model. The following specifier records "
            "models' outputs 1 and 2 as 0 and 1: '1:0,2:1'"
        ),
    )
    parser.add_argument(
        "-d",
        "--parent-dir",
        default="",
        type=str,
        help=(
            "Parent dir to the image paths in labels.json. "
            "If not provided, assume fnames relative to json file"
        ),
    )
    ARGS = parser.parse_args()

    # If parent dir is not provided, use JSON file's path
    if not ARGS.parent_dir:
        ARGS.parent_dir = os.path.dirname(os.path.abspath(ARGS.labels))

    cyi = CustomYoloInferrer()
    cyi.yolo11_inference()
