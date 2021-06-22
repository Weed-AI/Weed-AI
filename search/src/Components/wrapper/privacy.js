import React, {Component} from 'react';
import { withStyles } from '@material-ui/core/styles';
import Markdown from "../../Common/Markdown";
import content from './privacy.md'
import { useArticleStyles } from '../../styles/common'

class PrivacyComponent extends Component {
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
        <Markdown source={this.state.markdownContent} />
      </article>
    );
  }
}

export default withStyles(useArticleStyles)(PrivacyComponent);
