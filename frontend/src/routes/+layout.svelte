<script>
	import './layout.css';
	import favicon from '$lib/assets/favicon.svg';
	import Layout from '$lib/components/Layout.svelte';
	import { page } from '$app/stores';
	import { goto } from '$app/navigation';
	import { browser } from '$app/environment';
	import { loggedIn, isProtectedPath } from '$lib/stores/authStore.js';

	let { children } = $props();

	// Reactive check: if user becomes logged out while on a protected route, immediately redirect
	$effect(() => {
		if (browser && !$loggedIn && isProtectedPath($page.url.pathname)) {
			goto('/settings', { replaceState: true });
		}
	});
</script>

<svelte:head><link rel="icon" href={favicon} /></svelte:head>

<Layout>
	{#if browser && !$loggedIn && isProtectedPath($page.url.pathname)}
		<div class="min-h-[400px]"></div>
	{:else}
		{@render children()}
	{/if}
</Layout>
