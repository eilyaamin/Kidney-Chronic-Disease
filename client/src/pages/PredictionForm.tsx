import React, { useState, useEffect, ChangeEvent, FormEvent } from "react";
import { Input, Button, Spinner } from "@nextui-org/react";
import { fetchColumns } from "../services/api";

interface FormData {
  [property: string]: string;
}

interface InputConfig {
  type: "text" | "number";
  name: string;
}

interface ModelConfig {
  name: string;
  description: string;
  accuracy: string;
}

interface Feature {
  name: string;
  type: string;
}

const PredictionForm: React.FC = () => {
  const [formData, setFormData] = useState<FormData>({});
  const [columns, setColumns] = useState<Feature[]>([]); // Update the type here
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const storedModel = localStorage.getItem("model");

    if (storedModel) {
      const parsedModel: ModelConfig = JSON.parse(storedModel);
      console.log(parsedModel);
    } else {
      console.log("Model data not found in local storage.");
    }
  }, []);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const modelData: Feature[] = await fetchColumns(); // Update the type here
        setColumns(modelData);
      } catch (error) {
        console.error("Error fetching data:", error);
      } finally {
        setLoading(false);
      }
    };

    if (columns.length === 0) {
      fetchData();
    }
  }, [columns]);

  const handleChange = (e: ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setFormData((prevFormData) => ({
      ...prevFormData,
      [name]: value,
    }));
  };

  const handleSubmit = (e: FormEvent) => {
    e.preventDefault();
    console.log(formData);
  };

  return (
    <div className="pred-form">
      {loading ? (
        <Spinner />
      ) : (
        <form onSubmit={handleSubmit}>
          {columns.map((input) => (
            <div key={input.name}>
              <Input
                variant="faded"
                type={input.type}
                label={input.name}
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
