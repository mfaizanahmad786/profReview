import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
});

// Add auth token to requests if available
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Professor API calls
export const getProfessors = (search = '', department = '') => {
  return api.get('/professors', { params: { search, department } });
};

export const getProfessor = (id) => {
  return api.get(`/professors/${id}`);
};

// Review API calls
export const getProfessorReviews = (professorId) => {
  return api.get(`/reviews/professor/${professorId}`);
};

export const getGradeDistribution = (professorId) => {
  return api.get(`/reviews/professor/${professorId}/grade-distribution`);
};

export const createReview = (reviewData) => {
  return api.post('/reviews', reviewData);
};

// Auth API calls
export const login = (email, password) => {
  const formData = new FormData();
  formData.append('username', email);
  formData.append('password', password);
  return api.post('/auth/login', formData);
};

export const signup = (email, password) => {
  return api.post('/auth/signup', { email, password });
};

export const getCurrentUser = () => {
  return api.get('/auth/me');
};

export default api;

