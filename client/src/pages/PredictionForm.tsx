import React, { useState, useEffect, ChangeEvent, FormEvent } from "react";
import { Input, Button, Spinner } from "@nextui-org/react";
import { fetchColumns } from "../services/api";

interface FormData {
  [property: string]: string | object;
}

interface InputConfig {
  type: "text" | "number";
  name: string;
}

const PredictionForm: React.FC = () => {
  const [formData, setFormData] = useState<FormData>({});
  const [features, setFeatures] = useState<InputConfig[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const storedModel = localStorage.getItem("model");
        const featuresData: InputConfig[] = await fetchColumns();

        setFeatures(featuresData);

        if (storedModel) {
          const parsedModel: FormData = JSON.parse(storedModel);
          setFormData((prevFormData) => ({
            ...prevFormData,
            model: parsedModel,
          }));
        } else {
          console.log("Model data not found in local storage.");
        }
      } catch (error) {
        console.error("Error fetching data:", error);
      } finally {
        setLoading(false);
      }
    };

    if (features.length === 0) {
      fetchData();
    }
  }, [features]);

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
          {features.map((feature) => (
            <div key={feature.name}>
              <Input
                isRequired
                variant="faded"
                type={feature.type}
                label={feature.name}
                placeholder={feature.name}
                name={feature.name}
                value={formData[feature.name] as string} // Force casting value to string
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
