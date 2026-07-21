<script>
	import { loggedIn } from '$lib/stores/authStore.js';
	import LoginRequired from '$lib/components/LoginRequired.svelte';
</script>

<svelte:head>
	<title>Settings | AeriQ</title>
	<meta name="description" content="Manage your account preferences, notification configuration, and general settings." />
</svelte:head>

{#if !$loggedIn}
	<LoginRequired title="System Settings" description="Modify account credentials, manage notification triggers, sync API integrations, and coordinate regional data sensors." />
{:else}
	<div class="space-y-6">
		<!-- Breadcrumbs and Header -->
		<div class="space-y-1">
			<div class="flex items-center gap-2 text-xs font-semibold text-zinc-400 dark:text-zinc-500 uppercase tracking-wider">
				<span>App</span>
				<span>/</span>
				<span class="text-emerald-500 dark:text-emerald-400">Settings</span>
			</div>
			<h1 class="text-3xl font-extrabold tracking-tight text-zinc-900 dark:text-white">Settings</h1>
			<p class="text-sm text-zinc-500 dark:text-zinc-400">Configure account preferences, email routing, API keys, and dark/light system sync.</p>
		</div>

		<!-- Main Card -->
		<div class="bg-white dark:bg-zinc-900 border border-zinc-200/80 dark:border-zinc-800/80 rounded-2xl p-8 shadow-sm flex flex-col items-center justify-center text-center min-h-[400px] gap-4 transition-all duration-300">
			<div class="h-16 w-16 rounded-2xl bg-emerald-50 dark:bg-emerald-950/30 text-emerald-500 flex items-center justify-center shadow-sm">
				<svg class="h-8 w-8 text-emerald-500" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
					<path stroke-linecap="round" stroke-linejoin="round" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" />
					<path stroke-linecap="round" stroke-linejoin="round" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
				</svg>
			</div>
			<div class="max-w-md space-y-1">
				<h2 class="text-xl font-bold text-zinc-900 dark:text-white">Settings Panel Under Development</h2>
				<p class="text-sm text-zinc-500 dark:text-zinc-400">
					Manage notification alerts, configure vulnerable group metrics, and modify geolocation preferences or Celsius/Fahrenheit units.
				</p>
			</div>
			<button class="mt-2 px-4.5 py-2.5 bg-zinc-900 dark:bg-zinc-850 hover:bg-zinc-800 dark:hover:bg-zinc-800/70 text-white dark:text-zinc-200 text-sm font-semibold rounded-xl transition-all shadow-sm focus:outline-none">
				Save Changes
			</button>
		</div>
	</div>
{/if}
