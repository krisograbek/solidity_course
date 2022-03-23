import TabPanel from '@mui/lab/TabPanel';
import TabContext from '@mui/lab/TabContext';
import TabList from '@mui/lab/TabList';
import Box from '@mui/material/Box';
import Tab from '@mui/material/Tab';
import Typography from '@mui/material/Typography';
import React, { useState } from 'react';
import { Token } from '../MainLayout';
import WalletBalance from './WalletBalance';
import StakeForm from './StakeForm';

interface YourWalletProps {
  supportedTokens: Array<Token>
}

export function YourWallet({ supportedTokens }: YourWalletProps) {
  const [selectedTokenIndex, setSelectedTokenIndex] = useState<number>(0);

  const handleOnChange = (event: React.ChangeEvent<{}>, newValue: string) => {
    setSelectedTokenIndex(parseInt(newValue))
  }

  return (
    <Box>
      <Typography variant='h3'>This is Your Wallet</Typography>
      <Box>
        <TabContext value={selectedTokenIndex.toString()}>
          <TabList onChange={handleOnChange} >
            {supportedTokens.map((token, index) => {
              return (
                <Tab label={token.name} value={index.toString()} key={index} />
              )
            })}
          </TabList>
          {supportedTokens.map((token, index) => {
            return (
              <TabPanel value={index.toString()} key={index} >
                <WalletBalance token={supportedTokens[selectedTokenIndex]} />
                <StakeForm token={supportedTokens[selectedTokenIndex]} />
              </TabPanel>
            )
          })}
        </TabContext>
      </Box>
    </Box>
  )
}

// export default YourWallet;