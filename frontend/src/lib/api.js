import {
    currentAQI,
    forecastData,
    weatherHourly,
    isLoading,
    errorMessage
} from '$lib/stores/aqiStore.js';
import { writable } from 'svelte/store';
import { logout } from '$lib/stores/authStore.js';

// Configure PUBLIC_API_BASE_URL as https://aeriq-backend.onrender.com/api.
const configuredApiBase = (import.meta.env.PUBLIC_API_BASE_URL || 'https://aeriq-backend.onrender.com/api').replace(/\/+$/, '');
const API_BASE_URL = configuredApiBase.endsWith('/api') ? configuredApiBase : `${configuredApiBase}/api`;
export const serverWaking = writable(false);
let activeRequests = 0;

// Reusable function for making API requests

/**
 * Makes a reusable request to the AeriQ backend.
 * @param {string} endpoint
 * @param {RequestInit} options
 * @returns {Promise<any>}
 */
async function apiRequest(endpoint, options = {}) {
    const normalizedPath = endpoint.startsWith('/api/') ? endpoint.slice(4) : endpoint;
    const controller = new AbortController();
    const timeout = setTimeout(() => controller.abort(), 75000);
    activeRequests += 1;
    const wakeTimer = setTimeout(() => serverWaking.set(true), 2500);
    try {
        const token = typeof localStorage !== 'undefined' ? localStorage.getItem('accessToken') : null;
        const response = await fetch(`${API_BASE_URL}${normalizedPath}`, {
            ...options,
            signal: options.signal || controller.signal,
            headers: {
                ...(options.body !== undefined ? { 'Content-Type': 'application/json' } : {}),
                ...(token ? { Authorization: `Bearer ${token}` } : {}),
                ...options.headers
            }
        });

        if (!response.ok) {
            const payload = await response.json().catch(() => null);
            if (response.status === 401 && token) logout();
            const detail = payload?.detail;
            const message = typeof detail === 'string' ? detail : Array.isArray(detail) ? detail.map((item) => item.msg).join('; ') : detail?.error;
            throw new Error(message || `Request failed (${response.status})`);
        }
        if (response.status === 204) return null;
        return await response.json();
    } catch (error) {
        console.error(`AeriQ API error at ${endpoint}:`, error);
        if (error instanceof Error && error.name === 'AbortError') throw new Error('The server took too long to respond. Please try again.');
        if (error instanceof TypeError) throw new Error('Cannot reach the AeriQ server. Check your connection and try again.');
        throw error;
    } finally {
        clearTimeout(timeout);
        clearTimeout(wakeTimer);
        activeRequests = Math.max(0, activeRequests - 1);
        if (activeRequests === 0) serverWaking.set(false);
    }
}

export const api = { request: apiRequest };
/** @param {{ email: string, password: string }} credentials */
export const signIn = (credentials) => apiRequest('/auth/login', { method: 'POST', body: JSON.stringify(credentials) });
/** @param {object} profile */
export const signUp = (profile) => apiRequest('/auth/register', { method: 'POST', body: JSON.stringify(profile) });
/** @param {string} city */
export const predictCityAQI = (city) => apiRequest(`/predict/${encodeURIComponent(city)}`);
export const getCities = () => apiRequest('/cities/all');
export const getCurrentUser = () => apiRequest('/auth/me');
/** @param {string} city */
export const assessHealthRisk = (city) => apiRequest('/health/assess', { method: 'POST', body: JSON.stringify({ city }) });
/** @param {string} city1 @param {string} city2 */
export const compareCities = (city1, city2) => apiRequest(`/compare/${encodeURIComponent(city1)}/${encodeURIComponent(city2)}`);

/**
 * Get the current AQI for a location.
 * @param {number} latitude
 * @param {number} longitude
 */
export async function getCurrentAQI(latitude, longitude) {
    return apiRequest(
        `/aqi/current?latitude=${latitude}&longitude=${longitude}`
    );
}

/**
 * Get the predicted AQI for the next 24–72 hours.
 * @param {number} latitude
 * @param {number} longitude
 */
export async function getAQIForecast(latitude, longitude) {
    return apiRequest(
        `/aqi/forecast?latitude=${latitude}&longitude=${longitude}`
    );
}

/**
 * Load current AQI and update the Svelte stores.
 * @param {number} latitude
 * @param {number} longitude
 */
export async function loadCurrentAQI(latitude, longitude) {
    isLoading.set(true);
    errorMessage.set(null);

    try {
        const data = await getCurrentAQI(latitude, longitude);
        currentAQI.set(data);
        return data;
    } catch (error) {
        const message =
            error instanceof Error
                ? error.message
                : 'Unable to load the current AQI.';

        errorMessage.set(message);
        currentAQI.set(null);
        throw error;
    } finally {
        isLoading.set(false);
    }
}

/**
 * Load forecast AQI data and update Svelte stores.
 * @param {number} latitude
 * @param {number} longitude
 */
export async function loadAQIForecast(latitude, longitude) {
    isLoading.set(true);
    errorMessage.set(null);

    try {
        const data = await getAQIForecast(latitude, longitude);
        forecastData.set(data.forecast || []);
        return data;
    } catch (error) {
        const message =
            error instanceof Error
                ? error.message
                : 'Unable to load the air quality forecast.';

        errorMessage.set(message);
        forecastData.set([]);
        throw error;
    } finally {
        isLoading.set(false);
    }
}

/**
 * Get weather hourly forecast.
 * @param {number} latitude
 * @param {number} longitude
 */
export async function getWeatherHourly(latitude, longitude) {
    return apiRequest(
        `/weather/hourly?latitude=${latitude}&longitude=${longitude}`
    );
}

/**
 * Load weather hourly data and update stores.
 * @param {number} latitude
 * @param {number} longitude
 */
export async function loadWeatherHourly(latitude, longitude) {
    isLoading.set(true);
    errorMessage.set(null);

    try {
        const data = await getWeatherHourly(latitude, longitude);
        weatherHourly.set(data.hourly || []);
        return data;
    } catch (error) {
        const message =
            error instanceof Error
                ? error.message
                : 'Unable to load the hourly weather forecast.';

        errorMessage.set(message);
        weatherHourly.set([]);
        throw error;
    } finally {
        isLoading.set(false);
    }
}



