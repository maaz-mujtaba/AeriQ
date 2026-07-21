<script>
	import { loggedIn } from '$lib/stores/authStore.js';
	import LoginRequired from '$lib/components/LoginRequired.svelte';
</script>

<svelte:head>
	<title>Reports | AeriQ</title>
	<meta name="description" content="Generate and download customized PDF/CSV air quality reports." />
</svelte:head>

{#if !$loggedIn}
	<LoginRequired title="Reports Generator" description="Generate, compile, and schedule customized PDF, CSV, and JSON data exports for your monitor arrays." />
{:else}
	<div class="space-y-6">
		<!-- Breadcrumbs and Header -->
		<div class="space-y-1">
			<div class="flex items-center gap-2 text-xs font-semibold text-zinc-400 dark:text-zinc-500 uppercase tracking-wider">
				<span>App</span>
				<span>/</span>
				<span class="text-emerald-500 dark:text-emerald-400">Reports</span>
			</div>
			<h1 class="text-3xl font-extrabold tracking-tight text-zinc-900 dark:text-white">Reports</h1>
			<p class="text-sm text-zinc-500 dark:text-zinc-400">Generate, schedule, and compile structured logs and trends data.</p>
		</div>

		<!-- Main Card -->
		<div class="bg-white dark:bg-zinc-900 border border-zinc-200/80 dark:border-zinc-800/80 rounded-2xl p-8 shadow-sm flex flex-col items-center justify-center text-center min-h-[400px] gap-4 transition-all duration-300">
			<div class="h-16 w-16 rounded-2xl bg-emerald-50 dark:bg-emerald-950/30 text-emerald-500 flex items-center justify-center shadow-sm">
				<svg class="h-8 w-8 text-emerald-500" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
					<path stroke-linecap="round" stroke-linejoin="round" d="M9 17v-2m3 2v-4m3 4v-6m2 10H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
				</svg>
			</div>
			<div class="max-w-md space-y-1">
				<h2 class="text-xl font-bold text-zinc-900 dark:text-white">Reports Manager Under Development</h2>
				<p class="text-sm text-zinc-500 dark:text-zinc-400">
					Compile monthly statistics into publication-ready formats (PDF, CSV, JSON). Automate report deliveries straight to your email.
				</p>
			</div>
			<button class="mt-2 px-4.5 py-2.5 bg-emerald-500 hover:bg-emerald-600 active:scale-95 text-white text-sm font-semibold rounded-xl transition-all shadow-md shadow-emerald-500/10 focus:outline-none">
				Generate PDF Report
			</button>
		</div>
	</div>
{/if}
