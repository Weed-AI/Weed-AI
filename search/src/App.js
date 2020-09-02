import React, { Component } from 'react';
import {
	ReactiveBase,
	CategorySearch,
	DataSearch,
	SingleRange,
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
						dataField="annotations.category.common_name.keyword"
						categoryField="common_name"
						placeholder="Search for species"
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
							and: ["CategoryFilter", "SearchFilter"]
						}}
						showFilter={true}
						filterLabel="Role"
						URLParams={false}
						style={{
							padding: "5px",
							marginTop: "10px"
						}}
					/>
				</div>
				<ReactiveList
					componentId="result"
					title="Results"
					dataField="day_of_week"
					from={0}
					size={5}
					pagination={true}
					react={{
						and: ["searchbox" /*, "ratingsfilter" */ ]
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
											{item.day_of_week + " " + '*'.repeat(item.total_quantity)}
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
