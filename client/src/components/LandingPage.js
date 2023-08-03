import React from 'react'
import Dropdown from './DropDown'

function Test () {
  return (
    <div className="landing-pg">
      <Dropdown
        options={[
          'Decision Tree',
          'Random Forest',
          'Logistic Regression',
          'Neural Network'
        ]}
      />
      <h1>Welcome to Personal Chronic Kidney Disease Risk Estimator</h1>
      <p>
        The Chronic Kidney Disease Estimator is a powerful web-based tool
        designed to provide you with an accurate assessment of your risk for
        developing chronic kidney disease (CKD). This user-friendly application
        utilizes advanced algorithms and cutting-edge medical research to
        analyze your unique set of factors and deliver personalized risk
        estimates.
        <br />
        <br />
        With the Chronic Kidney Disease Estimator, you can gain valuable
        insights into your kidney health and make informed decisions to
        safeguard your well-being. By inputting key information such as your
        medical history, lifestyle choices, and existing health conditions, our
        estimator calculates your individual risk profile and provides you with
        a clear understanding of your likelihood of developing CKD.
        <br />
        <br />
        Ready to assess your risk for chronic kidney disease? Take control of
        your kidney health today with the Chronic Kidney Disease Estimator.
        Discover your risk level, identify potential areas for improvement, and
        embark on a path towards proactive kidney care.
        <br />
        <br />
        Click below to start using the Chronic Kidney Disease Estimator and gain
        valuable insights into your kidney health. Take control of your
        well-being and make informed decisions for a healthier future.
        <br />
        <br />
      </p>
      <button>Get Started</button>
    </div>
  )
}

export default Test
