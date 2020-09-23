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
		let facetProps = {
			queryFormat: "or",
			URLParams: true,
			react: {
				or: ["searchbox", "resslider", "agcontextfilter", "rolefilter", "speciesfilter", "grainstextfilter"]
			}
		}
		let multilistFacetProps = {
			showCheckbox: true,
			showCount: true,
			showFilter: true,
			style: {
				padding: "5px",
				marginTop: "10px"
			},
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
						componentId="rolefilter"
						title="Filter by role"
						dataField="annotation__category__role.keyword"
						sortBy="asc"
						selectAllLabel="All roles"
						placeholder="Search Role"
						filterLabel="Role"
						{...facetProps}
						{...multilistFacetProps}
					/>
					<MultiList
						componentId="speciesfilter"
						title="Filter by species"
						dataField="annotation__category__species.keyword"
						sortBy="asc"
						selectAllLabel="All species"
						placeholder="Search Species"
						filterLabel="Species"
						{...facetProps}
						{...multilistFacetProps}
					/>
					<MultiList
						componentId="agcontextfilter"
						title="Filter by Collection"
						dataField="agcontext__agcontext_name.keyword"
						sortBy="asc"
						selectAllLabel="All collections"
						placeholder="Search collection"
						filterLabel="Agcontext"
						{...facetProps}
						{...multilistFacetProps}
					/>
					<MultiList
						componentId="grainstextfilter"
						title="Filter by Growth Stage"
						dataField="agcontext__grains_descriptive_text.keyword"
						sortBy="asc"
						selectAllLabel="All growth stages"
						placeholder="Search growth stage"
						filterLabel="Growth stage"
						{...facetProps}
						{...multilistFacetProps}
					/>
					<RangeSlider
						componentId="resslider"
						dataField="resolution"
						title="Resolution (pixels)"
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
						{...facetProps}
						{...multilistFacetProps}
					/>
				</div>
				<div style={{ position: "absolute", left: "20rem" }}>
					<SelectedFilters />
					<ReactiveList
						componentId="result"
						title="Results"
						dataField="annotations__category__common_name"
						from={0}
						size={20}
						{...facetProps}
						infiniteScroll={true}
						react={{
							and: ["searchbox", "resslider", "agcontextfilter", "rolefilter", "speciesfilter", "grainstextfilter"]
						}}
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
