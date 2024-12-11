#! /usr/bin/env python3

import sys
import argparse
import faster_coco_eval

# Replace pycocotools with faster_coco_eval
faster_coco_eval.init_as_pycocotools()

from pycocotools.coco import COCO
from pycocotools.cocoeval import COCOeval


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Compute MS-COCO metrics.")
    parser.add_argument("gt", type=str, help="MS-COCO .json labels (ground truth)")
    parser.add_argument("pred", type=str, help="MS-COCO .json results (predictions)")
    ARGS = parser.parse_args()

    anno = COCO(ARGS.gt)  # init annotations api
    pred = anno.loadRes(ARGS.pred)  # init predictions api

    val = COCOeval(anno, pred, "bbox")
    val.evaluate()
    val.accumulate()
    val.summarize()
