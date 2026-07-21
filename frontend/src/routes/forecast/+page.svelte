<svelte:head>
	<title>Forecast | AeriQ</title>
	<meta name="description" content="View air quality predictions for the next 24 to 72 hours." />
</svelte:head>

<div class="space-y-6">
	<!-- Breadcrumbs and Header -->
	<div class="space-y-1">
		<div class="flex items-center gap-2 text-xs font-semibold text-zinc-400 dark:text-zinc-500 uppercase tracking-wider">
			<span>App</span>
			<span>/</span>
			<span class="text-emerald-500 dark:text-emerald-400">Forecast</span>
		</div>
		<h1 class="text-3xl font-extrabold tracking-tight text-zinc-900 dark:text-white">Forecast</h1>
		<p class="text-sm text-zinc-500 dark:text-zinc-400">Future projections for PM2.5, PM10, and ozone concentrations.</p>
	</div>

	<!-- Main Card -->
	<div class="bg-white dark:bg-zinc-900 border border-zinc-200/80 dark:border-zinc-800/80 rounded-2xl p-8 shadow-sm flex flex-col items-center justify-center text-center min-h-[400px] gap-4 transition-all duration-300">
		<div class="h-16 w-16 rounded-2xl bg-emerald-50 dark:bg-emerald-950/30 text-emerald-500 flex items-center justify-center shadow-sm animate-pulse">
			<svg class="h-8 w-8" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
				<path stroke-linecap="round" stroke-linejoin="round" d="M3 15a4 4 0 004 4h9a5 5 0 10-.1-9.999 5.002 5.002 0 10-9.78 2.096A4.001 4.001 0 003 15z" />
			</svg>
		</div>
		<div class="max-w-md space-y-1">
			<h2 class="text-xl font-bold text-zinc-900 dark:text-white">Forecast Under Development</h2>
			<p class="text-sm text-zinc-500 dark:text-zinc-400">
				Here you will find our ML-powered 24–72 hour air quality projections. Anticipate pollution spikes and optimize outdoor schedules.
			</p>
		</div>
		<div class="mt-2 flex items-center gap-3">
			<span class="px-3 py-1 bg-zinc-100 dark:bg-zinc-850 rounded-lg text-xs font-semibold text-zinc-500 dark:text-zinc-400">Model: LightGBM v1.2</span>
			<span class="px-3 py-1 bg-zinc-100 dark:bg-zinc-850 rounded-lg text-xs font-semibold text-zinc-500 dark:text-zinc-400">Accuracy: 94.2%</span>
		</div>
	</div>
</div>
