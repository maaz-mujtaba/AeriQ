import { redirect } from '@sveltejs/kit';
import { browser } from '$app/environment';
import { hasSession } from '$lib/stores/authStore.js';

/** @type {import('./$types').PageLoad} */
export function load() {
	const isAuthed = browser && hasSession();
	if (isAuthed) {
		throw redirect(307, '/map');
	} else {
		throw redirect(307, '/settings');
	}
}
