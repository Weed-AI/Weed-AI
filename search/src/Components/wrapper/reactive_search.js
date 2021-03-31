import React, { Component } from 'react';
import Tooltip from '@material-ui/core/Tooltip';
import {
    ReactiveBase,
    RangeSlider,
    ResultCard,
    MultiList,
    ReactiveList,
    SelectedFilters,
    MultiDropdownList
} from '@appbaseio/reactivesearch';
import { GeoDistanceSlider } from "@appbaseio/reactivemaps";
import Cookies from 'js-cookie';
import axios from 'axios';


const theme = {
    typography: {
        fontFamily: 'Raleway, Helvetica, sans-serif',
    },
    colors: {
        primaryColor: '#0A0A0A',
        titleColor: '#E64626',
    },
    component: {
        padding: 10
    }
}

const WeedAIResultCard = (props) => {
  const {item, datasetNames, baseURL} = props;
  const formatCropType = (typ) => {
    return typ == "other" ? "other crop type" : typ;
  }
  const formatGrowthRange = (item) => {
    if (item.agcontext__growth_stage_min_text == item.agcontext__growth_stage_max_text)
      return item.agcontext__growth_stage_min_text;
    return item.agcontext__growth_stage_min_text + " to " + item.agcontext__growth_stage_max_text;
  }
  const formatTaskType = (taskTypes) => (
    taskTypes.includes("segmentation") ? "segment" : (taskTypes.includes("bounding box") ? "bounding box" : "labels"));
  const pluralise = (text, n) => n == 1 ? text : (text.match(/[zsx]$/) ? text + "es" : text + "s");
  return (
    <ResultCard>
        <ResultCard.Image
            src={item.thumbnail_bbox || item.thumbnail}
        />
        <ResultCard.Description>
            <ul className="annotations">
            {
                // TODO: make this more idiomatically React
                Array.from(new Set(item.annotation__category__name)).map((annotName) => {
                    const annot = annotName.match(/^[^:]*/)
                    return annot.length > 0 ? (<Tooltip title={annotName}><li className={annot[0]}>{annot[0]}</li></Tooltip>) : ""
                })
            }
            </ul>
            {" " + pluralise(formatTaskType(item.task_type), item.annotations.length) + " in " + formatCropType(item.agcontext__crop_type) + (item.agcontext__bbch_growth_range == "na" ? "" : " (" + formatGrowthRange(item) + ")") + "."}
          <div><a title={item.upload_id in datasetNames ? datasetNames[item.upload_id] : ""} href={`${baseURL}datasets/${item.upload_id}`}>See Dataset</a></div>
        </ResultCard.Description>
    </ResultCard>
  );
};


