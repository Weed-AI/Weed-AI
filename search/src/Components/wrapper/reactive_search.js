import React, { Component } from 'react';
import Paper from '@material-ui/core/Paper';
import IconButton from '@material-ui/core/IconButton';
import Typography from '@material-ui/core/Typography';
import CloseIcon from '@material-ui/icons/Close'
import Tooltip from '@material-ui/core/Tooltip';
import {
    RangeSlider,
    MultiList,
    SelectedFilters,
    MultiDropdownList
} from '@appbaseio/reactivesearch';
import { GeoDistanceSlider } from "@appbaseio/reactivemaps";
import SearchBase from '../search/SearchBase';
import ResultsList from '../search/ResultsList';


const IntroText = () => {
  const [show, setShow] = React.useState((localStorage.getItem("showIntro") === "false") ? false : true);
  const onClose = () => { localStorage.setItem("showIntro", "false"); setShow(false) }
  return show ? (
    <Paper style={{ marginTop: "15px", padding: "1em" }}>
      <div style={{float: "right"}}><IconButton style={{ padding: 0 }} onClick={ onClose } aria-label="Close this introductory text"><CloseIcon /></IconButton></div>
      <Typography variant="h6">Welcome to Weed-AI</Typography>
      <Typography>
        Find and download <a href="/datasets">datasets</a> of annotated weed imagery.
        Search by crop and weed species, crop growth stage, location, photography attributes, annotation task type and more.
        Collect and <a href="/upload">upload</a> your own!
      </Typography>
    </Paper>
  ) : [];
}


class ReactiveSearchComponent extends Component {

    render() {
        let makeProps = function (id, ismultilist) {
            let multilistFacetProps = {
                showCheckbox: true,
                showCount: true,
                showFilter: true,
                showSearch: false,
                style: {
                    padding: "5px",
                    marginTop: "10px"
                },
            }
            if (!ismultilist) {
                multilistFacetProps = {}
            }
            let facetProps = {
                innerClass: {
                    title: "filter-title",
                    checkbox: "filter-checkbox"
                },
                queryFormat: "or",
                URLParams: true,
                react: {
                    and: [
                        "crop_type_filter",
                        "category_filter",
                        "grains_text_filter",
                        "task_type_filter",
                        "lighting_filter",
                        "geo_distance_filter",
                        "dataset_name_filter",
                    ]
                },
                ...multilistFacetProps
            }
            var idx
            //remove id from query
            if ((idx = facetProps.react.and.indexOf(id)) !== -1) {
                facetProps.react.and.splice(idx, 1);
            }
            return (facetProps)
        }

        return (
            <SearchBase>
                <div style={{ position: "fixed", width: "20rem", overflow: "scroll", height: "90%", left: 0, padding: '1rem' }}>
                    <IntroText />
                    <MultiList
                        componentId="crop_type_filter"
                        title="Crop Type"
                        dataField="agcontext__crop_type.keyword"
                        sortBy="asc"
                        selectAllLabel="All types"
                        placeholder="Search types"
                        filterLabel="Types"
                        {...makeProps("crop_type_filter", true)}
                    />
                    <MultiList
                        componentId="category_filter"
                        title="Annotated Species"
                        dataField="annotation__category__name.keyword"
                        sortBy="asc"
                        selectAllLabel="All species"
                        placeholder="Search Species"
                        filterLabel="Species"
                        {...makeProps("categoryfilter", true)}
                        showSearch={true}
                    />
                    <MultiList
                        componentId="grains_text_filter"
                        title="Crop Growth Stage"
                        dataField="agcontext__growth_stage_texts.keyword"
                        sortBy="asc"
                        selectAllLabel="All growth stages"
                        placeholder="Search growth stage"
                        filterLabel="Growth stage"
                        {...makeProps("grainstextfilter", true)}
                    />
                    <GeoDistanceSlider
                      title="Location"
                      componentId="geo_distance_filter"
                      placeholder="Search Location"
                      dataField="location"
                      unit="km"
                      showFilter={true}
                      autoLocation={false}
                      range={{
                        start: 10,
                        end: 1000
                      }}
                      defaultValue={{
                        distance: 1000
                      }}
                      rangeLabels={{
                        start: '10km',
                        end: '1000km',
                      }}
                      {...makeProps("geo_distance_filter", false)}
                    />
                    <MultiList
                        componentId="task_type_filter"
                        title="Computer Vision Task"
                        dataField="task_type.keyword"
                        sortBy="asc"
                        selectAllLabel="All tasks"
                        placeholder="Search Tasks"
                        filterLabel="Tasks"
                        {...makeProps("task_type_filter", true)}
                    />
                    <MultiList
                        componentId="lighting_filter"
                        title="Lighting Mode"
                        dataField="agcontext__lighting.keyword"
                        sortBy="asc"
                        selectAllLabel="All lighting"
                        placeholder="Search Lighting"
                        filterLabel="Lighting"
                        {...makeProps("lighting_filter", true)}
                    />
                </div>
                <div style={{ position: "absolute", left: "20rem", paddingRight: "1rem", marginTop: "1rem" }}>
                    <MultiDropdownList
                        componentId="dataset_name_filter"
                        dataField="dataset_name.keyword"
                        URLParams={true}
                        title="Dataset Name"
                        placeholder="Search datasets"
                        sortBy="asc"
                        filterLabel="Datasets"
                        {...makeProps("dataset_name_filter", true)}
                    />
                    <SelectedFilters clearAllLabel="Clear filters" />
                    <ResultsList
                        listProps={makeProps("result", false)}
                    />
                    {this.props.footer}
                </div>
            </SearchBase>
        );
    }
}

export default ReactiveSearchComponent;
