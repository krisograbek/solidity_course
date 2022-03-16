import { useEthers } from '@usedapp/core'
import { constants } from "ethers"
import React from 'react'
import networkMapping from "../chain-info/deployments/map.json"
import helperConfig from "../helper-config.json"
import brownieConfig from "../brownie-config.json"
import dappImg from "../dapp.png"
import daiImg from "../dai.png"
import ethImg from "../eth.png"
import { YourWallet } from './yourWallet'

export type Token = {
  img: string
  address: string
  name: string
}


function MainLayout() {
  const { chainId } = useEthers();
  const networkName = chainId ? helperConfig[chainId] : "dev";

  const dappTokenAddress = chainId ? networkMapping[String(chainId)]["DappToken"][0] : constants.AddressZero;
  const wethTokenAddress = chainId ? brownieConfig["networks"][networkName]["weth_token"] : constants.AddressZero;
  const daiTokenAddress = chainId ? brownieConfig["networks"][networkName]["dai_token"] : constants.AddressZero;

  const supportedTokens: Array<Token> = [
    {
      img: dappImg,
      address: dappTokenAddress,
      name: "DAPP"
    },
    {
      img: daiImg,
      address: daiTokenAddress,
      name: "DAI"
    },
    {
      img: ethImg,
      address: wethTokenAddress,
      name: "WETH"
    }
  ]

  return (
    <YourWallet supportedTokens={supportedTokens} />
  )
}

export default MainLayout