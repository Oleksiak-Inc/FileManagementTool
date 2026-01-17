import { setCookie, getCookie, deleteCookie } from '../utils/cookies.js';

const API_URL = 'http://localhost:5000/api/v1';

export const login = async (email, password) => {
    const response = await fetch(`${API_URL}/auth/login`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, password })
    });

    if (!response.ok) {
        throw new Error('Login failed');
    }

    const data = await response.json();
    setCookie('access_token', data.access_token);
    return data;
};

export const register = async (userData) => {
    const response = await fetch(`${API_URL}/testers/register`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(userData)
    });

    if (!response.ok) {
        throw new Error('Registration failed');
    }

    return response.json();
};

export const logout = () => {
    deleteCookie('access_token');
    window.location.href = '/login';
};

export const getCurrentUser = () => {
    const token = getCookie('access_token');
    if (!token) return null;

    // Decode JWT token to get user info
    try {
        const payload = JSON.parse(atob(token.split('.')[1]));
        return payload;
    } catch (error) {
        return null;
    }
};

export const isAuthenticated = () => {
    return !!getCookie('access_token');
};