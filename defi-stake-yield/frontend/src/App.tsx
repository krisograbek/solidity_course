import Container from '@mui/material/Container';
import { Config, DAppProvider, Kovan } from '@usedapp/core';
import React from 'react';
import Header from './components/Header';
import MainLayout from './components/MainLayout';


const config: Config = {
  networks: [Kovan],
  // every second, check our blockchain
  // if there are any transactions
  notifications: {
    expirationPeriod: 1000,
    checkInterval: 1000
  }
}

function App() {
  return (
    <DAppProvider config={config}>
      <Header />
      <Container maxWidth="md">
        <MainLayout />
      </Container>
    </DAppProvider>
  );
}

export default App;
