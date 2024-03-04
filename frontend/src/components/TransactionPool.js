import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { Transaction } from './Transaction';
import { API_URL, SECONDS_JS } from '../config';
import { Button } from 'react-bootstrap';
import history from '../history';
import NavBar from './NavBar';

const POLL_INTERVAL = 10 * SECONDS_JS;


export function TransactionPool() {
    const [transactions, setTransactions] = useState([]);

    const fetchTransaction = () => {
        fetch(`${API_URL}/transactions`)
        .then(response => response.json())
        .then(json => {
            console.log('transaction pool', json);
            setTransactions(json)});
    }

    useEffect(() => {
        fetchTransaction()

        const intervalId = setInterval(fetchTransaction, POLL_INTERVAL);

        return () => clearInterval(intervalId);
    }, []);

    const fetchMineBlock = () => {
        fetch(`${API_URL}/blockchain/mine`)
        .then(() => {
            alert('Transaction mined!');

            history.push('/blockchain');
        })
    }

    return (
        <div className='TransactionPool'>
            <NavBar />
            <br />
            <h3><b>Transaction Pool</b></h3>
            <h5><i>*You will be rewarded with 50 SBC for every transaction you mine</i></h5>
            <div>
                {transactions.map(transaction => (
                    <div key={transaction.id}>
                        <hr />
                        <Transaction transaction={transaction}/>
                    </div>
                ))}
            </div>
            <hr />
            <Button variant="warning" onClick={fetchMineBlock}>Mine a block</Button>
        </div>
    )
}
