import React, {Component} from 'react';
import { Helmet } from "react-helmet";
import { withStyles } from '@material-ui/core/styles';
import ReactMarkdown from "react-markdown";
import content from './about.md'

const useStyles = (theme) => ({
    page: {
        margin: theme.spacing(15)
    },
})


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
        <Helmet>
            <title>About - Weed-AI</title>
            <meta
              name="description"
              content="Weed-AI is a repository of weed imagery in crops. Find and download datasets of annotated weed imagery. Search by crop and weed species, crop growth stage, location, photography attributes, annotation task type and more. Collect and upload your own!"
            />
        </Helmet>
        <img src="/weedai-logo-small.png" title="Weed-AI" alt="Weed-AI logo" style={{float: "right", marginBottom: "1rem", marginLeft: "1rem"}} />
        <ReactMarkdown source={this.state.markdownContent} />
      </article>
    );
  }
}

export default withStyles(useStyles)(AboutComponent);
