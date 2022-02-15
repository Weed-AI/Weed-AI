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


const CardSelector = ({ classes, cardData, selected, handleSelect }) => {
  return (
    <Grid container spacing={2}>
      {cardData.map(card => (
        <Grid item key={card.id} xs={12} md={4}>
          <Card
            onClick={() => { handleSelect(card.id) }}
            role="button"
            aria-pressed={card.id == selected ? "true" : "false"}
            aria-label={card.name}
            className={classes.card + " " + (card.id == selected ? classes.selected : "")}
          >
            <CardContent>
              <Typography variant="h5" component="div">
               {card.name}
              </Typography>
              {card.description}
            </CardContent>
          </Card>
        </Grid>
      ))}
    </Grid>
  )
}


export default withStyles(useStyles)(CardSelector);
