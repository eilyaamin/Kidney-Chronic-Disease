import React, { useState, useEffect } from "react";
import { Input, Button, Spinner } from "@nextui-org/react";


interface FormData {
  [property: string]: string;
}

interface InputConfig {
  label: string;
  type: "text" | "number";
  name: string;
}

const PredictionForm: React.FC = () => {
  const [formData, setFormData] = useState<FormData>({});
  const [columns, setColumns] = useState<InputConfig[]>([]);

  useEffect(() => {
    const storedModel = localStorage.getItem("model");
  
    if (storedModel) {
      const parsedModel = JSON.parse(storedModel);
      console.log(parsedModel);
    } else {
      console.log("Model data not found in local storage.");
    }
  }, []);
  

  // Commented out the fetchData block for now
  // useEffect(() => {
  //   const fetchData = async () => {
  //     try {
  //       const modelData: ModelData = await fetchModelsData();
  //       const inputConfigs: InputConfig[] = Object.values(modelData).map(
  //         (model) => ({
  //           label: model.name,
  //           type: "text",
  //           name: model.name,
  //         })
  //       );
  //       setColumns(inputConfigs);
  //     } catch (error) {
  //       console.error("Error fetching data:", error);
  //     }
  //   };
  //   if (columns.length === 0) {
  //     fetchData();
  //   }
  // }, []);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setFormData((prevFormData) => ({
      ...prevFormData,
      [name]: value,
    }));
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    console.log(formData);
  };

  return (
    <div className="pred-form">
      {columns.length === 0 ? (
        <Spinner />
      ) : (
        <form onSubmit={handleSubmit}>
          {columns.map((input) => (
            <div key={input.name}>
              <Input
                variant="faded"
                type={input.type}
                label={input.label}
                placeholder={input.name}
                name={input.name}
                value={formData[input.name] || ""}
                onChange={handleChange}
              />
            </div>
          ))}
          <Button type="submit">Show Results</Button>
        </form>
      )}
    </div>
  );
};

export default PredictionForm;
