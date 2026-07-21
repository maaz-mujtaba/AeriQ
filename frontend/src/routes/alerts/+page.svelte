<svelte:head>
	<title>Alerts | AeriQ</title>
	<meta name="description" content="Set custom notifications and vulnerability group filters for air pollution warnings." />
</svelte:head>

<div class="space-y-6">
	<!-- Breadcrumbs and Header -->
	<div class="space-y-1">
		<div class="flex items-center gap-2 text-xs font-semibold text-zinc-400 dark:text-zinc-500 uppercase tracking-wider">
			<span>App</span>
			<span>/</span>
			<span class="text-emerald-500 dark:text-emerald-400">Alerts</span>
		</div>
		<h1 class="text-3xl font-extrabold tracking-tight text-zinc-900 dark:text-white">Alerts</h1>
		<p class="text-sm text-zinc-500 dark:text-zinc-400">Configure real-time air quality notifications and email warnings.</p>
	</div>

	<!-- Main Card -->
	<div class="bg-white dark:bg-zinc-900 border border-zinc-200/80 dark:border-zinc-800/80 rounded-2xl p-8 shadow-sm flex flex-col items-center justify-center text-center min-h-[400px] gap-4 transition-all duration-300">
		<div class="h-16 w-16 rounded-2xl bg-emerald-50 dark:bg-emerald-950/30 text-emerald-500 flex items-center justify-center shadow-sm">
			<svg class="h-8 w-8 animate-bounce" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
				<path stroke-linecap="round" stroke-linejoin="round" d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9" />
			</svg>
		</div>
		<div class="max-w-md space-y-1">
			<h2 class="text-xl font-bold text-zinc-900 dark:text-white">Alerts Management Under Development</h2>
			<p class="text-sm text-zinc-500 dark:text-zinc-400">
				Configure threshold alerts for ozone levels, particulate matter warnings, and configure customized email routing profiles for vulnerable family members.
			</p>
		</div>
		<button class="mt-2 px-4.5 py-2.5 bg-zinc-900 dark:bg-zinc-850 hover:bg-zinc-800 dark:hover:bg-zinc-800/70 text-white dark:text-zinc-200 text-sm font-semibold rounded-xl transition-all shadow-sm focus:outline-none">
			Configure Channels
		</button>
	</div>
</div>
