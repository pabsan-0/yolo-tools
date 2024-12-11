#! /usr/bin/env python3

from ultralytics import YOLO
import json
import argparse
import pprint
import sys
import os
import cv2
import tqdm


ARGS = None
WDIR = f"/tmp/pabsan-0/{sys.argv[0].split('/')[-1]}/"


class CustomYoloPainter:

    def __init__(self):

        self.labels_json = self.__parse_json(ARGS.labels)
        self.preds_json = self.__parse_json(ARGS.preds)

        (
            self.images,
            self.images_by_id,
            self.images_by_fname,
            self.annotations_by_fname,
        ) = self.__digest_labels()

        self.preds_by_fname = self.__digest_preds()

    def __parse_json(self, fname):
        """Loads json as attribute"""
        with open(fname, "r") as file:
            src_json = json.load(file)

        return src_json

    def __digest_labels(self):
        """Builds several fname and id indexed dicts to handle JSON labels"""

        images = []  # Will receive existing image label {}-fields
        images_by_id = {}  # Will receive id->{} mapping
        images_by_fname = {}  # Will receive path->{} mapping

        for image in self.labels_json["images"]:

            fname = os.path.join(ARGS.parent_dir, image["file_name"])

            if os.path.exists(fname):
                images.append(image)
                images_by_id[image["id"]] = image
                images_by_fname[fname] = image
            else:
                print("File %s not found." % fname, file=sys.stderr)

        annotations_by_fname = {}  # Will receive existing label path->{[]} mapping
        for annotation in self.labels_json["annotations"]:
            image_id = annotation["image_id"]

            # Get the image path if image has been checked to exist
            if image_id in images_by_id:
                image = images_by_id[image_id]
                fname = os.path.join(ARGS.parent_dir, image["file_name"])

                # Allocate space for this image if needed
                if not fname in annotations_by_fname:
                    annotations_by_fname[fname] = []

                # Add the current prediciton (may be more than one)
                annotations_by_fname[fname].append(annotation)

        return images, images_by_id, images_by_fname, annotations_by_fname

    def __digest_preds(self):
        """Builds fname-indexed dict to handle JSON predictions"""

        preds_by_fname = {}  # Will receive path->{[]} mapping

        # Get the image id
        for pred in self.preds_json:
            image_id = pred["image_id"]

            # Get the image path if image has been checked to exist
            if image_id in self.images_by_id:
                image = self.images_by_id[image_id]
                fname = os.path.join(ARGS.parent_dir, image["file_name"])

                # Allocate space for this image if needed
                if not fname in preds_by_fname:
                    preds_by_fname[fname] = []

                # Add the current prediciton (may be more than one)
                preds_by_fname[fname].append(pred)

        return preds_by_fname

    def path_to_id(self, fname):
        """Fetches the id of an image given its filename"""
        return self.images_by_fname[fname]["id"]

    def id_to_path(self, fid):
        """Fetches the path of an image given its id"""
        return self.images_by_id[fid]["file_name"]

    def draw_annots(self, img, img_data):
        """Draws annotations onto images"""
        fname = os.path.join(ARGS.parent_dir, img_data["file_name"])

        annot_data = self.annotations_by_fname.get(fname, False)
        if not annot_data:
            print("No annot data in %s for %s" % (ARGS.labels, fname))
            return img

        for annot in annot_data:
            cls = annot["category_id"]
            x1, y1, x2, y2 = annot["bbox"]
            img = cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 4)
            img = cv2.putText(
                img, "a" + str(cls), (x1, y1), 0, 4, (0, 255, 0), 4, cv2.LINE_AA
            )

        return img

    def draw_preds(self, img, img_data):
        """Draws predictions onto images"""
        fname = os.path.join(ARGS.parent_dir, img_data["file_name"])

        pred_data = self.preds_by_fname.get(fname, False)
        if not pred_data:
            print("No pred data!")
            return img

        for pred in pred_data:
            cls = pred["category_id"]
            x1, y1, x2, y2 = pred["bbox"]
            img = cv2.rectangle(img, (x1, y1), (x2, y2), (255, 0, 0), 4)
            img = cv2.putText(
                img, "p" + str(cls), (x1, y1), 0, 4, (255, 0, 0), 4, cv2.LINE_AA
            )

        return img

    def dataset_draw(self):

        for image in self.images:
            fname = os.path.join(ARGS.parent_dir, image["file_name"])

            img = cv2.imread(fname)
            img = self.draw_annots(img, image)
            img = self.draw_preds(img, image)

            cv2.imshow("s", img)
            cv2.waitKey()
            cv2.imwrite(WDIR + str(image["id"]) + ".png", img)

            print("Saved image to", WDIR + str(image["id"]) + ".png")


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="")
    parser.add_argument("labels", type=str, help="MS-COCO like .json label file")
    parser.add_argument("preds", type=str, help="MS-coco like .json results file")
    parser.add_argument(
        "-d",
        "--parent-dir",
        default="",
        type=str,
        help=(
            "Parent dir to the image paths in labels.json."
            "If not provided, assume fnames relative to label file."
        ),
    )
    ARGS = parser.parse_args()

    # If parent dir is not provided, use JSON file's path
    if not ARGS.parent_dir:
        ARGS.parent_dir = os.path.dirname(os.path.abspath(ARGS.labels))

    cyp = CustomYoloPainter()
    cyp.dataset_draw()
