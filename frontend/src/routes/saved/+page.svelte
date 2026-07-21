<script>
	import { loggedIn } from '$lib/stores/authStore.js';
	import LoginRequired from '$lib/components/LoginRequired.svelte';
</script>

<svelte:head>
	<title>Saved Cities | AeriQ</title>
	<meta name="description" content="View air quality conditions in your saved locations." />
</svelte:head>

{#if !$loggedIn}
	<LoginRequired title="Saved Cities" description="Track, compare, and get push alert integrations for all your bookmarked locations and custom zones." />
{:else}
	<div class="space-y-6">
		<!-- Breadcrumbs and Header -->
		<div class="space-y-1">
			<div class="flex items-center gap-2 text-xs font-semibold text-zinc-400 dark:text-zinc-500 uppercase tracking-wider">
				<span>App</span>
				<span>/</span>
				<span class="text-emerald-500 dark:text-emerald-400">Saved Cities</span>
			</div>
			<h1 class="text-3xl font-extrabold tracking-tight text-zinc-900 dark:text-white">Saved Cities</h1>
			<p class="text-sm text-zinc-500 dark:text-zinc-400">Track and compare air indexes across multiple locations.</p>
		</div>

		<!-- Main Card -->
		<div class="bg-white dark:bg-zinc-900 border border-zinc-200/80 dark:border-zinc-800/80 rounded-2xl p-8 shadow-sm flex flex-col items-center justify-center text-center min-h-[400px] gap-4 transition-all duration-300">
			<div class="h-16 w-16 rounded-2xl bg-emerald-50 dark:bg-emerald-950/30 text-emerald-500 flex items-center justify-center shadow-sm">
				<svg class="h-8 w-8 text-emerald-500" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
					<path stroke-linecap="round" stroke-linejoin="round" d="M5 5a2 2 0 012-2h10a2 2 0 012 2v16l-7-3.5L5 21V5z" />
				</svg>
			</div>
			<div class="max-w-md space-y-1">
				<h2 class="text-xl font-bold text-zinc-900 dark:text-white">Saved Cities Panel Under Development</h2>
				<p class="text-sm text-zinc-500 dark:text-zinc-400">
					Access custom dashboard reports for all your bookmarked locations. Add custom labels (e.g. Home, Office, Travel) and watch live side-by-side indexes.
				</p>
			</div>
			<button class="mt-2 px-4.5 py-2.5 bg-zinc-900 dark:bg-zinc-850 hover:bg-zinc-800 dark:hover:bg-zinc-800/70 text-white dark:text-zinc-200 text-sm font-semibold rounded-xl transition-all shadow-sm focus:outline-none">
				Add New City
			</button>
		</div>
	</div>
{/if}