export const TestWeedAIResultCard = () => {
  return <ReactiveBase
        app="weedid"
        url={"https://localhost/elasticsearch/"}
        theme={theme}
        headers={{'X-CSRFToken': Cookies.get('csrftoken')}}
    >
      <WeedAIResultCard item={ {
        "id": 20,
        "file_name": "cwfid_images/020_image.png",
        "license": 0,
        "agcontext_id": 0,
        "width": 1296,
        "height": 966,
        "annotations": [
          {
            "id": 490,
            "image_id": 20,
            "category_id": 0,
            "segmentation": [
              [
                807,
                563,
                695,
                635,
                694,
                671,
                816,
                741,
                842,
                713,
                849,
                663,
                821,
                564
              ]
            ],
            "iscrowd": 0,
            "category": {
              "name": "crop: daucus carota",
              "common_name": "carrot",
              "species": "daucus carota",
              "eppo_taxon_code": "DAUCS",
              "eppo_nontaxon_code": "3UMRC",
              "role": "crop",
              "id": 0
            },
            "category__name": "crop: daucus carota",
            "category__common_name": "carrot",
            "category__species": "daucus carota",
            "category__eppo_taxon_code": "DAUCS",
            "category__eppo_nontaxon_code": "3UMRC",
            "category__role": "crop",
            "category__id": 0
          },
          {
            "id": 491,
            "image_id": 20,
            "category_id": 0,
            "segmentation": [
              [
                768,
                747,
                708,
                775,
                699,
                818,
                757,
                897,
                771,
                900,
                789,
                885,
                791,
                815,
                799,
                758
              ]
            ],
            "iscrowd": 0,
            "category": {
              "name": "crop: daucus carota",
              "common_name": "carrot",
              "species": "daucus carota",
              "eppo_taxon_code": "DAUCS",
              "eppo_nontaxon_code": "3UMRC",
              "role": "crop",
              "id": 0
            },
            "category__name": "crop: daucus carota",
            "category__common_name": "carrot",
            "category__species": "daucus carota",
            "category__eppo_taxon_code": "DAUCS",
            "category__eppo_nontaxon_code": "3UMRC",
            "category__role": "crop",
            "category__id": 0
          },
          {
            "id": 492,
            "image_id": 20,
            "category_id": 1,
            "segmentation": [
              [
                209,
                711,
                125,
                730,
                95,
                773,
                88,
                816,
                121,
                861,
                180,
                857,
                245,
                785,
                240,
                738
              ]
            ],
            "iscrowd": 0,
            "category": {
              "name": "weed: UNSPECIFIED",
              "species": "UNSPECIFIED",
              "role": "weed",
              "id": 1
            },
            "category__name": "weed: UNSPECIFIED",
            "category__species": "UNSPECIFIED",
            "category__role": "weed",
            "category__id": 1
          },
          {
            "id": 493,
            "image_id": 20,
            "category_id": 0,
            "segmentation": [
              [
                777,
                216,
                730,
                252,
                694,
                294,
                682,
                340,
                774,
                395,
                860,
                411,
                897,
                402,
                906,
                355,
                884,
                284,
                841,
                240
              ]
            ],
            "iscrowd": 0,
            "category": {
              "name": "crop: daucus carota",
              "common_name": "carrot",
              "species": "daucus carota",
              "eppo_taxon_code": "DAUCS",
              "eppo_nontaxon_code": "3UMRC",
              "role": "crop",
              "id": 0
            },
            "category__name": "crop: daucus carota",
            "category__common_name": "carrot",
            "category__species": "daucus carota",
            "category__eppo_taxon_code": "DAUCS",
            "category__eppo_nontaxon_code": "3UMRC",
            "category__role": "crop",
            "category__id": 0
          }
        ],
        "thumbnail": "foo/02/020_image.png",
        "upload_id": "#",
        "resolution": 1251936,
        "agcontext": {
          "id": 0,
          "agcontext_name": "cwfid",
          "crop_type": "daucus carota",
          "bbch_growth_range": [
            10,
            20
          ],
          "soil_colour": "grey",
          "surface_cover": "none",
          "surface_coverage": "0-25",
          "weather_description": "sunny",
          "location_lat": 53,
          "location_long": 11,
          "location_datum": 4326,
          "upload_time": "2020-09-23 16:34:49",
          "camera_make": "JAI AD-130GE",
          "camera_lens": "Fujinon TF15-DA-8",
          "camera_lens_focallength": 15,
          "camera_height": 450,
          "camera_angle": 90,
          "camera_fov": 22.6,
          "photography_description": "Mounted on boom",
          "lighting": "natural",
          "cropped_to_plant": false,
          "url": "https://github.com/cwfid/dataset",
          "growth_stage_min_text": "Seedling",
          "growth_stage_max_text": "Tillering",
          "growth_stage_texts": [
            "Seedling",
            "Tillering"
          ]
        },
        "sortKey": 2797745463957061359,
        "agcontext__id": 0,
        "agcontext__agcontext_name": "cwfid",
        "agcontext__crop_type": "daucus carota",
        "agcontext__bbch_growth_range": [
          10,
          20
        ],
        "agcontext__soil_colour": "grey",
        "agcontext__surface_cover": "none",
        "agcontext__surface_coverage": "0-25",
        "agcontext__weather_description": "sunny",
        "agcontext__location_lat": 53,
        "agcontext__location_long": 11,
        "agcontext__location_datum": 4326,
        "agcontext__upload_time": "2020-09-23 16:34:49",
        "agcontext__camera_make": "JAI AD-130GE",
        "agcontext__camera_lens": "Fujinon TF15-DA-8",
        "agcontext__camera_lens_focallength": 15,
        "agcontext__camera_height": 450,
        "agcontext__camera_angle": 90,
        "agcontext__camera_fov": 22.6,
        "agcontext__photography_description": "Mounted on boom",
        "agcontext__lighting": "natural",
        "agcontext__cropped_to_plant": false,
        "agcontext__url": "https://github.com/cwfid/dataset",
        "agcontext__growth_stage_min_text": "Seedling",
        "agcontext__growth_stage_max_text": "Tillering",
        "agcontext__growth_stage_texts": [
          "Seedling",
          "Tillering"
        ],
        "annotation__id": [
          490,
          491,
          492,
          493
        ],
        "annotation__image_id": [
          20,
          20,
          20,
          20
        ],
        "annotation__category_id": [
          0,
          0,
          1,
          0
        ],
        "annotation__segmentation": [
          [
            [
              807,
              563,
              695,
              635,
              694,
              671,
              816,
              741,
              842,
              713,
              849,
              663,
              821,
              564
            ]
          ],
          [
            [
              768,
              747,
              708,
              775,
              699,
              818,
              757,
              897,
              771,
              900,
              789,
              885,
              791,
              815,
              799,
              758
            ]
          ],
          [
            [
              209,
              711,
              125,
              730,
              95,
              773,
              88,
              816,
              121,
              861,
              180,
              857,
              245,
              785,
              240,
              738
            ]
          ],
          [
            [
              777,
              216,
              730,
              252,
              694,
              294,
              682,
              340,
              774,
              395,
              860,
              411,
              897,
              402,
              906,
              355,
              884,
              284,
              841,
              240
            ]
          ]
        ],
        "annotation__iscrowd": [
          0,
          0,
          0,
          0
        ],
        "annotation__category": [
          {
            "name": "crop: daucus carota",
            "common_name": "carrot",
            "species": "daucus carota",
            "eppo_taxon_code": "DAUCS",
            "eppo_nontaxon_code": "3UMRC",
            "role": "crop",
            "id": 0
          },
          {
            "name": "crop: daucus carota",
            "common_name": "carrot",
            "species": "daucus carota",
            "eppo_taxon_code": "DAUCS",
            "eppo_nontaxon_code": "3UMRC",
            "role": "crop",
            "id": 0
          },
          {
            "name": "weed: UNSPECIFIED",
            "species": "UNSPECIFIED",
            "role": "weed",
            "id": 1
          },
          {
            "name": "crop: daucus carota",
            "common_name": "carrot",
            "species": "daucus carota",
            "eppo_taxon_code": "DAUCS",
            "eppo_nontaxon_code": "3UMRC",
            "role": "crop",
            "id": 0
          }
        ],
        "annotation__category__name": [
          "crop: daucus carota",
          "crop: daucus carota",
          "weed: UNSPECIFIED",
          "crop: daucus carota"
        ],
        "annotation__category__common_name": [
          "carrot",
          "carrot",
          "carrot"
        ],
        "annotation__category__species": [
          "daucus carota",
          "daucus carota",
          "UNSPECIFIED",
          "daucus carota"
        ],
        "annotation__category__eppo_taxon_code": [
          "DAUCS",
          "DAUCS",
          "DAUCS"
        ],
        "annotation__category__eppo_nontaxon_code": [
          "3UMRC",
          "3UMRC",
          "3UMRC"
        ],
        "annotation__category__role": [
          "crop",
          "crop",
          "weed",
          "crop"
        ],
        "annotation__category__id": [
          0,
          0,
          1,
          0
        ],
        "task_type": [
          "bounding box",
          "classification",
          "segmentation"
        ]
      }
    }  datasetNames={ {"#": "foobar"} } />
  </ReactiveBase>
};

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
                URLParams: false,
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

        const baseURL = new URL(window.location.origin);

        const datasetNames = {};
        axios.get(baseURL + 'api/upload_list/')
        .then(res => res.data)
        .then(json => json.map((dataset) =>
            {datasetNames[dataset.upload_id] = dataset.name;}
        ));

        return (
            <ReactiveBase
                app="weedid"
                mapKey="AIzaSyDDiJ4QoRW9_DJEV94ehO3z8zfCHRuHfxk"
                url={baseURL + "elasticsearch/"}
                theme={theme}
                headers={{'X-CSRFToken': Cookies.get('csrftoken')}}
            >
                <div style={{ position: "fixed", width: "20rem", overflow: "scroll", height: "90%", left: 0, padding: '1rem' }}>
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
                        title="Datasets"
                        placeholder="Select datasets"
                        sortBy="asc"
                        filterLabel="Datasets"
                        {...makeProps("dataset_name_filter", true)}
                    />
                    <SelectedFilters clearAllLabel="Clear filters" />
                    <ReactiveList
                        componentId="result"
                        dataField="results"
                        title="Results"
                        sortOptions={[{"label": "random order", "dataField": "sortKey", "sortBy": "asc"}]}
                        from={0}
                        size={20}
                        {...makeProps("result", false)}
                        infiniteScroll={true}
                        renderResultStats={
                            function(stats){
                                return (
                                    <p style={{position: 'absolute', left: 0, fontSize: '0.8em'}}>{stats.numberOfResults} annotated images found</p>
                                )
                            }
                        }
                        render={({ data }) => (
                            <ReactiveList.ResultCardsWrapper>
                              {
                                data.map(item => <WeedAIResultCard key={item._id} item={item} datasetNames={datasetNames} baseURL={baseURL} />)
                              }
                            </ReactiveList.ResultCardsWrapper>
                        )}
                    />
                    {this.props.footer}
                </div>
            </ReactiveBase>
        );
    }
}

export default ReactiveSearchComponent;
