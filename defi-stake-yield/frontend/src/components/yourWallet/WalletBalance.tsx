import { formatUnits } from '@ethersproject/units';
import Typography from '@mui/material/Typography';
import { useEthers, useTokenBalance } from '@usedapp/core';
import React from 'react'
import { Token } from '../MainLayout'
import BallanceMessage from './BallanceMessage';

interface WalletBallanceProps {
  token: Token
}

function WalletBalance({ token }: WalletBallanceProps) {
  const { img, address, name } = token;
  const { account } = useEthers();
  const tokenBalance = useTokenBalance(address, account);
  // console.log(tokenBalance?.toString())
  const formattedTokenBallance: number = tokenBalance ? parseFloat(formatUnits(tokenBalance, 18)) : 0;

  return (
    <BallanceMessage
      label={`Your un-staked ${name} balance`}
      amount={formattedTokenBallance}
      imgSrc={img}
    />
  )
}

export default WalletBalance