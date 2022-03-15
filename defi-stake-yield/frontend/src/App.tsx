import { ChainId, Config, DAppProvider, Kovan, Rinkeby } from '@usedapp/core';
import Container from '@mui/material/Container';
import React from 'react';
import Header from './components/Header';


const config: Config = {
  networks: [Kovan, Rinkeby]
}

function App() {
  return (
    <DAppProvider config={config}>
      <Header />
      <Container maxWidth="md">
        <div>Hi</div>
      </Container>
    </DAppProvider>
  );
}

export default App;
