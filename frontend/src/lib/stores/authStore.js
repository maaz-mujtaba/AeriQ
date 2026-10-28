import { writable } from 'svelte/store';

const isBrowser = typeof window !== 'undefined';

// Fetch initial state from localStorage if browser matches, else default to false
const initialStatus = isBrowser ? Boolean(localStorage.getItem('accessToken')) : false;

export const loggedIn = writable(initialStatus);
export const hasSession = () => isBrowser && Boolean(localStorage.getItem('accessToken'));

/**
 * Simulates a successful login
 */
export function login(session) {
	if (isBrowser) {
		if (!session?.access_token) throw new Error('The server did not return an access token.');
		localStorage.setItem('accessToken', session.access_token);
		localStorage.setItem('user', JSON.stringify(session.user));
	}
	loggedIn.set(true);
}

/**
 * Simulates logging out
 */
export function logout() {
	if (isBrowser) {
		localStorage.removeItem('accessToken');
		localStorage.removeItem('user');
		localStorage.removeItem('isLoggedIn');
	}
	loggedIn.set(false);
}

export const protectedRoutes = [
	'/forecast',
	'/alerts',
	'/map',
	'/aqi-map',
	'/health',
	'/saved',
	'/saved-cities',
	'/reports'
];

/**
 * Checks if a given pathname belongs to protected routes.
 * @param {string} pathname
 * @returns {boolean}
 */
export function isProtectedPath(pathname) {
	const normalized = pathname.replace(/\/$/, '') || '/';
	return protectedRoutes.some(
		(route) => normalized === route || normalized.startsWith(route + '/')
	);
}
