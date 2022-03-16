import { formatUnits } from '@ethersproject/units';
import Box from '@mui/material/Box';
import Button from '@mui/material/Button';
import Input from '@mui/material/Input';
import { useEthers, useTokenBalance } from '@usedapp/core';
import React, { useState } from 'react'

import { Token } from "../MainLayout"

interface StakeFormProps {
  token: Token
}

function StakeForm({ token }: StakeFormProps) {
  const { address, name } = token;
  const { account } = useEthers();
  const tokenBallance = useTokenBalance(address, account);
  const formattedTokenBallance: number = tokenBallance ? parseFloat(formatUnits(tokenBallance, 18)) : 0;

  const [amount, setAmount] = useState<number | string | Array<number | string>>(0);

  const handleInputChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const newAmount = event.target.value === "" ? "" : Number(event.target.value)
    setAmount(newAmount);
  }

  return (
    <Box>
      <Input onChange={handleInputChange} />
      <Button color="primary" size='large'>Stake!</Button>
    </Box>
  )
}

export default StakeForm