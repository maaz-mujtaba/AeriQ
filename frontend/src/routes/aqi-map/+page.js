import { redirect } from '@sveltejs/kit';
import { browser } from '$app/environment';

/** @type {import('./$types').PageLoad} */
export function load() {
	const isAuthed = browser ? localStorage.getItem('isLoggedIn') === 'true' : false;
	if (isAuthed) {
		throw redirect(307, '/map');
	} else {
		throw redirect(307, '/settings');
	}
}
