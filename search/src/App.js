import React, { Component } from 'react';
import { 
	ReactiveBase, CategorySearch, SingleRange, ResultCard, ReactiveList 
} from '@appbaseio/reactivesearch';
import logo from './logo.svg';
import './App.css';

class App extends Component {
	render() {
		return (
				<ReactiveBase
				app="kibana_sample_data_ecommerce"
				url="http://localhost:9200/">
			    <CategorySearch
						componentId="searchbox"
						dataField="day_of_week"
						categoryField="day_of_week"
						placeholder="Search for days"
					/>
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
												src='https://bit.do/demoimg'
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
				</ReactiveBase>
		);
	}
}

export default App;
