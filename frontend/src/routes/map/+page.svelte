<svelte:head>
	<title>AQI Map | AeriQ</title>
	<meta name="description" content="View global live AQI values on our interactive map." />
</svelte:head>

<div class="space-y-6">
	<!-- Breadcrumbs and Header -->
	<div class="space-y-1">
		<div class="flex items-center gap-2 text-xs font-semibold text-zinc-400 dark:text-zinc-500 uppercase tracking-wider">
			<span>App</span>
			<span>/</span>
			<span class="text-emerald-500 dark:text-emerald-400">AQI Map</span>
		</div>
		<h1 class="text-3xl font-extrabold tracking-tight text-zinc-900 dark:text-white">AQI Map</h1>
		<p class="text-sm text-zinc-500 dark:text-zinc-400">Geospatial heatmaps and station indexes for major cities.</p>
	</div>

	<!-- Main Card -->
	<div class="bg-white dark:bg-zinc-900 border border-zinc-200/80 dark:border-zinc-800/80 rounded-2xl p-8 shadow-sm flex flex-col items-center justify-center text-center min-h-[400px] gap-4 transition-all duration-300">
		<div class="h-16 w-16 rounded-2xl bg-emerald-50 dark:bg-emerald-950/30 text-emerald-500 flex items-center justify-center shadow-sm">
			<svg class="h-8 w-8 text-emerald-500 animate-spin" style="animation-duration: 6s;" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
				<path stroke-linecap="round" stroke-linejoin="round" d="M9 20l-5.447-2.724A1 1 0 013 16.382V5.618a1 1 0 011.447-.894L9 7m0 13l6-3m-6 3V7m6 10l4.553 2.276A1 1 0 0021 18.382V7.618a1 1 0 00-.553-.894L15 4m0 13V4m0 0L9 7" />
			</svg>
		</div>
		<div class="max-w-md space-y-1">
			<h2 class="text-xl font-bold text-zinc-900 dark:text-white">AQI Map Under Development</h2>
			<p class="text-sm text-zinc-500 dark:text-zinc-400">
				An interactive geospatial map layer showcasing air tracking stations worldwide. Filter by custom parameters (PM2.5, PM10, SO2, NO2).
			</p>
		</div>
		<button class="mt-2 px-4.5 py-2.5 bg-emerald-500 hover:bg-emerald-600 active:scale-95 text-white text-sm font-semibold rounded-xl transition-all shadow-md shadow-emerald-500/10 focus:outline-none">
			Initialize WebGL Map
		</button>
	</div>
</div>
