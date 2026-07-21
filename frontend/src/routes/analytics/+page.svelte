<svelte:head>
	<title>Analytics | AeriQ</title>
	<meta name="description" content="View historical air quality charts and historical pollution statistics." />
</svelte:head>

<div class="space-y-6">
	<!-- Breadcrumbs and Header -->
	<div class="space-y-1">
		<div class="flex items-center gap-2 text-xs font-semibold text-zinc-400 dark:text-zinc-500 uppercase tracking-wider">
			<span>App</span>
			<span>/</span>
			<span class="text-emerald-500 dark:text-emerald-400">Analytics</span>
		</div>
		<h1 class="text-3xl font-extrabold tracking-tight text-zinc-900 dark:text-white">Analytics</h1>
		<p class="text-sm text-zinc-500 dark:text-zinc-400">Deep-dive reports, historical air quality patterns, and factor correlation.</p>
	</div>

	<!-- Main Card -->
	<div class="bg-white dark:bg-zinc-900 border border-zinc-200/80 dark:border-zinc-800/80 rounded-2xl p-8 shadow-sm flex flex-col items-center justify-center text-center min-h-[400px] gap-4 transition-all duration-300">
		<div class="h-16 w-16 rounded-2xl bg-emerald-50 dark:bg-emerald-950/30 text-emerald-500 flex items-center justify-center shadow-sm">
			<svg class="h-8 w-8" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
				<path stroke-linecap="round" stroke-linejoin="round" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
			</svg>
		</div>
		<div class="max-w-md space-y-1">
			<h2 class="text-xl font-bold text-zinc-900 dark:text-white">Analytics Panel Under Development</h2>
			<p class="text-sm text-zinc-500 dark:text-zinc-400">
				Here you will be able to analyze long-term trends, download CSV history archives, and visualize pollutant indexes against environmental metrics.
			</p>
		</div>
		<div class="flex items-center gap-2 mt-2">
			<span class="h-2.5 w-2.5 rounded-full bg-emerald-500"></span>
			<span class="text-xs text-zinc-400 dark:text-zinc-500 font-semibold uppercase tracking-wider">Ready to connect to API</span>
		</div>
	</div>
</div>
