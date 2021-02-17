import {createMuiTheme} from '@material-ui/core/styles'


const self_grey = "#b5b7b9";
const self_orange = "#f0983a";
const self_blue = "#4490db";

export default createMuiTheme({
    palette: {
        common: {
            blue: `${self_blue}`,
            orange: `${self_orange}`,
            grey: `${self_grey}`
        },
        primary: {
            main: `${self_grey}`
        },
        secondary: {
            main: `${self_orange}`
        }
    }
})