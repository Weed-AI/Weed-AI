import React from 'react';
import CategoryTooltip from './CategoryTooltip';
import Tooltip from '@material-ui/core/Tooltip';
import {
    ResultCard
} from '@appbaseio/reactivesearch';

const AnnotationCategory = ({ categoryName }) => {
  const [role, species] = categoryName.match(/^([^:]*): (.*)/).slice(1);
  return <CategoryTooltip categoryName={categoryName}>
    <li className={role}>{species}</li>
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
            {linkToDataset === false ? [] : <div><Tooltip title={item.dataset_name}><a title={item.dataset_name} href={`${baseURL}datasets/${item.upload_id}`}>See Dataset</a></Tooltip></div>}
        </ResultCard.Description>
    </ResultCard>
  );
};


export default WeedAIResultCard;
