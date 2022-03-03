import CircularProgress from '@material-ui/core/CircularProgress';
import IconButton from '@material-ui/core/IconButton';
import Link from '@material-ui/core/Link';
import Paper from '@material-ui/core/Paper';
import { makeStyles } from '@material-ui/core/styles';
import Table from '@material-ui/core/Table';
import TableBody from '@material-ui/core/TableBody';
import TableCell from '@material-ui/core/TableCell';
import TableContainer from '@material-ui/core/TableContainer';
import TableHead from '@material-ui/core/TableHead';
import TableRow from '@material-ui/core/TableRow';
import PhotoIcon from '@material-ui/icons/Photo';
import axios from 'axios';
import React, { useState } from 'react';
import { Helmet } from "react-helmet";
import UploadDialog from '../upload/upload_dialog';


const useStyles = makeStyles((theme) => ({
  table: {
    minWidth: 650,
  },
  root: {
    margin: theme.spacing(10)
  },
  tableHeader: {
    fontWeight: 700,
    fontSize: '1.2rem'
  },
  command: {
    padding: '0.5em',
    marginRight: '1em',
    color: 'white',
    border: 'none',
    borderRadius: '6px',
    '&:hover': {
      cursor: 'pointer'
    }
    
  },
  approval: {
    backgroundColor: 'green'
  },
  reject: {
    backgroundColor: 'red'
  },
  commandCol: {
    display: 'flex'
  }
}))

export default function DatasetList(props) {
  const inReview = props.inReview;  // should we list 
  const baseURL = new URL(window.location.origin);
  const classes = useStyles();
  const [loading, setLoading] = useState(false);

  const handleApprove = (upload_id) => {
    setLoading(true)
    axios.get(`/api/dataset_approve/${upload_id}`)
         .then(window.location.reload.bind(window.location))
         .catch(err => {
           console.log(err)
           setLoading(false)
         })
  }
  
  const handleReject = (upload_id) => {
    setLoading(true)
    axios.get(`/api/dataset_reject/${upload_id}`)
         .then(window.location.reload.bind(window.location))
         .catch(err => {
           console.log(err)
           setLoading(false)
         })
  }

  return (
    <div className={classes.root}>
      <Helmet>
        <title>Datasets - Weed-AI</title>
        <meta name="description" content="All datasets in Weed-AI with annotated images and metadata for download." />
      </Helmet>
      <h2>{props.title}</h2>
      <TableContainer component={Paper}>
        <Table className={classes.table} aria-label="simple table">
          <TableHead>
            <TableRow>
              <TableCell className={classes.tableHeader}>Dataset Title</TableCell>
              {inReview ? <TableCell className={classes.tableHeader}>Contact</TableCell> : ""}
              <TableCell className={classes.tableHeader}>Upload Date</TableCell>
              <TableCell className={classes.tableHeader}>Explore</TableCell>
              <TableCell className={classes.tableHeader}>Edit</TableCell>
              {inReview ? <TableCell className={classes.tableHeader}>Command</TableCell> : ""}
            </TableRow>
          </TableHead>
          <TableBody>
            {props.upload_list.map((row) => (
              <TableRow key={row.upload_id}>
                <TableCell component="th" scope="row">
                <Link href={baseURL + 'datasets/' + row.upload_id} color='blue'>
                  {row.name}
                </Link>
                </TableCell>
                {inReview ? <TableCell><a href="mailto:{row.contributor_email}">{row.contributor_email}</a></TableCell> : ""}
                <TableCell>{row.upload_date}</TableCell>
                <TableCell><IconButton href={"/explore?dataset_name_filter=%5B%22" + row.name + "%22%5D"}><PhotoIcon /></IconButton></TableCell>
                <TableCell>
                  {row.editable
                  ?<UploadDialog upload_mode={'edit'} upload_id={row.upload_id}/>
                  : ""}
                </TableCell>
                {inReview
                  ?<TableCell className={classes.commandCol}>
                    <button className={`${classes.command} ${classes.approval}`} onClick={() => handleApprove(row.upload_id)}>Approve</button>
                    <button className={`${classes.command} ${classes.reject}`} onClick={() => handleReject(row.upload_id)}>Reject</button>
                    {loading ? <CircularProgress style={{height: "2em", width: "2em"}}/> : ""}
                  </TableCell>
                  :""}
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>
    </div>
  )
}
