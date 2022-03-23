import { formatUnits } from '@ethersproject/units';
import { CircularProgress } from '@mui/material';
import Box from '@mui/material/Box';
import Button from '@mui/material/Button';
import Input from '@mui/material/Input';
import { useEthers, useNotifications, useTokenBalance } from '@usedapp/core';
import { utils } from 'ethers';
import React, { useEffect, useState } from 'react'
import { useStakeTokens } from '../../hooks';

import { Token } from "../MainLayout"

interface StakeFormProps {
  token: Token
}

function StakeForm({ token }: StakeFormProps) {
  const { address: tokenAddress, name } = token;
  const { account } = useEthers();
  const tokenBallance = useTokenBalance(tokenAddress, account);
  const formattedTokenBallance: number = tokenBallance ? parseFloat(formatUnits(tokenBallance, 18)) : 0;
  const { notifications } = useNotifications();

  const [amount, setAmount] = useState<number | string | Array<number | string>>(0);

  const handleInputChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const newAmount = event.target.value === "" ? "" : Number(event.target.value)
    setAmount(newAmount);
  }

  const { approveAndStake, state: approveAndStakeERC20State } = useStakeTokens(tokenAddress);

  const isMining = approveAndStakeERC20State.status === "Mining";

  const handleStakeSubmit = () => {
    const amountAsWei = utils.parseEther(amount.toString())
    return approveAndStake(amountAsWei.toString())
  }

  useEffect(() => {
    if (notifications.filter((notification) =>
      notification.type === "transactionSucceed" &&
      notification.transactionName === "Approve ERC20 transfer").length > 0) {
      console.log("Approved")
    }
    if (notifications.filter((notification) =>
      notification.type === "transactionSucceed" &&
      notification.transactionName === "Staking tokens").length > 0) {
      console.log("Tokens Staked")
    }
  }, [notifications])

  return (
    <Box>
      <Input onChange={handleInputChange} />
      <Button
        color="primary" size='large'
        onClick={handleStakeSubmit}
        disabled={isMining}
      >
        {isMining ? <CircularProgress size={24} /> : "STAKE!"}
      </Button>
    </Box>
  )
}

export default StakeForm