export const useArticleStyles = (theme) => ({
    page: {
        marginTop: theme.spacing(10),
		marginLeft: "auto",
		marginRight: "auto",
        fontSize: "1.1rem",
        maxWidth: 900,
		lineHeight: "150%",
        '@media (max-width: 1000px)': {
          margin: theme.spacing(4),
          fontSize: "1.3rem",
        },
    },
})
