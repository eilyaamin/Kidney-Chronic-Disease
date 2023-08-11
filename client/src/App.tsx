import React, { useState } from "react";
import "./styles/main.scss";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import LandingPage from "./pages/LandingPage";
import PredictionForm from "./pages/PredictionForm";
import ModelSelection from "./pages/ModelSelection";
import Navigationbar from "./components/Navbar";
import Result from "./pages/Result";


const App = () => {
  return (
    <>
      <BrowserRouter>
        <Navigationbar />
        <Routes>
          <Route path="/" element={<LandingPage />} />
          <Route path="model-selection" element={<ModelSelection />} />
          <Route path="pred-form" element={<PredictionForm />} />
          <Route path="result" element={<Result />} />
        </Routes>
      </BrowserRouter>
    </>
  );
};

export default App;
