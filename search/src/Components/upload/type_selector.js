import React from 'react';
import Grid from '@material-ui/core/Grid';
import Card from '@material-ui/core/Card';
import CardActionArea from '@material-ui/core/CardActionArea';
import CardContent from '@material-ui/core/CardContent';
import Typography from '@material-ui/core/Typography';
import { withStyles } from '@material-ui/core/styles';

const useStyles = (theme) => ({
    card: {
      "&:hover": {
        backgroundColor: theme.palette.primary.light,
      },
      cursor: "pointer",
    },
    selected: {
      backgroundColor: theme.palette.secondary.light,
      "&:hover": {
        backgroundColor: theme.palette.secondary.main,
      },
    },
  });


const typeData = [
  {
    "id": "weedcoco",
    "name": "WeedCOCO",
    "description": <Typography>Weed-AI's custom extension of MS COCO with everything included.</Typography>
  },
  {
    "id": "coco",
    "name": "MS COCO",
    "description": <Typography>MS COCO format for classification, bounding boxes or segmentation.</Typography>
  },
  {
    "id": "voc",
    "name": "Pascal VOC",
    "description": <Typography>Pascal VOC's XML annotation format for bounding boxes.</Typography>
  },
  {
    "id": "masks",
    "name": "Mask PNGs",
    "description": <Typography>Colour coded mask images for segmentation.</Typography>
  },
]

const TypeSelector = ({ classes, uploadType, handleSelect }) => {
  return (
    <div>
      <Typography gutterBottom variant="subtitle1" component="div">
        Select an input annotation format:
      </Typography>
      <Grid container spacing={2}>
        {typeData.map(type => (
          <Grid item key={type.id} xs={12} md={4}>
            <Card
              onClick={() => { handleSelect(type.id) }}
              role="button"
              aria-pressed={type.id == uploadType ? "true" : "false"}
              aria-label={type.name}
              className={classes.card + " " + (type.id == uploadType ? classes.selected : "")}
            >
              <CardContent>
                <Typography variant="h5" component="div">
                 {type.name}
                </Typography>
                {type.description}
              </CardContent>
            </Card>
          </Grid>
        ))}
      </Grid>
    </div>
  )
}


export default withStyles(useStyles)(TypeSelector);
