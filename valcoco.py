import sys
from pycocotools.coco import COCO
from pycocotools.cocoeval import COCOeval

"""
Usage:

valcoco.py groundtruth.json results.json
"""

if __name__ == '__main__':
    gt = sys.argv[1]
    pred = sys.argv[2]

    cocoGt = COCO(gt)
    cocoDt = cocoGt.loadRes(pred)

    cocoEval = COCOeval(cocoGt, cocoDt, 'bbox')
    cocoEval.evaluate()
    cocoEval.accumulate()
    cocoEval.summarize()