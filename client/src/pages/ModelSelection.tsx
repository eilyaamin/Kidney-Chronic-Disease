import React, { useState, useEffect } from "react";
import Model from "../components/Model";
import { Link, Spinner } from "@nextui-org/react";
import { fetchModelsData } from "../services/api";

interface ModelConfig {
  name: string;
  description: string;
  accuracy: string;
}

interface ModelData {
  [modelName: string]: ModelConfig;
}

const ModelSelection: React.FC = () => {
  const [columns, setColumns] = useState<ModelConfig[]>([]);

  const setModelName = (model: ModelConfig) => {
    localStorage.setItem("model", JSON.stringify(model.name));
  };

  useEffect(() => {
    const fetchData = async () => {
      try {
        const modelData: ModelData = await fetchModelsData();
        const inputConfigs: ModelConfig[] = Object.values(modelData);
        setColumns(inputConfigs);
      } catch (error) {
        console.error("Error fetching data:", error);
      }
    };
    fetchData();
  }, []);

  return (
    <div className="model-selection">
      {columns.length === 0 ? (
        <Spinner />
      ) : (
        <div className="model-selection">
          <label className="title">Select Model</label>
          <div className="model-selection-grid">
            {columns.map((model: ModelConfig) => (
              <Link
                key={model.name}
                href="/pred-form"
                className="model"
                onClick={() => setModelName(model)}
              >
                <Model
                  accuracy={model.accuracy}
                  name={model.name}
                  description={model.description}
                />
              </Link>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

export default ModelSelection;
