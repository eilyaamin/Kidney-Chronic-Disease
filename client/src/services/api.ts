interface ModelData {
  [modelName: string]: {
    name: string;
    description: string;
    accuracy: string;
  };
}

const fetchModelsData = async (): Promise<ModelData> => {
  // Simulating an API call delay with a timeout
  await new Promise((resolve) => setTimeout(resolve, 1000));

  const response = await fetch("http://localhost:3050/api/models");

  const res = await response.json();

  return res;
};

export default fetchModelsData;
