import { redirect } from '@sveltejs/kit';
import { browser } from '$app/environment';
import { isProtectedPath } from '$lib/stores/authStore.js';

export const ssr = false;

/** @type {import('./$types').LayoutLoad} */
export function load({ url }) {
	if (isProtectedPath(url.pathname)) {
		const isAuthed = browser ? localStorage.getItem('isLoggedIn') === 'true' : false;
		if (!isAuthed) {
			throw redirect(307, '/settings');
		}
	}

	return {};
}
