import React, { useState, useEffect, ChangeEvent, FormEvent } from "react";
import { Input, Button, Spinner, RadioGroup, Radio, Divider } from "@nextui-org/react";
import { fetchColumns, sendPateintData } from "../services/api";
import { useNavigate } from "react-router-dom";

interface FormData {
  [property: string]: string | object;
}

interface InputConfig {
  type: "text" | "number";
  name: string;
  categories?: string[];
  min?: number;
  max?: number;
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
          const navigate = useNavigate();
          return navigate("/model-selection");
        }
      } catch (error) {
        console.error("Error fetching data:", error);
      } finally {
        setLoading(false);
        setTimeout(() => {
          console.log("Delayed action after 10 seconds");
        }, 5000);
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

  const handleChange2 = (name: string, value: string) => {
    setFormData((prevFormData) => ({
      ...prevFormData,
      [name]: value,
    }));
  };

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    const res = await sendPateintData(formData);
    console.log(res);
  };

  return (
    <div className="pred-form">
      {loading ? (
        <Spinner />
      ) : (
        <>
          <label className="title">Chronic Kidney Disease (CKD) Form {localStorage.getItem("model")}</label>
          <Divider className="my-4" />
          <form onSubmit={handleSubmit}>
            {features.map((feature) => (
              <div key={feature.name}>
                {feature.type === "text" ? (
                  <RadioGroup label={feature.name + " *"} >
                    {feature.categories?.map((category) => (
                      <Radio
                        value={category}
                        onClick={() => handleChange2(feature.name, category)}
                        key={category}
                      >
                        {category}
                      </Radio>
                    ))}
                  </RadioGroup>
                ) : (
                  <Input
                    key={feature.name}
                    
                    variant="faded"
                    type={feature.type}
                    label={feature.name}
                    placeholder={`Range ${feature.min}-${feature.max}`}
                    name={feature.name}
                    value={formData[feature.name] as string}
                    onChange={handleChange}
                  />
                )}
              </div>
            ))}
            <Button type="submit">Show Results</Button>
          </form>
        </>
      )}
    </div>
  );
};

export default PredictionForm;
