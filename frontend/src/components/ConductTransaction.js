import React, {useState, useEffect} from 'react';
import { FormGroup, FormControl, Button } from 'react-bootstrap';
import { API_URL } from '../config';
import { Link } from 'react-router-dom';
import NavBar from './NavBar';
import history from '../history';

export function ConductTransaction() {
    const [amount, setAmount] = useState(0);
    const [recipient, setRecipient] = useState('');
    const [knownAddresses, setKnownAddresses] = useState([]);
    const [walletInfo, setWalletInfo] = useState({});

    useEffect(() => {

        fetch(`${API_URL}/wallet/info`)
        .then(response => response.json())
        .then(json => setWalletInfo(json));

        fetch(`${API_URL}/known-addresses`)
        .then(response => response.json())
        .then(json => setKnownAddresses(json));
    }, []);

    const updateRecipient = (event) => {
        setRecipient(event.target.value);
    }

    const updateAmount = (event) => {
        setAmount(Number(event.target.value));
    }

    const submitTransaction = () => {
        fetch(`${API_URL}/wallet/transact`, { method: 'POST', headers: {'Content-Type':'application/json'}, body: JSON.stringify({recipient, amount})})
        .then(response => response.json())
        .then(json => {
            console.log('submitTransaction json', json);
            alert('Submitted!');
            history.push('/transaction-pool');
        })

    }
    const { address, balance } = walletInfo;

    return (
        <div className="ConductTransaction">
            <NavBar />
            <br />
            <h3><b>Conduct a Transaction</b></h3>
            <br />
            <div style={{display: 'flex', justifyContent: 'center', flexDirection: 'column', textAlign: 'center'}}>
            <b>Wallet Address:</b> {address}
            <b>Your Current Wallet Balance:</b> {balance} SBC
            </div>
            <hr />
            <br />
            <FormGroup>
                <FormControl 
                input="text"
                placeholder="recipient"
                value={recipient}
                onChange={updateRecipient}
                />
            </FormGroup>
            <br />
            <FormGroup>
                <FormControl 
                input="number"
                placeholder="amount"
                value={amount}
                onChange={updateAmount}
                />
            </FormGroup>
            <br />
            <div>
                <Button variant="warning" onClick={submitTransaction}>
                    Submit
                </Button>
            </div>
            <br />
            <h4><b>Known Addresses</b></h4>
            <hr />
            <div>
                {
                    knownAddresses.map((knownAddress, i) => (
                        <span key={knownAddress}>
                            <u>{knownAddress}</u>
                            {i !== knownAddresses.length - 1 ? ', ' : ' '}
                            </span>
                    ))
                }
            </div>
        </div>
    )
}