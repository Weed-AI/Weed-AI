import ReactMarkdown from "react-markdown";
import gfm from 'remark-gfm'

export default function Markdown (props) {
  return <ReactMarkdown plugins={[gfm]} {...props} />
}
