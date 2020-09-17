import React, { Component } from 'react';
import {
	ReactiveBase,
	DataSearch,
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
					{/* <DataSearch
						componentId="searchbox"
						dataField={["annotations__category__common_name","annotation__category__role.keyword","agcontext__agcontext_name.keyword","annotation__category__species.keyword"]}
						placeholder="Search for species, role, or agcontext"
						autoSuggest={true}
						defaultSuggestions={[
							{label: "Weed", value: "weed"},
							{label: "Carrot", value: "carrot"}
						]}
						highlight={true}
						highlightField={["annotations__category__common_name","annotation__category__role.keyword","agcontext__agcontext_name.keyword","annotation__category__species.keyword"]}
						queryFormat="or"
						fuzziness={0}
						debounce={100}
						react={{
						  and: ["searchbox","resslider","agcontextfilter","rolefilter","speciesfilter","grainstextfilter"]
						}}
						showFilter={true}
						filterLabel="General filter"
						URLParams={true}
				/> */}
					<MultiList
						componentId="rolefilter"
						title="Filter by role"
						dataField="annotation__category__role.keyword"
						sortBy="asc"
						queryFormat="and"
						selectAllLabel="All roles"
						showCheckbox={true}
						showCount={true}
						showSearch={true}
						placeholder="Search Role"
						react={{
							and: ["searchbox", "resslider", "agcontextfilter", "rolefilter", "speciesfilter", "grainstextfilter"]
						}}
						showFilter={true}
						filterLabel="Role"
						URLParams={true}
						style={{
							padding: "5px",
							marginTop: "10px"
						}}
					/>
					<MultiList
						componentId="speciesfilter"
						title="Filter by species"
						dataField="annotation__category__species.keyword"
						sortBy="asc"
						queryFormat="and"
						selectAllLabel="All species"
						showCheckbox={true}
						showCount={true}
						showSearch={true}
						placeholder="Search Species"
						react={{
							and: ["searchbox", "resslider", "agcontextfilter", "rolefilter", "speciesfilter", "grainstextfilter"]
						}}
						showFilter={true}
						filterLabel="Species"
						URLParams={true}
						style={{
							padding: "5px",
							marginTop: "10px"
						}}
					/>
					<MultiList
						componentId="agcontextfilter"
						title="Filter by Collection"
						dataField="agcontext__agcontext_name.keyword"
						sortBy="asc"
						queryFormat="and"
						selectAllLabel="All collections"
						showCheckbox={true}
						showCount={true}
						showSearch={true}
						placeholder="Search collection"
						react={{
							and: ["searchbox", "resslider", "agcontextfilter", "rolefilter", "speciesfilter", "grainstextfilter"]
						}}
						showFilter={true}
						filterLabel="Agcontext"
						URLParams={true}
						style={{
							padding: "5px",
							marginTop: "10px"
						}}
					/>
					<MultiList
						componentId="grainstextfilter"
						title="Filter by Growth Stage"
						dataField="agcontext__grains_descriptive_text.keyword"
						sortBy="asc"
						queryFormat="and"
						selectAllLabel="All growth stages"
						showCheckbox={true}
						showCount={true}
						showSearch={true}
						placeholder="Search growth stage"
						react={{
							and: ["searchbox", "resslider", "agcontextfilter", "rolefilter", "speciesfilter", "grainstextfilter"]
						}}
						showFilter={true}
						filterLabel="Growth stage"
						URLParams={true}
						style={{
							padding: "5px",
							marginTop: "10px"
						}}
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
						showFilter={true}
						interval={10000}
						react={{
							and: ["searchbox", "resslider", "agcontextfilter", "rolefilter", "speciesfilter", "grainstextfilter"]
						}}
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
												{item._id + " " + '*'.repeat(item.total_quantity)}
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
