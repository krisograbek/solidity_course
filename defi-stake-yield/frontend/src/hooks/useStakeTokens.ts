import { useContractFunction, useEthers } from "@usedapp/core"
import { constants, utils } from "ethers";
import TokenFarm from "../chain-info/contracts/TokenFarm.json"
import ERC20 from "../chain-info/contracts/MockERC20.json"
import networkMapping from "../chain-info/deployments/map.json"
import { Contract } from '@usedapp/core/node_modules/@ethersproject/contracts'
import { useEffect, useState } from "react";

export const useStakeTokens = (tokenAddress: string) => {
  // We need to approve before we can stake. To do this
  // let's grab: token Farm address, abi, and chainId

  const { chainId } = useEthers();
  // getting token Farm contract...
  // token Farm ABI
  const { abi } = TokenFarm;
  // token Farm address
  const tokenFarmAddress = chainId ? networkMapping[String(chainId)]["TokenFarm"][0] : constants.AddressZero;
  // token Farm Interface
  const tokenFarmInterface = new utils.Interface(abi);
  const tokenFarmContract = new Contract(tokenFarmAddress, tokenFarmInterface);

  // getting dapp Token Contract...
  const erc20abi = ERC20.abi;
  const erc20Interface = new utils.Interface(erc20abi);
  const erc20Contract = new Contract(tokenAddress, erc20Interface);

  // approve
  const { send: approveERC20Send, state: approveAndStakeERC20State } =
    useContractFunction(erc20Contract, "approve", { transactionName: "Approve ERC20 transfer" })

  const approveAndStake = (amount: string) => {
    // set the amount we want to stake
    // we do it before calling the approve
    // it's safe, because we stake only if approve is successful
    setAmountToStake(amount);
    // call Solidity's approve
    // it takes 2 parameters: spender and amount
    return approveERC20Send(tokenFarmAddress, amount) // why aren't we converting?
  }

  const { send: stakeSend, state: stakeState } = useContractFunction(
    tokenFarmContract, "stakeTokens", { transactionName: "Staking tokens" })


  const [amountToStake, setAmountToStake] = useState("0");

  useEffect(() => {
    if (approveAndStakeERC20State.status === "Success") {
      // send stake
      // this is stakeTokens in TokenFarm.sol
      stakeSend(amountToStake, tokenAddress)
    }
  }, [approveAndStakeERC20State]) // wait for status to change

  const [state, setState] = useState(approveAndStakeERC20State);

  useEffect(() => {
    if (approveAndStakeERC20State.status === "Success") {
      setState(stakeState)
    }
    else {
      setState(approveAndStakeERC20State)
    }
  }, [approveAndStakeERC20State, stakeState])


  return { approveAndStake, state }

}