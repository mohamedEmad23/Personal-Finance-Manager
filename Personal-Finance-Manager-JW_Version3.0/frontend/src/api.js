import axios from "axios";

const instance = axios.create({
  baseURL: "http://localhost:8000/api/v1",
  withCredentials: true, // Include cookies (if necessary)
});

export const signup = async (userData) => {
  try {
    const response = await instance.post("/users/users/", userData);
    return response.data;
  } catch (error) {
    console.error("Signup error:", error);
    throw error;
  }
};

export default instance