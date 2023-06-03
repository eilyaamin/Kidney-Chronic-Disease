import React, { useState } from 'react'
import PropTypes from 'prop-types'

const Dropdown = ({ options }) => {
  const [selectedOption, setSelectedOption] = useState(options[0])

  const handleOptionSelect = (e) => {
    setSelectedOption(e.target.value)
  }

  return (
    <div className="dropdown">
      <label htmlFor="model">
        Choose Model:
      </label>
      <select id="model"
        value={selectedOption}
        onChange={handleOptionSelect}
      >
        {options.map((option, index) => (
          <option
            key={index}
            value={option}
          >
            {option}
          </option>
        ))}
      </select>
    </div>
  )
}

Dropdown.propTypes = {
  options: PropTypes.array.isRequired
}

export default Dropdown
