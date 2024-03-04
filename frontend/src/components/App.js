import React, {useState, useEffect} from 'react';
import { NavBar } from './NavBar';
import logo from '../assets/logo.png';
import hello from './hello.json';
import { API_URL } from '../config';

function App() {
  const [walletInfo, setWalletInfo] = useState({});
  const [greeting, setGreeting] = useState('');

  const getRandomGreeting = () => {
    const randomIndex = Math.floor(Math.random() * hello.length);
    return hello[randomIndex];
  }

  useEffect(() => {
    fetch(`${API_URL}/wallet/info`)
    .then(response => response.json())
    .then(json => setWalletInfo(json));

    const selectedGreeting = getRandomGreeting();
    setGreeting(selectedGreeting.hello);
  }, [])

  const { address, balance } = walletInfo;

  return (
    <div className="App">
      <NavBar />
      <img className='logo' src={logo} alt="logo"/>
      <h3><i><b>"{greeting}"</b></i></h3>
      <br />
      <br />
      <div>
            <div><b>Wallet Address:</b> {address}</div>
            <div><b>Your Current Wallet Balance:</b> {balance} SBC</div>
            </div>
    </div>
  );
}

export default App;
