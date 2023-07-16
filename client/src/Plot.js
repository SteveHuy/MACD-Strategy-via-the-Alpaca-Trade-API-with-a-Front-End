import React, { useState } from 'react';
import "./Plot.css"
import left from "./left.png"
import right from "./right.png"

const Plot = () => {
  const [imageList, setImageList] = useState([]);
  const [currentIndex, setCurrentIndex] = useState(0);

  const generatePlots = async () => {
    try {
      await fetch('/api/plot/generate')
    } catch (error) {
      console.error('Error:', error);
    }
  }

  const fetchImageList = async () => {
    try {
      const response = await fetch('/api/plot/filenames'); // Replace with your backend endpoint URL
      const imageListData = await response.json();
      setImageList(imageListData);
    } catch (error) {
      console.error('Error:', error);
    }
  };

  const handleNextImage = () => {
    setCurrentIndex((prevIndex) => (prevIndex + 1) % imageList.length);
  };

  const handlePreviousImage = () => {
    setCurrentIndex((prevIndex) => (prevIndex - 1 + imageList.length) % imageList.length);
  };

  return (
    <div>
      <div className='container'>
        <button className='generate_button' onClick={generatePlots}>Generate Plots</button>
      </div>
      <div>
        <p>  </p>
      </div>
      <div className='container'>
        <button className='load_button' onClick={fetchImageList}>Load Images</button>
      </div>
      {imageList.length > 0 && (
        <div className='container'>
          <button onClick={handlePreviousImage}>
            <img src={left} alt="Button Left" className='button_image' />
          </button>
          <img src={`plots/${imageList[currentIndex]}`} alt={`plot ${currentIndex + 1}`} />
          <button onClick={handleNextImage}>
            <img src={right} alt="Button Right" className='button_image' />
          </button>
        </div>
      )}
    </div>
  );
};

export default Plot;