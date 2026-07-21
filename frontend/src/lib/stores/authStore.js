import { writable } from 'svelte/store';

const isBrowser = typeof window !== 'undefined';

// Fetch initial state from localStorage if browser matches, else default to false
const initialStatus = isBrowser ? localStorage.getItem('isLoggedIn') === 'true' : false;

export const loggedIn = writable(initialStatus);

/**
 * Simulates a successful login
 */
export function login() {
	if (isBrowser) {
		localStorage.setItem('isLoggedIn', 'true');
	}
	loggedIn.set(true);
}

/**
 * Simulates logging out
 */
export function logout() {
	if (isBrowser) {
		localStorage.removeItem('isLoggedIn');
	}
	loggedIn.set(false);
}
