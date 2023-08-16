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
  const response = await fetch("https://chronic-kidney-disease-server.onrender.com/models");

  const res = await response.json();

  return res;
};

const fetchColumns = async (): Promise<InputConfig[]> => {
  const response = await fetch("https://chronic-kidney-disease-server.onrender.com/features");

  const res = await response.json();

  console.log(res);

  return res;
};

const sendPateintData = async (data: PostData) => {
  const url = "https://chronic-kidney-disease-server.onrender.com/predict";
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

    console.log(responseData);

    return responseData;
  } catch (error) {
    throw error;
  }
};

export { fetchModelsData, fetchColumns, sendPateintData };
