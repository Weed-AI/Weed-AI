import React, {Component} from 'react';
import { withStyles } from '@material-ui/core/styles';
import ReactMarkdown from "react-markdown";
import content from './about.md'
import { useArticleStyles } from '../../styles/common'


class AboutComponent extends Component {
  constructor(props) {
    super(props)
    this.state = { markdownContent: null }
  }

  componentWillMount() {
    fetch(content).then((response) => response.text()).then((text) => {
      this.setState({ markdownContent: text })
    })
  }

  render() {
    return (
      <article className={this.props.classes.page}>
		<img src="/weedai-logo-small.png" title="Weed-AI" alt="Weed-AI logo" style={{float: "right", marginBottom: "1rem", marginLeft: "1rem"}} />
        <ReactMarkdown source={this.state.markdownContent} />
      </article>
    );
  }
}

export default withStyles(useArticleStyles)(AboutComponent);
