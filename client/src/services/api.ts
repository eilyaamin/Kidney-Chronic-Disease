interface ModelData {
  [modelName: string]: {
    name: string;
    description: string;
    accuracy: string;
  };
}

interface InputConfig {
  type: "text" | "number";
  name: string;
  categories?: string[];
  min?: number;
  max?: number;
}

interface PostData {
  [property: string]: string | object;
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

const sendPateintData = async (data: PostData) => {
  const url = "http://localhost:3050/api/predict";
  const requestOptions: RequestInit = {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(data),
  };

  try {
    const response = await fetch(url, requestOptions);

    if (!response.ok) {
      throw new Error(`HTTP error! Status: ${response.status}`);
    }
    const responseData = await response.json();

    return responseData;
  } catch (error) {
    throw error;
  }
};

export { fetchModelsData, fetchColumns, sendPateintData };
