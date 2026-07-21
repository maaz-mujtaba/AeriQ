<script>
	import { page } from '$app/stores';
	import { onMount } from 'svelte';
	import { loggedIn } from '$lib/stores/authStore.js';

	// Props using Svelte 5 bindable runes
	let {
		isCollapsed = $bindable(false),
		isMobileOpen = $bindable(false),
		isDark = $bindable(false)
	} = $props();

	// Function to toggle dark mode
	function toggleDarkMode() {
		isDark = !isDark;
		if (typeof window !== 'undefined') {
			if (isDark) {
				document.documentElement.classList.add('dark');
				localStorage.setItem('theme', 'dark');
			} else {
				document.documentElement.classList.remove('dark');
				localStorage.setItem('theme', 'light');
			}
		}
	}

	// Active path derivation from store
	let activePath = $derived($page.url.pathname);
</script>

<!-- Mobile Overlay Backdrop -->
{#if isMobileOpen}
	<button
		class="fixed inset-0 z-40 bg-zinc-900/40 backdrop-blur-sm transition-opacity duration-300 lg:hidden"
		onclick={() => (isMobileOpen = false)}
		aria-label="Close sidebar"
	></button>
{/if}

<!-- Sidebar Container -->
<aside
	class="fixed top-0 bottom-0 left-0 z-50 flex flex-col bg-white dark:bg-zinc-900 border-r border-zinc-200/80 dark:border-zinc-800 transition-all duration-300 ease-in-out
		{isCollapsed ? 'w-16' : 'w-64'}
		{isMobileOpen ? 'translate-x-0' : '-translate-x-full lg:translate-x-0'}"
>
	<!-- Header / Logo -->
	<div class="h-16 flex items-center px-4 border-b border-zinc-100 dark:border-zinc-800/60">
		<a href="/" class="flex items-center gap-2.5 overflow-hidden focus:outline-none">
			<div class="flex items-center justify-center h-9 w-9 rounded-xl bg-emerald-500 text-white shadow-md shadow-emerald-500/20 shrink-0">
				<svg class="h-5 w-5 animate-pulse" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
					<path stroke-linecap="round" stroke-linejoin="round" d="M9.59 4.59A2 2 0 1111 8H2m10.59 11.41A2 2 0 1014 16H2m15.73-8.27A2.5 2.5 0 1119.5 12H2" />
				</svg>
			</div>
			{#if !isCollapsed}
				<span class="text-xl font-bold tracking-tight bg-gradient-to-r from-zinc-900 via-emerald-600 to-zinc-900 dark:from-white dark:via-emerald-400 dark:to-white bg-clip-text text-transparent">
					AeriQ
				</span>
			{/if}
		</a>
	</div>

	<!-- Navigation Items -->
	<nav class="flex-1 overflow-y-auto px-3 py-4 space-y-1 select-none">
		<!-- Dashboard -->
		<a
			href="/dashboard"
			class="flex items-center gap-3 px-3 py-2.5 rounded-xl text-sm font-medium transition-all duration-150 group relative
				{activePath === '/dashboard'
					? 'bg-emerald-50 text-emerald-700 dark:bg-emerald-950/40 dark:text-emerald-400 shadow-sm'
					: 'text-zinc-600 dark:text-zinc-400 hover:bg-zinc-50 dark:hover:bg-zinc-800/40 hover:text-zinc-900 dark:hover:text-zinc-200'}"
			onclick={() => (isMobileOpen = false)}
		>
			<svg class="h-5 w-5 shrink-0" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
				<path stroke-linecap="round" stroke-linejoin="round" d="M4 6a2 2 0 012-2h2a2 2 0 012 2v4a2 2 0 01-2 2H6a2 2 0 01-2-2V6zM14 6a2 2 0 012-2h2a2 2 0 012 2v4a2 2 0 01-2 2h-2a2 2 0 01-2-2V6zM4 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2v-2zM14 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2v-2z" />
			</svg>
			{#if !isCollapsed}
				<span class="transition-opacity duration-200">Dashboard</span>
			{:else}
				<div class="absolute left-full ml-3 px-2 py-1 bg-zinc-900 dark:bg-zinc-800 text-white text-xs rounded shadow-md opacity-0 group-hover:opacity-100 transition-opacity duration-150 pointer-events-none whitespace-nowrap z-50">
					Dashboard
				</div>
			{/if}
		</a>

		<!-- Forecast -->
		<a
			href="/forecast"
			class="flex items-center gap-3 px-3 py-2.5 rounded-xl text-sm font-medium transition-all duration-150 group relative
				{activePath === '/forecast'
					? 'bg-emerald-50 text-emerald-700 dark:bg-emerald-950/40 dark:text-emerald-400 shadow-sm'
					: 'text-zinc-600 dark:text-zinc-400 hover:bg-zinc-50 dark:hover:bg-zinc-800/40 hover:text-zinc-900 dark:hover:text-zinc-200'}"
			onclick={() => (isMobileOpen = false)}
		>
			<svg class="h-5 w-5 shrink-0" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
				<path stroke-linecap="round" stroke-linejoin="round" d="M3 15a4 4 0 004 4h9a5 5 0 10-.1-9.999 5.002 5.002 0 10-9.78 2.096A4.001 4.001 0 003 15z" />
			</svg>
			{#if !isCollapsed}
				<span class="transition-opacity duration-200">Forecast</span>
			{:else}
				<div class="absolute left-full ml-3 px-2 py-1 bg-zinc-900 dark:bg-zinc-800 text-white text-xs rounded shadow-md opacity-0 group-hover:opacity-100 transition-opacity duration-150 pointer-events-none whitespace-nowrap z-50">
					Forecast
				</div>
			{/if}
		</a>

		<!-- Alerts -->
		<a
			href="/alerts"
			class="flex items-center gap-3 px-3 py-2.5 rounded-xl text-sm font-medium transition-all duration-150 group relative
				{activePath === '/alerts'
					? 'bg-emerald-50 text-emerald-700 dark:bg-emerald-950/40 dark:text-emerald-400 shadow-sm'
					: 'text-zinc-600 dark:text-zinc-400 hover:bg-zinc-50 dark:hover:bg-zinc-800/40 hover:text-zinc-900 dark:hover:text-zinc-200'}"
			onclick={() => (isMobileOpen = false)}
		>
			<svg class="h-5 w-5 shrink-0" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
				<path stroke-linecap="round" stroke-linejoin="round" d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9" />
			</svg>
			{#if !isCollapsed}
				<span class="transition-opacity duration-200">Alerts</span>
			{:else}
				<div class="absolute left-full ml-3 px-2 py-1 bg-zinc-900 dark:bg-zinc-800 text-white text-xs rounded shadow-md opacity-0 group-hover:opacity-100 transition-opacity duration-150 pointer-events-none whitespace-nowrap z-50">
					Alerts
				</div>
			{/if}
		</a>

		<!-- Analytics -->
		<a
			href="/analytics"
			class="flex items-center gap-3 px-3 py-2.5 rounded-xl text-sm font-medium transition-all duration-150 group relative
				{activePath === '/analytics'
					? 'bg-emerald-50 text-emerald-700 dark:bg-emerald-950/40 dark:text-emerald-400 shadow-sm'
					: 'text-zinc-600 dark:text-zinc-400 hover:bg-zinc-50 dark:hover:bg-zinc-800/40 hover:text-zinc-900 dark:hover:text-zinc-200'}"
			onclick={() => (isMobileOpen = false)}
		>
			<svg class="h-5 w-5 shrink-0" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
				<path stroke-linecap="round" stroke-linejoin="round" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
			</svg>
			{#if !isCollapsed}
				<span class="transition-opacity duration-200">Analytics</span>
			{:else}
				<div class="absolute left-full ml-3 px-2 py-1 bg-zinc-900 dark:bg-zinc-800 text-white text-xs rounded shadow-md opacity-0 group-hover:opacity-100 transition-opacity duration-150 pointer-events-none whitespace-nowrap z-50">
					Analytics
				</div>
			{/if}
		</a>

		<!-- AQI Map -->
		<a
			href="/map"
			class="flex items-center gap-3 px-3 py-2.5 rounded-xl text-sm font-medium transition-all duration-150 group relative
				{activePath === '/map'
					? 'bg-emerald-50 text-emerald-700 dark:bg-emerald-950/40 dark:text-emerald-400 shadow-sm'
					: 'text-zinc-600 dark:text-zinc-400 hover:bg-zinc-50 dark:hover:bg-zinc-800/40 hover:text-zinc-900 dark:hover:text-zinc-200'}"
			onclick={() => (isMobileOpen = false)}
		>
			<svg class="h-5 w-5 shrink-0" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
				<path stroke-linecap="round" stroke-linejoin="round" d="M9 20l-5.447-2.724A1 1 0 013 16.382V5.618a1 1 0 011.447-.894L9 7m0 13l6-3m-6 3V7m6 10l4.553 2.276A1 1 0 0021 18.382V7.618a1 1 0 00-.553-.894L15 4m0 13V4m0 0L9 7" />
			</svg>
			{#if !isCollapsed}
				<span class="transition-opacity duration-200">AQI Map</span>
			{:else}
				<div class="absolute left-full ml-3 px-2 py-1 bg-zinc-900 dark:bg-zinc-800 text-white text-xs rounded shadow-md opacity-0 group-hover:opacity-100 transition-opacity duration-150 pointer-events-none whitespace-nowrap z-50">
					AQI Map
				</div>
			{/if}
		</a>

		<!-- Health -->
		{#if $loggedIn}
			<a
				href="/health"
				class="flex items-center gap-3 px-3 py-2.5 rounded-xl text-sm font-medium transition-all duration-150 group relative
					{activePath === '/health'
						? 'bg-emerald-50 text-emerald-700 dark:bg-emerald-950/40 dark:text-emerald-400 shadow-sm'
						: 'text-zinc-600 dark:text-zinc-400 hover:bg-zinc-50 dark:hover:bg-zinc-800/40 hover:text-zinc-900 dark:hover:text-zinc-200'}"
				onclick={() => (isMobileOpen = false)}
			>
				<svg class="h-5 w-5 shrink-0" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
					<path stroke-linecap="round" stroke-linejoin="round" d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z" />
				</svg>
				{#if !isCollapsed}
					<span class="transition-opacity duration-200">Health</span>
				{:else}
					<div class="absolute left-full ml-3 px-2 py-1 bg-zinc-900 dark:bg-zinc-800 text-white text-xs rounded shadow-md opacity-0 group-hover:opacity-100 transition-opacity duration-150 pointer-events-none whitespace-nowrap z-50">
						Health
					</div>
				{/if}
			</a>
		{/if}

		<!-- Saved Cities -->
		{#if $loggedIn}
			<a
				href="/saved"
				class="flex items-center gap-3 px-3 py-2.5 rounded-xl text-sm font-medium transition-all duration-150 group relative
					{activePath === '/saved'
						? 'bg-emerald-50 text-emerald-700 dark:bg-emerald-950/40 dark:text-emerald-400 shadow-sm'
						: 'text-zinc-600 dark:text-zinc-400 hover:bg-zinc-50 dark:hover:bg-zinc-800/40 hover:text-zinc-900 dark:hover:text-zinc-200'}"
				onclick={() => (isMobileOpen = false)}
			>
				<svg class="h-5 w-5 shrink-0" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
					<path stroke-linecap="round" stroke-linejoin="round" d="M5 5a2 2 0 012-2h10a2 2 0 012 2v16l-7-3.5L5 21V5z" />
				</svg>
				{#if !isCollapsed}
					<span class="transition-opacity duration-200">Saved Cities</span>
				{:else}
					<div class="absolute left-full ml-3 px-2 py-1 bg-zinc-900 dark:bg-zinc-800 text-white text-xs rounded shadow-md opacity-0 group-hover:opacity-100 transition-opacity duration-150 pointer-events-none whitespace-nowrap z-50">
						Saved Cities
					</div>
				{/if}
			</a>
		{/if}

		<!-- Reports -->
		{#if $loggedIn}
			<a
				href="/reports"
				class="flex items-center gap-3 px-3 py-2.5 rounded-xl text-sm font-medium transition-all duration-150 group relative
					{activePath === '/reports'
						? 'bg-emerald-50 text-emerald-700 dark:bg-emerald-950/40 dark:text-emerald-400 shadow-sm'
						: 'text-zinc-600 dark:text-zinc-400 hover:bg-zinc-50 dark:hover:bg-zinc-800/40 hover:text-zinc-900 dark:hover:text-zinc-200'}"
				onclick={() => (isMobileOpen = false)}
			>
				<svg class="h-5 w-5 shrink-0" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
					<path stroke-linecap="round" stroke-linejoin="round" d="M9 17v-2m3 2v-4m3 4v-6m2 10H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
				</svg>
				{#if !isCollapsed}
					<span class="transition-opacity duration-200">Reports</span>
				{:else}
					<div class="absolute left-full ml-3 px-2 py-1 bg-zinc-900 dark:bg-zinc-800 text-white text-xs rounded shadow-md opacity-0 group-hover:opacity-100 transition-opacity duration-150 pointer-events-none whitespace-nowrap z-50">
						Reports
					</div>
				{/if}
			</a>
		{/if}

		<!-- Settings -->
		{#if $loggedIn}
			<a
				href="/settings"
				class="flex items-center gap-3 px-3 py-2.5 rounded-xl text-sm font-medium transition-all duration-150 group relative
					{activePath === '/settings'
						? 'bg-emerald-50 text-emerald-700 dark:bg-emerald-950/40 dark:text-emerald-400 shadow-sm'
						: 'text-zinc-600 dark:text-zinc-400 hover:bg-zinc-50 dark:hover:bg-zinc-800/40 hover:text-zinc-900 dark:hover:text-zinc-200'}"
				onclick={() => (isMobileOpen = false)}
			>
				<svg class="h-5 w-5 shrink-0" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
					<path stroke-linecap="round" stroke-linejoin="round" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" />
					<path stroke-linecap="round" stroke-linejoin="round" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
				</svg>
				{#if !isCollapsed}
					<span class="transition-opacity duration-200">Settings</span>
				{:else}
					<div class="absolute left-full ml-3 px-2 py-1 bg-zinc-900 dark:bg-zinc-800 text-white text-xs rounded shadow-md opacity-0 group-hover:opacity-100 transition-opacity duration-150 pointer-events-none whitespace-nowrap z-50">
						Settings
					</div>
				{/if}
			</a>
		{/if}

		<!-- About -->
		<a
			href="/about"
			class="flex items-center gap-3 px-3 py-2.5 rounded-xl text-sm font-medium transition-all duration-150 group relative
				{activePath === '/about'
					? 'bg-emerald-50 text-emerald-700 dark:bg-emerald-950/40 dark:text-emerald-400 shadow-sm'
					: 'text-zinc-600 dark:text-zinc-400 hover:bg-zinc-50 dark:hover:bg-zinc-800/40 hover:text-zinc-900 dark:hover:text-zinc-200'}"
			onclick={() => (isMobileOpen = false)}
		>
			<svg class="h-5 w-5 shrink-0" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
				<path stroke-linecap="round" stroke-linejoin="round" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
			</svg>
			{#if !isCollapsed}
				<span class="transition-opacity duration-200">About</span>
			{:else}
				<div class="absolute left-full ml-3 px-2 py-1 bg-zinc-900 dark:bg-zinc-800 text-white text-xs rounded shadow-md opacity-0 group-hover:opacity-100 transition-opacity duration-150 pointer-events-none whitespace-nowrap z-50">
					About
				</div>
			{/if}
		</a>
	</nav>

	<!-- Sidebar Bottom: Theme Toggle & Footer -->
	<div class="p-3 border-t border-zinc-100 dark:border-zinc-800/60 space-y-4">
		<!-- Dark Mode Toggle -->
		{#if !isCollapsed}
			<div class="flex items-center justify-between p-1 bg-zinc-100 dark:bg-zinc-800/50 rounded-xl relative">
				<!-- Sliding background indicator -->
				<div class="absolute top-1 bottom-1 w-[calc(50%-4px)] bg-white dark:bg-zinc-900 rounded-lg shadow-sm border border-zinc-200/50 dark:border-zinc-700/50 transition-all duration-300 ease-out
					{isDark ? 'translate-x-[100%]' : 'translate-x-0'}">
				</div>

				<button
					onclick={() => isDark && toggleDarkMode()}
					class="relative z-10 flex-1 flex items-center justify-center gap-1.5 py-1.5 text-xs font-semibold rounded-lg focus:outline-none transition-colors duration-200
						{!isDark ? 'text-emerald-600 dark:text-emerald-400' : 'text-zinc-400 dark:text-zinc-500 hover:text-zinc-600'}"
				>
					<svg class="h-3.5 w-3.5" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
						<path stroke-linecap="round" stroke-linejoin="round" d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364-6.364l-.707.707M6.343 17.657l-.707.707m0-12.728l.707.707m12.728 12.728l.707-.707M12 8a4 4 0 100 8 4 4 0 000-8z" />
					</svg>
					Light
				</button>
				<button
					onclick={() => !isDark && toggleDarkMode()}
					class="relative z-10 flex-1 flex items-center justify-center gap-1.5 py-1.5 text-xs font-semibold rounded-lg focus:outline-none transition-colors duration-200
						{isDark ? 'text-emerald-400' : 'text-zinc-500 dark:text-zinc-400 hover:text-zinc-700'}"
				>
					<svg class="h-3.5 w-3.5" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
						<path stroke-linecap="round" stroke-linejoin="round" d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z" />
					</svg>
					Dark
				</button>
			</div>
		{:else}
			<button
				onclick={toggleDarkMode}
				class="w-full flex items-center justify-center p-2.5 rounded-xl border border-zinc-200/50 dark:border-zinc-800 hover:bg-zinc-50 dark:hover:bg-zinc-800/40 text-zinc-500 dark:text-zinc-400 hover:text-zinc-900 dark:hover:text-zinc-100 transition-colors focus:outline-none relative group"
				aria-label="Toggle dark mode"
			>
				{#if isDark}
					<svg class="h-4.5 w-4.5" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
						<path stroke-linecap="round" stroke-linejoin="round" d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z" />
					</svg>
				{:else}
					<svg class="h-4.5 w-4.5" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
						<path stroke-linecap="round" stroke-linejoin="round" d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364-6.364l-.707.707M6.343 17.657l-.707.707m0-12.728l.707.707m12.728 12.728l.707-.707M12 8a4 4 0 100 8 4 4 0 000-8z" />
					</svg>
				{/if}
				<div class="absolute left-full ml-3 px-2 py-1 bg-zinc-900 dark:bg-zinc-800 text-white text-xs rounded shadow-md opacity-0 group-hover:opacity-100 transition-opacity duration-150 pointer-events-none whitespace-nowrap z-50">
					Toggle Theme
				</div>
			</button>
		{/if}

		<!-- Footer -->
		{#if !isCollapsed}
			<p class="text-[10px] text-center text-zinc-400 dark:text-zinc-500 font-medium tracking-wide transition-opacity duration-200">
				Breathe Better. Live Better.
			</p>
		{/if}
	</div>
</aside>
