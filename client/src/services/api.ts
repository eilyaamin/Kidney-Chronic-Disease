interface ModelData {
  [modelName: string]: {
    name: string;
    description: string;
    accuracy: string;
  };
}

interface Features {
  [modelName: string]: {
    name: string;
    type: string;
  };
}

interface InputConfig {
  type: "text" | "number";
  name: string;
}


const fetchModelsData = async (): Promise<ModelData> => {

  const response = await fetch("http://localhost:3050/api/models");

  const res = await response.json();

  return res;
};

const fetchColumns = async (): Promise<InputConfig[]> => {

  const response = await fetch("http://localhost:3050/api/features");

  const res = await response.json();

  return res;
};

export { fetchModelsData, fetchColumns };
