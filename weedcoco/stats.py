import pandas as pd
from weedcoco.utils import get_task_types


class WeedCOCOStats:
    def __init__(self, weedcoco):
        self.annotations = self.compute_annotation_frame(weedcoco)
        self.category_summary = self.compute_summary(
            self.annotations, ["agcontext_id", "category_id"]
        )
        self.agcontext_summary = self.compute_summary(
            self.annotations, ["agcontext_id"]
        )

    @staticmethod
    def compute_annotation_frame(weedcoco):
        out = [
            {
                "annotation_id": annotation["id"],
                "image_id": annotation["image_id"],
                "category_id": annotation["category_id"],
                **{task_type: 1 for task_type in get_task_types(annotation)},
            }
            for annotation in weedcoco["annotations"]
        ]
        out = pd.DataFrame(out)

        image_to_agcontext = pd.Series(
            {image["id"]: image["agcontext_id"] for image in weedcoco["images"]}
        )
        out["agcontext_id"] = out.image_id.map(image_to_agcontext)
        return out

    @staticmethod
    def compute_summary(annotation_frame, by):
        gb = annotation_frame.groupby(by)
        return pd.DataFrame(
            {
                "annotation_count": gb.size(),
                "image_count": gb["image_id"].nunique(),
                "segmentation_count": gb["segmentation"].sum(),
                "bounding_box_count": gb["bounding box"].sum(),
            }
        )
