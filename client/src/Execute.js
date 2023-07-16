import React, { useState } from 'react';
import "./Execute.css"

const Execute = () => {

    const [message, setMessage] = useState('')

    const execute = async () => {
        try {
            const response = await fetch('/api/execute');
            const executeData = await response.json();
            setMessage(executeData);
        } catch (error) {
            console.error('Error:', error);
        }
    };
    console.log(message)

    return (
        <div>
            <div className='text_container'>
                <p className='text'>Upon execute it will check if the there was a signal on the previous day to make a long position and if so it takes the position based on the ratios shown above.</p>
                <p className='text'>The Notional is equal to the current balance of the account x 0.1 x winrate.</p>
                <p className='text'>The Long Position will have a stop loss based on the stop loss ratio x EMA (200 day moving average) and take profit based on the take profit ratio x stop loss previously calculated</p>
                <p className='text_warning'>Repeatly pressing this button will cause multiple long positions to be taken therefore, do not spam the button.</p>

            </div>
            <div className='button_container'>
            <button className='button_execute' onClick={execute}> Execute </button>

            </div>
            <div className='text_container'>
                {Object.entries(message).map(([name, value]) => (
                    <p className='text' key={name}>
                        {value ? "A Long Position was found for " + name + " and an order has been placed": "No signals were found for " + name}
                    </p>

                ))}
            </div>
        </div>
    )
};


export default Execute;