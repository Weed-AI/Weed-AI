import React from 'react';
import CategoryTooltip from './CategoryTooltip';
import { parseCategoryName } from '../../Common/weedcocoUtil';
import Tooltip from '@material-ui/core/Tooltip';
import CardActions from '@material-ui/core/CardActions';
import Button from '@material-ui/core/Button';
import {
    ResultCard
} from '@appbaseio/reactivesearch';


const AnnotationCategory = ({ categoryName }) => {
  const { role, taxon } = parseCategoryName(categoryName);
  return <CategoryTooltip categoryName={categoryName}>
    <li className={role}>{taxon || role}</li>
  </CategoryTooltip>
};

const WeedAIResultCard = (props) => {
  const {item, baseURL, linkToDataset} = props;
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
    <ResultCard>
        <ResultCard.Image
            src={item.thumbnail_bbox || item.thumbnail}
        />
        <ResultCard.Description>
            <ul className="annotations">
            {
                Array.from(new Set(item.annotation__category__name)).map(
                  (annotName) => <AnnotationCategory categoryName={annotName} key={annotName} />)
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
            <CardActions>
              {linkToDataset === false ? []
                : <Tooltip title={item.dataset_name}><Button size="small" variant="outlined" color="primary" href={`${baseURL}datasets/${item.upload_id}`}>See Dataset</Button></Tooltip>}
            </CardActions>
        </ResultCard.Description>
    </ResultCard>
  );
};


export default WeedAIResultCard;
