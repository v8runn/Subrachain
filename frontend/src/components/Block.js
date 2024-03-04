import React, { useState } from "react";
import { Button } from 'react-bootstrap';
import { MILLISECONDS_PY } from "../config";
import { Transaction } from "./Transaction";

function ToggleTransactionDisplay({block}) {
    const [ displayTransaction, setDisplayTransaction ] = useState(false);
    const { data } = block;

    const toggleDisplayTransaction = () => {
        setDisplayTransaction(!displayTransaction);
    }

    if (displayTransaction) {
        return (
            <div>
                {data.map(transaction => (
                    <div key={transaction.id}>
                        <hr />
                        <Transaction transaction={transaction} />
                    </div>
                ))}
                <br />
                <Button
                variant="warning"
                onClick={toggleDisplayTransaction}
                >
                   Show Less 
                </Button>
            </div>
        )
    }

    return (
        <div>
            <br />
            <Button
            variant="warning"
            onClick={toggleDisplayTransaction}
            >Show More</Button>
        </div>
    )
}

export function Block({ block }) {
    const { timestamp, hash } = block;
    const hashDisplay = `${hash.substring(0, 15)}...`;
    const timestampDisplay = new Date(timestamp / MILLISECONDS_PY).toLocaleString();

    return (
        <div className="Block">
            <div><b>Hash:</b> {hashDisplay}</div>
            <div><b>Timestamp:</b> {timestampDisplay}</div>
            <ToggleTransactionDisplay block={block}/>
        </div>
    )
}