import React, {Component} from 'react';
import { Helmet } from "react-helmet";
import { withStyles } from '@material-ui/core/styles';
import Markdown from "../../Common/Markdown";
import content from './weedcoco.md'
import { useArticleStyles } from '../../styles/common'

class WeedCOCOComponent extends Component {
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
        <Helmet>
            <title>About WeedCOCO - Weed-AI</title>
            <meta name="description" content="WeedCOCO is a standard interchange format for images annotated with weeds and their metadata." />
        </Helmet>
        <Markdown source={this.state.markdownContent} />
      </article>
    );
  }
}

export default withStyles(useArticleStyles)(WeedCOCOComponent);
