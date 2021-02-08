import React, { Component } from 'react';
import {
	ReactiveBase,
	RangeSlider,
	ResultCard,
	MultiList,
	ReactiveList,
	SelectedFilters
} from '@appbaseio/reactivesearch';
import Cookies from 'js-cookie'


const csrftoken = Cookies.get('csrftoken');

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
						"searchbox",
						"crop_type_filter",
						"category_filter",
						"grains_text_filter",
						"task_type_filter",
						"lighting_filter",
						"resslider",
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

		const esURL = new URL(window.location.origin);

		return (
			<ReactiveBase
				app="weedid"
				url={esURL + "elasticsearch/"}
				theme={{
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
				}}
				headers={{'X-CSRFToken': csrftoken}}
			>
				<div style={{ position: "fixed", width: "20rem", overflow: "scroll", height: "90%", left: 0, padding: '0 1rem' }}>
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
					<RangeSlider
						componentId="resslider"
						dataField="resolution"
						title="Image Resolution (pixels)"
						range={{
							"start": 0,
							"end": 1500000
						}}
						rangeLabels={{
							"start": "Start",
							"end": "End"
						}}
						stepValue={10000}
						showHistogram={true}
						showFilter={true}
						interval={15000}
						{...makeProps("resslider", false)}
					/>
				</div>
				<div style={{ position: "absolute", left: "20rem", paddingRight: "1rem" }}>
					<SelectedFilters />
					<ReactiveList
						componentId="result"
						dataField="results"
						title="Results"
						sortOptions={[{"label": "random order", "dataField": "sortKey", "sortBy": "asc"}]}
						from={0}
						size={20}
						{...makeProps("result", false)}
						infiniteScroll={true}
						render={({ data }) => (
							<ReactiveList.ResultCardsWrapper>
								{
									data.map(item => (
										<ResultCard key={item._id}>
											<ResultCard.Image
												src={item.thumbnail}
											/>
											<ResultCard.Description>
												<ul className="annotations">
												{
													// TODO: make this more idiomatically React
													Array.from(new Set(item.annotation__category__name)).map((annotName) => {
														const annot = annotName.match(/^[^:]*/)
														return annot.length > 0 ? (<li className={annot[0]}>{annot[0]}</li>) : ""
													})
												}
												</ul>
												{" in " + item.agcontext__growth_stage_texts + " " + item.agcontext__crop_type}
											</ResultCard.Description>
											<div><a title={item.info ? item.info.name : ""} href={esURL + item.dataset_url}>See Dataset</a></div>
										</ResultCard>
									))
								}
							</ReactiveList.ResultCardsWrapper>
						)}
					/>
				</div>
			</ReactiveBase>
		);
	}
}

export default ReactiveSearchComponent;
