import React, { useEffect, useState } from "react";

const ResultPage: React.FC = () => {
  const [prediction, setPrediction] = useState<string | null>(null);

  useEffect(() => {
    // Retrieve the prediction value from localStorage
    const storedPrediction = localStorage.getItem("prediction");

    if (storedPrediction) {
      setPrediction(storedPrediction);
    }

    localStorage.removeItem("prediction");
  }, []);

  const positiveText = (
    <div>
      <h2>Positive Case</h2>
      <p>
        Your prediction result suggests that you may have Chronic Kidney
        Disease.
      </p>
      <p>
        It is important to consult a healthcare professional for further
        evaluation and advice.
      </p>
    </div>
  );

  const negativeText = (
    <div>
      <h2>Negative Case</h2>
      <p>
        Your prediction result indicates that you do not have Chronic Kidney
        Disease.
      </p>
      <p>
        Remember to maintain a healthy lifestyle and regular medical check-ups
        to stay well.
      </p>
    </div>
  );

  return (
    <div>
      <h1>Chronic Kidney Disease Prediction Result</h1>
      {prediction !== null ? (
        <div>{prediction === "1" ? positiveText : negativeText}</div>
      ) : (
        <p>No prediction available.</p>
      )}
    </div>
  );
};

export default ResultPage;
