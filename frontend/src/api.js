import axios from "axios";

export const api = axios.create({
  baseURL: "https://hrms-backend-72bf.onrender.com",
});
