import React, { useState } from 'react';
import "./Stats.css"

const Stats = () => {
    const [data, setData] = useState([]);
    const [averageData, setAverageData] = useState([]);


    const getStats = async () => {
        try {
            const response = await fetch('/api/stocks/stats');
            const responseData = await response.json();
            setData(responseData)
        } catch (error) {
            console.error('Error:', error);
        }

    };

    const getStatsAverage = async () => {
        try {
            const response = await fetch('/api/stocks/stat/average');
            const responseData = await response.json();
            setAverageData(responseData)
        } catch (error) {
            console.error('Error:', error);
        }

    };

    const handleStats = () => {
        getStats();
        getStatsAverage();
    }
    return (
        <div>
            <div className='button_container'>
                <button className='button_stat' onClick={handleStats}>Load Stats</button>
            </div>
            {data.map((item, index) => (
                <div className='button_container' key={index}>
                    <p className='text'>{index + 1}: {item.name} ({item.symbol}): Winrate: {item.winrate}%  Money Made: {item.money_made} USD  Take Profit Ratio: {item.profit_take}  Stop Loss Ratio: {item.stop_loss}</p>
                </div>
            ))}
            <div className='button_container'>
            <p className='text'>Average Money Made: {averageData.money_made} USD Average Winrate: {averageData.winrate * 100}%</p>
            </div>
        </div>
    );

}

export default Stats;