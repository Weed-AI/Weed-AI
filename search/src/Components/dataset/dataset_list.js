import React, { useState } from 'react';
import { makeStyles } from '@material-ui/core/styles';
import Table from '@material-ui/core/Table';
import TableBody from '@material-ui/core/TableBody';
import TableCell from '@material-ui/core/TableCell';
import TableContainer from '@material-ui/core/TableContainer';
import TableHead from '@material-ui/core/TableHead';
import TableRow from '@material-ui/core/TableRow';
import Paper from '@material-ui/core/Paper';
import Link from '@material-ui/core/Link';
import CircularProgress from '@material-ui/core/CircularProgress';
import axios from 'axios';


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

  const datalist_table = (table_list, command) => (
    <div className={classes.root}>
      <TableContainer component={Paper}>
        <Table className={classes.table} aria-label="simple table">
          <TableHead>
            <TableRow>
              <TableCell className={classes.tableHeader}>Dataset Title</TableCell>
              <TableCell className={classes.tableHeader}>Task Type</TableCell>
              <TableCell className={classes.tableHeader}>Crop</TableCell>
              <TableCell className={classes.tableHeader}>Weed Species</TableCell>
              <TableCell className={classes.tableHeader}>Contributor</TableCell>
              <TableCell className={classes.tableHeader}>Upload Date</TableCell>
              {command ? <TableCell className={classes.tableHeader}>Command</TableCell> : ""}
            </TableRow>
          </TableHead>
          <TableBody>
            {table_list.map((row) => (
              <TableRow key={row.name}>
                <TableCell component="th" scope="row">
                <Link href={baseURL + 'datasets/' + row.upload_id} color='blue'>
                  {row.name}
                </Link>
                </TableCell>
                <TableCell>Classification</TableCell>
                <TableCell>Pasture</TableCell>
                <TableCell></TableCell>
                <TableCell>{row.contributor}</TableCell>
                <TableCell>{row.upload_date}</TableCell>
                {command
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

  return (
    <React.Fragment>
      {datalist_table(props.upload_list, false)}
      {props.is_staff ? datalist_table(props.awaiting_list, true) : ""}
    </React.Fragment>
  );
}
