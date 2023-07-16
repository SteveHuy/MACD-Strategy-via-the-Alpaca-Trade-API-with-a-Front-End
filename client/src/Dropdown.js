import React, { useState, useEffect } from 'react';
import "./Dropdown.css"

const Dropdown = () => {
  const [options, setOptions] = useState([]);
  const [selectedValue, setSelectedValue] = useState('');
  const [stats, setStats] = useState([]);
  const [message, setMessage] = useState('')

  const addStock = async () => {
    try {
      const response = await fetch('/api/stocks/add', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ selectedValue })
      });
  
      if (!response.ok) {
        throw new Error('Request failed'); 
      }
  
      const responseData = await response.json();
      setMessage(responseData)
      console.log(message); // Log the response data
    } catch (error) {
      console.error(error); // Handle error if the request fails
    }
  };

  const removeStock = async () => {
    try {
      const response = await fetch('/api/stocks/remove', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ selectedValue })
      });
  
      if (!response.ok) {
        throw new Error('Request failed'); 
      }
  
      const responseData = await response.json();
      setMessage(responseData)
      console.log(message); // Log the response data
    } catch (error) {
      console.error(error); // Handle error if the request fails
    }
  };


  const getStats = async () => {
    try {
      const response = await fetch('/api/stocks/stat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(selectedValue),
      });

      const statsResponse = await response.json();
      setStats(statsResponse);
      console.log(stats)
    } catch (error) {
      console.error('Error:', error);
    }
  };


  useEffect(() => {
    fetchOptions()
  }, []);


  const fetchOptions = async () => {
    try {
      const response = await fetch('/api/stocks'); 
      const optionsData = await response.json();
      setOptions(optionsData);
    } catch (error) {
      console.error('Error:', error);
    }
  };
  console.log(options)



  return (
    <div>
      <div className="dropdown_container">

        <select className='dropdown' value={selectedValue} onChange={(e) => setSelectedValue(e.target.value)}>
          <option value="">Select an option</option>
          {Object.keys(options).map((option) => (
            <option key={option} value={option}>
              {options[option]}
            </option>
          ))}
        </select>
      </div>
      <div className='button_container'>
        <button className='button_sell' onClick={removeStock}>Remove Stock</button>
        <button className='button_stats' onClick={getStats}>Get Stats</button>
        <button className='button_buy' onClick={addStock}>Add Stock</button>
      </div>
      <div className='message_container'>
        <p className='text'>{message.message}</p>
      </div>
      <div className='stats_container'>
        <p className='text'>Winrate: {stats.winrate * 100}%</p>
        <p className='text'>Money Made: {stats.money} USD</p>
      </div>

    </div>
  );
};



export default Dropdown;