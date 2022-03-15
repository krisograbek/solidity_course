import Button from '@mui/material/Button';
import makeStyles from '@mui/styles/makeStyles';
import { useEthers } from '@usedapp/core'
import React from 'react'


const useStyles = makeStyles((theme) => ({
  container: {
    padding: 32,
    display: "flex",
    justifyContent: "flex-end",
    gap: 8
  }
}))


function Header() {
  const classes = useStyles();
  const { account, activateBrowserWallet, deactivate } = useEthers();

  const isConnected = account !== undefined;

  return (
    <div className={classes.container}>
      {isConnected ? (
        <Button color='primary' variant='contained' onClick={deactivate}>
          Disconnect
        </Button>
      ) : (
        <Button color='primary' variant='contained' onClick={() => activateBrowserWallet()}>
          Connect
        </Button>
      )
      }
    </div>
  )
}

export default Header
