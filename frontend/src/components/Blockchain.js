import React, {useState, useEffect } from 'react';
import { Button } from 'react-bootstrap';
import { API_URL } from '../config';
import { Block } from './Block';
import NavBar from './NavBar';

const PAGE_RANGE = 3;

export function Blockchain() {
    const [blockchain, setBlockchain] = useState([]);
    const [blockchainLength, setBlockchainLength] = useState(0);

    const fetchBlockchainPage = ({start, end}) => {
        fetch(`${API_URL}/blockchain/range?start=${start}&end=${end}`)
        .then(response => response.json())
        .then(json => setBlockchain(json));
    }

    useEffect(() => {
       fetchBlockchainPage({start: 0, end: PAGE_RANGE})

        fetch(`${API_URL}/blockchain/length`)
        .then(response => response.json())
        .then(json => setBlockchainLength(json));
    }, [])

    const buttonNumbers = []
    for (let i=0; i<blockchainLength/PAGE_RANGE; i++) {
        buttonNumbers.push(i);
    }

    return (
        <div className='Blockchain'>
            <NavBar />
            <br />
            <h3><b>Blockchain</b></h3>
            <hr />
            <br />
            <div>{blockchain.map((block) => <Block key={block.hash} block={block}/>)}</div>
            <div>
                {
                    buttonNumbers.map(number => {
                        const start = number * PAGE_RANGE;
                        const end = (number +1) * PAGE_RANGE;
                        return (
                        <span key={number} onClick={() => fetchBlockchainPage({start, end})}>
                            <Button variant="warning">
                                {number + 1}
                            </Button>{' '}
                        </span>
                        )
                    })
                }
            </div>
        </div>
    )
}