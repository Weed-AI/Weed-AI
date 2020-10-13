import React, { Component } from 'react';
import {
	ReactiveBase,
	RangeSlider,
	ResultCard,
	MultiList,
	ReactiveList,
	SelectedFilters
} from '@appbaseio/reactivesearch';
import logo from './logo.svg';
import './App.css';

class App extends Component {
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
				queryFormat: "or",
				URLParams: true,
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

		return (
			<ReactiveBase
				app="weedid"
				url="http://localhost:9200/"
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
			>
				<div style={{ position: "fixed", width: "20rem", overflow: "scroll", height: "100%" }}>
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
						dataField="agcontext__grains_descriptive_text.keyword"
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
						interval={10000}
						{...makeProps("resslider", false)}
					/>
				</div>
				<div style={{ position: "absolute", left: "20rem" }}>
					<SelectedFilters />
					<ReactiveList
						componentId="result"
						dataField="results"
						title="Results"
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
												src={'thumbnails/' + item.thumbnail}
											/>
											<ResultCard.Title
												dangerouslySetInnerHTML={{
													__html: item.customer_phone
												}}
											/>
											<ResultCard.Description>
												{"Crop: " + item.agcontext__crop_type}
											</ResultCard.Description>
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

export default App;
