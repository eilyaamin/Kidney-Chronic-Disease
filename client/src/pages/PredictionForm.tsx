import React, { useState, useEffect } from "react";
import { Input, Button, Spinner } from "@nextui-org/react";
import fetchModelsData from "../services/api";

interface FormData {
  [property: string]: string;
}

interface InputConfig {
  label: string;
  type: "text" | "number";
  name: string;
}

interface ModelData {
  [modelName: string]: {
    id: number;
    name: string;
    accuracy: string;
  };
}

const PredictionForm: React.FC = () => {
  const [formData, setFormData] = useState<FormData>({});
  const [columns, setColumns] = useState<InputConfig[]>([]);

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
      [name]: value.toString(),
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
        <>
          <form onSubmit={handleSubmit}>
            {columns?.map((input) => (
              <div key={input.name}>
                <Input
                  variant={"faded"}
                  type={input.type}
                  label={input.label}
                  placeholder={input.name}
                  name={input.name}
                  value={formData[input.name] || ""}
                  onChange={handleChange}
                />
              </div>
            ))}
            <Button isDisabled={false} type="submit">
              Show Results
            </Button>
          </form>
        </>
      )}
    </div>
  );
};

export default PredictionForm;
