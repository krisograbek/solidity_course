import Container from '@mui/material/Container';
import { Config, DAppProvider, Kovan, Rinkeby } from '@usedapp/core';
import React from 'react';
import Header from './components/Header';
import MainLayout from './components/MainLayout';


const config: Config = {
  networks: [Kovan, Rinkeby]
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
