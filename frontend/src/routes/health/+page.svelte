<script>
	import { loggedIn } from '$lib/stores/authStore.js';
	import LoginRequired from '$lib/components/LoginRequired.svelte';
</script>

<svelte:head>
	<title>Health Recommendations | AeriQ</title>
	<meta name="description" content="View personalized health and activity suggestions based on current AQI indices." />
</svelte:head>

{#if !$loggedIn}
	<LoginRequired title="Health Recommendations" description="Access medical-backed health recommendations, air quality alerts, and activity schedules tailored for your active locations." />
{:else}
	<div class="space-y-6">
		<!-- Breadcrumbs and Header -->
		<div class="space-y-1">
			<div class="flex items-center gap-2 text-xs font-semibold text-zinc-400 dark:text-zinc-500 uppercase tracking-wider">
				<span>App</span>
				<span>/</span>
				<span class="text-emerald-500 dark:text-emerald-400">Health</span>
			</div>
			<h1 class="text-3xl font-extrabold tracking-tight text-zinc-900 dark:text-white">Health Recommendations</h1>
			<p class="text-sm text-zinc-500 dark:text-zinc-400">Medical-backed guidance, activity indexes, and vulnerable group warnings.</p>
		</div>

		<!-- Main Card -->
		<div class="bg-white dark:bg-zinc-900 border border-zinc-200/80 dark:border-zinc-800/80 rounded-2xl p-8 shadow-sm flex flex-col items-center justify-center text-center min-h-[400px] gap-4 transition-all duration-300">
			<div class="h-16 w-16 rounded-2xl bg-emerald-50 dark:bg-emerald-950/30 text-emerald-500 flex items-center justify-center shadow-sm">
				<svg class="h-8 w-8 text-emerald-500 animate-pulse" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
					<path stroke-linecap="round" stroke-linejoin="round" d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z" />
				</svg>
			</div>
			<div class="max-w-md space-y-1">
				<h2 class="text-xl font-bold text-zinc-900 dark:text-white">Health Index Under Development</h2>
				<p class="text-sm text-zinc-500 dark:text-zinc-400">
					Receive medical advice matching the current pollution density. Calculate indoor/outdoor safety duration, mask suggestions, and ventilating alerts.
				</p>
			</div>
			<button class="mt-2 px-4.5 py-2.5 bg-emerald-500 hover:bg-emerald-600 active:scale-95 text-white text-sm font-semibold rounded-xl transition-all shadow-md shadow-emerald-500/10 focus:outline-none">
				View Guidelines
			</button>
		</div>
	</div>
{/if}
