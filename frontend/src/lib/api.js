import {
    currentAQI,
    isLoading,
    errorMessage
} from '$lib/stores/aqiStore.js';

// Base URL of the AeriQ FastAPI backend
const API_BASE_URL =
    import.meta.env.PUBLIC_API_BASE_URL || 'http://localhost:8000';

// Reusable function for making API requests

/**
 * Makes a reusable request to the AeriQ backend.
 * @param {string} endpoint
 * @param {RequestInit} options
 * @returns {Promise<any>}
 */
async function apiRequest(endpoint, options = {}) {
    try {
        const response = await fetch(`${API_BASE_URL}${endpoint}`, {
            headers: {
                'Content-Type': 'application/json',
                ...options.headers
            },
            ...options
        });

        if (!response.ok) {
            throw new Error(
                `API request failed: ${response.status} ${response.statusText}`
            );
        }

        return await response.json();
    } catch (error) {
        console.error(`AeriQ API error at ${endpoint}:`, error);
        throw error;
    }
}

/**
 * Get the current AQI for a location.
 * @param {number} latitude
 * @param {number} longitude
 */
export async function getCurrentAQI(latitude, longitude) {
    return apiRequest(
        `/api/aqi/current?latitude=${latitude}&longitude=${longitude}`
    );
}

/**
 * Get the predicted AQI for the next 24–72 hours.
 * @param {number} latitude
 * @param {number} longitude
 */
export async function getAQIForecast(latitude, longitude) {
    return apiRequest(
        `/api/aqi/forecast?latitude=${latitude}&longitude=${longitude}`
    );
}

/**
 * Get previous AQI readings.
 * @param {number} latitude
 * @param {number} longitude
 */
export async function getAQIHistory(latitude, longitude) {
    return apiRequest(
        `/api/aqi/history?latitude=${latitude}&longitude=${longitude}`
    );
}

/**
 * Subscribe a user to air-quality alerts.
 * @param {{
 *   email: string,
 *   latitude: number,
 *   longitude: number,
 *   vulnerableGroup: string
 * }} subscriptionData
 */
export async function subscribeToAlerts(subscriptionData) {
    return apiRequest('/api/alerts/subscribe', {
        method: 'POST',
        body: JSON.stringify(subscriptionData)
    });
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



