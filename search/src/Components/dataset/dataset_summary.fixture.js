import React from 'react';
import { DatasetSummary } from './dataset_summary';
import { useStyles } from './dataset_summary';
import { withStyles } from '@material-ui/core/styles';

const DatasetSummaryWrapper = (props) => {
    const Out = withStyles(useStyles)(DatasetSummary);
    console.log(props)
    return (<div style={{ margin: "3em" }}><Out {...props} /></div>);
}

export default <DatasetSummaryWrapper
    upload_id="foobar"
    metadata={{
        "creator": [
            {"name": "Sebastian Haug", "@type": "Person"},
            {"name": "J\u00f6rn Ostermann", "sameAs": "https://orcid.org/0000-0002-6743-3324", "@type": "Person", "affiliation": {"name": "Leibniz Universität Hannover", "sameAs": "https://ror.org/0304hq317", "@type": "Organization"}}
        ],
        "funder": [{"name": "some funder"}],
        "name": "A Crop/Weed Field Image Dataset for the Evaluation of Computer Vision Based Precision Agriculture Tasks",
        "description": "Weeds annotated in carrot crops.",
        "datePublished": "2015-03-19",
        "identifier": ["doi:10.1007/978-3-319-16220-1_8"],
        "license": "https://github.com/cwfid/dataset",
        "description": "Foobar",
        "citation": "Sebastian Haug, Jörn Ostermann: A Crop/Weed Field Image Dataset for the Evaluation of Computer Vision Based Precision Agriculture Tasks, CVPPP 2014 Workshop, ECCV 2014"
    }}
    agcontexts={[
        {"n_images": 3, "category_statistics": 
    {"crop: daucus carota sativus": {"annotation_count": 2, "image_count": 1, "segmentation_count": 2, "bounding_box_count": 2},
    "weed: lolium perenne": {"annotation_count": 3, "image_count": 2, "segmentation_count": 3, "bounding_box_count": 3},
    "weed: raphanus raphanistrum": {"annotation_count": 1, "image_count": 1, "segmentation_count": 0, "bounding_box_count": 0}},
            "id": 77, "lighting": "natural", "bbch_code": "na", "crop_type": "sorghum", "camera_fov": "variable", "camera_lens": "Telephoto", "camera_make": "Canon", "soil_colour": "dark_brown", "camera_angle": 45, "emr_channels": "visual", "location_lat": 80, "camera_height": 500, "location_long": 80, "surface_cover": "oilseed", "cropped_to_plant": true, "surface_coverage": "0-25", "weather_description": "rainy", "bbch_descriptive_text": "stem elongation", "camera_lens_focallength": 180, "grains_descriptive_text": "emergence", "photography_description": "poor lighting"}]
    }
/>;
