import React from 'react';
import { makeStyles } from '@material-ui/core/styles';
import Table from '@material-ui/core/Table';
import TableBody from '@material-ui/core/TableBody';
import TableCell from '@material-ui/core/TableCell';
import TableContainer from '@material-ui/core/TableContainer';
import TableHead from '@material-ui/core/TableHead';
import TableRow from '@material-ui/core/TableRow';
import Paper from '@material-ui/core/Paper';
import Link from '@material-ui/core/Link';


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
  }
}))

export default function DatasetList(props) {
  const baseURL = new URL(window.location.origin);
  const classes = useStyles();

  return (
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
            </TableRow>
          </TableHead>
          <TableBody>
            {props.upload_list.map((row) => (
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
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>
    </div>
  );
}
