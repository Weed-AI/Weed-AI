import React, { Component } from 'react';
import {
	ReactiveBase,
	CategorySearch,
	RangeSlider,
	ReactiveOpenStreetMap,
	ResultCard,
	MultiList,
	ReactiveList
} from '@appbaseio/reactivesearch';
import logo from './logo.svg';
import './App.css';

class App extends Component {
	render() {
		return (
			<ReactiveBase
			app="weedid"
			url="http://localhost:9200/">
				<div style={{ display: "flex", flexDirection: "row" }}>
					<div style={{ display: "flex", flexDirection: "column", width: "40%" }}>
			    <CategorySearch
						componentId="searchbox"
						dataField={["annotations.category.common_name.keyword","annotations.category.role.keyword","annotations.agcontext.agcontext_name.keyword"]}
						categoryField={["annotations.category.common_name.keyword","annotations.category.role.keyword","annotations.agcontext.agcontext_name.keyword"]}
						placeholder="Search for species, role, or agcontext"
						autoSuggest={true}
						defaultSuggestions={[{label: "Weed", value: "weed"}]}
						highlight={false}
						highlightField={["annotations.category.common_name.keyword","annotations.category.role.keyword","annotations.agcontext.agcontext_name.keyword"]}
						queryFormat="or"
						fuzziness={0}
						debounce={100}
						react={{
						  and: ["CategoryFilter", "SearchFilter"]
						}}
						showFilter={true}
						filterLabel="Venue filter"
						URLParams={false}
				/>
				<MultiList
						componentId="rolefilter"
						title="Filter by role"
						dataField="annotations.category.role.keyword"
						sortBy="asc"
						queryFormat="or"
						selectAllLabel="All roles"
						showCheckbox={true}
						showCount={true}
						showSearch={true}
						placeholder="Search Role"
						react={{
							and: ["searchbox", "SearchFilter"]
						}}
						showFilter={true}
						filterLabel="Role"
						URLParams={false}
						style={{
							padding: "5px",
							marginTop: "10px"
						}}
					/>
				<MultiList
						componentId="agcontextfilter"
						title="Filter by agcontext"
						dataField="annotations.agcontext.agcontext_name.keyword"
						sortBy="asc"
						queryFormat="or"
						selectAllLabel="All agcontexts"
						showCheckbox={true}
						showCount={true}
						showSearch={true}
						placeholder="Search Agcontext"
						react={{
							and: ["searchbox", "SearchFilter"]
						}}
						showFilter={true}
						filterLabel="Agcontext"
						URLParams={false}
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
							"end": 1000000
						}}
						rangeLabels={{
							"start": "Start",
							"end": "End"
						}}
						stepValue={10000}
						showHistogram={true}
						showFilter={true}
						interval={2}
						react={{
							and: ["Searchbox","CategoryFilter", "SearchFilter"]
						}}
				/>
				</div>
				<ReactiveList
					componentId="result"
					title="Results"
					dataField="annotations.category.common_name.keyword"
					from={0}
					size={5}
					pagination={true}
					react={{
						and: ["searchbox","resslider","agcontextfilter","rolefilter"]
					}}
					render={({ data }) => (
						<ReactiveList.ResultCardsWrapper>
							{
								data.map(item => (
									<ResultCard key={item._id}>
										<ResultCard.Image
											src={'thumbnails/' + item.file_name}
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
