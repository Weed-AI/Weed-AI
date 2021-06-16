import React from 'react';
import Tooltip from '@material-ui/core/Tooltip';
import {
    ResultCard
} from '@appbaseio/reactivesearch';
import { makeStyles } from '@material-ui/core/styles';
import Magnifier from "react-magnifier";
import {
  MagnifierContainer, MagnifierZoom, MagnifierPreview,
} from "react-image-magnifiers";

const useStyles = makeStyles(theme => (console.log(theme) || {
  imageContainer: {
    width: "calc(100% + 20px)",
    maxHeight: "220px",
    margin: "0 0 0 -10px",
    position: "relative",
    justifyContent: "center",
    alignItems: "center",
  },
  image: {
    maxWidth: "100%",
    maxHeight: "100%",
    width: "auto",
    height: "auto",
  },
}));


const BBox = ({ item, annot }) => {
  const containerHeight = 220;
  const containerWidth = 250; // XXX: can we compute this? it can be less...
  const aspectRatio = item.width / item.height;
  const thumbScale = aspectRatio >= (containerWidth / containerHeight) ? containerWidth / item.width : containerHeight / item.height;
  const thumbTop = 0 // (containerHeight - item.height * thumbScale) / 2;
  const thumbLeft = 0 // (containerWidth - item.width * thumbScale) / 2;
  const species = annot.category.name.match(/^([^:]*): (.*)/)[2]
  const color = annot.category.name.startsWith("weed") ? "#dc3545" : annot.category.name.startsWith("crop") ? "#28a745" : "#808080";
  return <div style={{
      pointerEvents: "none",
      border: "1px solid",
      borderColor: color,
      position: "absolute",
      left: thumbLeft + thumbScale * annot.bbox[0],
      top: thumbTop + thumbScale * annot.bbox[1],
      width: thumbScale * annot.bbox[2],
      height: thumbScale * annot.bbox[3],
  }} >
    { species ? <span style={{
      fontSize: ".5em",
      background: color + "30",  // transparent
      color: "white",
      position: "absolute",
      overflow: "hidden",
      maxWidth: Math.max(60, thumbScale * annot.bbox[2]),
      top: 0,
    }}>{species}</span> : [] }
  </div>
}

const WeedAIResultCard = (props) => {
  const {item, baseURL, linkToDataset} = props;
  const classes = useStyles();
  const formatCropType = (typ) => {
    return typ === "other" ? "other crop type" : typ;
  }
  const formatGrowthRange = (item) => {
    if (item.agcontext__growth_stage_min_text === item.agcontext__growth_stage_max_text)
      return item.agcontext__growth_stage_min_text;
    return item.agcontext__growth_stage_min_text + " to " + item.agcontext__growth_stage_max_text;
  }
  const formatTaskType = (taskTypes) => (
    taskTypes.includes("segmentation") ? "segment" : (taskTypes.includes("bounding box") ? "bounding box" : "labels"));
  const pluralise = (text, n) => n === 1 ? text : (text.match(/[zsx]$/) ? text + "es" : text + "s");
  return (
    <ResultCard style={{position: "relative"}}>
        <div className={classes.imageContainer}>
    <MagnifierContainer >
    <MagnifierPreview imageSrc={item.thumbnail} className={classes.image} />
            {item.annotations.filter(annot => annot.bbox).map(annot => <BBox item={item} annot={annot} />)}
    <MagnifierZoom style={{ height: "120px", zIndex: 5 }} imageSrc={"/code/images/" + item.upload_id + "/" + item.file_name} />
</MagnifierContainer>
        </div>
        <ResultCard.Description style={{position: "absolute", bottom: "12px"}}>
            <ul className="annotations">
            {
                // TODO: make this more idiomatically React
                Array.from(new Set(item.annotation__category__name)).map((annotName) => {
                    const annot = annotName.match(/^([^:]*): (.*)/)
                    return annot.length > 0 ? (<Tooltip title={annotName}><li className={annot[1]}>{annot[2]}</li></Tooltip>) : ""
                })
            }
            </ul>
            {
              " " +
              pluralise(formatTaskType(item.task_type), item.annotations.length) +
              " in " +
              formatCropType(item.agcontext__crop_type) +
              (item.agcontext__bbch_growth_range
                ? " (" + formatGrowthRange(item) + ")"
                : "") +
              "."
            }
            {linkToDataset === false ? [] : <div><Tooltip title={item.dataset_name}><a href={`${baseURL}datasets/${item.upload_id}`}>See Dataset</a></Tooltip></div>}
        </ResultCard.Description>
    </ResultCard>
  );
};


export default WeedAIResultCard;
