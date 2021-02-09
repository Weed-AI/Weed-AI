import pandas as pd


class WeedCOCOStats:
    def __init__(self, weedcoco):
        self.annotations = self.compute_annotation_frame(weedcoco)
        self.summary = self.compute_summary(self.annotations)

    @staticmethod
    def compute_annotation_frame(weedcoco):
        out = [
            {
                "annotation_id": annotation["id"],
                "image_id": annotation["image_id"],
                "category_id": annotation["category_id"],
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
    def compute_summary(annotation_frame):
        gb = annotation_frame.groupby(["agcontext_id", "category_id"])
        return pd.DataFrame(
            {"annotation_count": gb.size(), "image_count": gb["image_id"].nunique()}
        )
