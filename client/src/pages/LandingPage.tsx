import { Button } from "@nextui-org/react";
import { useNavigate } from "react-router-dom";

const LandingPage = () => {
  const navigate = useNavigate();

  const handleButtonClick = () => {
    // Perform any necessary logic here (if needed)
    // Redirect to a specific route using navigate()
    navigate("/model-selection");
  };
  return (
    <div className="landing-pg">
      <label className="title">Welcome to Personal Chronic Kidney Disease Risk Estimator</label>
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
      <div>
        <Button size="lg" color="primary" onPress={handleButtonClick}>
          Get Started
        </Button>
      </div>
    </div>
  );
};

export default LandingPage;
