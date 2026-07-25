import { writable } from 'svelte/store';

// Stores for AQI data
/** @type {import('svelte/store').Writable<any>} */
export const currentAQI = writable(null);
/** @type {import('svelte/store').Writable<any[]>} */
export const forecastData = writable([]);
/** @type {import('svelte/store').Writable<any[]>} */
export const historyData = writable([]);
/** @type {import('svelte/store').Writable<any[]>} */
export const weatherHourly = writable([]);

// Stores for request status
/** @type {import('svelte/store').Writable<boolean>} */
export const isLoading = writable(false);
/** @type {import('svelte/store').Writable<string | null>} */
export const errorMessage = writable(null);