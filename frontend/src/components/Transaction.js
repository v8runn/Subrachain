import React from 'react';

export function Transaction({ transaction }) {
    const { input, output } = transaction;
    const recipients = Object.keys(output);

    return (
        <div className='Transaction'>
            <div key={recipients}><b>From</b>: {input.address}</div>
            {recipients.map((recipient) => (
                <div><b>To:</b> {recipient} | <b>Sent:</b> {output[recipient]}</div>
            ))}
        </div>
    )
}