<svelte:head>
	<title>AQI Map | AeriQ</title>
	<meta name="description" content="View AQI values across major Indian cities on an interactive map." />
</svelte:head>

<script>
	import AQIMap from '$lib/components/AQIMap.svelte';
</script>

<div class="space-y-6">
	<!-- Breadcrumbs and Header -->
	<div class="space-y-1">
		<div class="flex items-center gap-2 text-xs font-semibold text-zinc-400 dark:text-zinc-500 uppercase tracking-wider">
			<span>App</span>
			<span>/</span>
			<span class="text-emerald-500 dark:text-emerald-400">AQI Map</span>
		</div>
		<h1 class="text-3xl font-extrabold tracking-tight text-zinc-900 dark:text-white">AQI Map</h1>
		<p class="text-sm text-zinc-500 dark:text-zinc-400">Interactive air quality index map for major Indian cities. Click markers to view detailed AQI data.</p>
	</div>

	<!-- AQI Map Component -->
	<AQIMap />
</div>
