import React, {Component} from 'react';
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
        <ReactMarkdown source={this.state.markdownContent} />
      </article>
    );
  }
}

export default withStyles(useStyles)(AboutComponent);
