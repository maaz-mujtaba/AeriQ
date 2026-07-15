import { writable } from 'svelte/store';

// Stores for AQI data
export const currentAQI = writable(null);
export const forecastData = writable([]);
export const historyData = writable([]);

// Stores for request status
export const isLoading = writable(false);
/** @type {import('svelte/store').Writable<string | null>} */
export const errorMessage = writable(null);