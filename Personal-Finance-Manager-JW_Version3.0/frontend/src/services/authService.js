import api from '../api';

export const signup = async (userData) => {
    try {
        const response = await api.post('users/users/', userData);
        return response.data;
    } catch (error) {
        console.error('Signup error:', error);
        throw error.response?.data || "An error occurred";
    }
};

export const login = async (credentials) => {
    try {
        const response = await api.post('/auth/login', credentials);
        return response.data;
    } catch (error) {
        console.error('Login error:', error);
        throw error.response?.data || "An error occurred";
    }
};
