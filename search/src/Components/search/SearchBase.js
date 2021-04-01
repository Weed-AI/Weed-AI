import React from 'react';
import {
    ReactiveBase,
} from '@appbaseio/reactivesearch';
import Cookies from 'js-cookie';

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

const SearchBase = ({ children, baseURL }) => {
  return <ReactiveBase
    app="weedid"
    mapKey="AIzaSyDDiJ4QoRW9_DJEV94ehO3z8zfCHRuHfxk"
    url={baseURL || new URL(window.location.origin) + "elasticsearch/"}
    theme={theme}
    headers={{'X-CSRFToken': Cookies.get('csrftoken')}}
  >
    {children}
  </ReactiveBase>;
}

export default SearchBase;
