import React, { useState } from 'react';
import './SliderComponent.css';
import Slider from 'react-slider';

const MIN = 100;
const MAX = 100000;

function SliderComponent({ setPriceFilter }) {
  const [values, setValues] = useState([MIN, MAX]);

  const handleSliderChange = (newValues) => {
    setValues(newValues);
    setPriceFilter(newValues);
  };

  return (
    <div className='Slider-Component'>
      <div className='box'>
        <p className='slider-h3'>
          Price <span>Range:</span>
        </p>
        <div className='small-box'>
          <div>
            <span className={'values'}>£{values[0]} - £{values[1]}</span>
          </div>
          <small className='small-current'>Current Range: £{values[1] - values[0]}</small>
        </div>
        <Slider
          className={'slider'}
          onChange={handleSliderChange}
          value={values}
          min={MIN}
          max={MAX}
        />
      </div>
    </div>
  );
}

export default SliderComponent;
