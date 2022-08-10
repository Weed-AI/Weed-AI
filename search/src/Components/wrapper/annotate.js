import React, {Component} from 'react';
import { Helmet } from "react-helmet";
import { withStyles } from '@material-ui/core/styles';
import Markdown from "../../Common/Markdown";
import content from './annotate.md'
import { useArticleStyles } from '../../styles/common'


class AnnotationComponent extends Component {
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
            <title>About Annotation - Weed-AI</title>
            <meta
              name="description"
              content="Weed-AI is a repository of weed imagery in crops. Find and download datasets of annotated weed imagery. Search by crop and weed species/genus, crop growth stage, location, photography attributes, annotation task type and more. Collect and upload your own!"
            />
        </Helmet>
        <Markdown escapeHtml={false} source={this.state.markdownContent} />
      </article>
    );
  }
}

export default withStyles(useArticleStyles)(AnnotationComponent);
