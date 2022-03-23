import Typography from '@mui/material/Typography'
import Box from '@mui/material/Box'
import React from 'react'
import makeStyles from '@mui/styles/makeStyles'

interface BallanceMessageProps {
  label: string
  amount: number
  imgSrc: string
}

const useStyles = makeStyles(() => ({
  container: {
    display: "inline-grid",
    gridTemplateColumns: "auto auto auto",
    gap: 8,
    alignItems: "center"
  },
  tokenImg: {
    width: 32
  },
  amount: {
    fontWeight: 700
  }
}))

function BallanceMessage({ label, amount, imgSrc }: BallanceMessageProps) {
  const classes = useStyles();
  return (
    <Box className={classes.container}>
      <Typography>{label}</Typography>
      <Typography variant="h4" className={classes.amount}>{amount}</Typography>
      <img className={classes.tokenImg} src={imgSrc} alt="token Logo" />
    </Box>
  )
}

export default BallanceMessage