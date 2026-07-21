<svelte:head>
	<title>About | AeriQ</title>
	<meta name="description" content="Learn more about AeriQ, our team, mission, and technology stack." />
</svelte:head>

<div class="space-y-6">
	<!-- Breadcrumbs and Header -->
	<div class="space-y-1">
		<div class="flex items-center gap-2 text-xs font-semibold text-zinc-400 dark:text-zinc-500 uppercase tracking-wider">
			<span>App</span>
			<span>/</span>
			<span class="text-emerald-500 dark:text-emerald-400">About</span>
		</div>
		<h1 class="text-3xl font-extrabold tracking-tight text-zinc-900 dark:text-white">About AeriQ</h1>
		<p class="text-sm text-zinc-500 dark:text-zinc-400">Our mission, technology, API citations, and scientific background.</p>
	</div>

	<!-- Main Card -->
	<div class="bg-white dark:bg-zinc-900 border border-zinc-200/80 dark:border-zinc-800/80 rounded-2xl p-8 shadow-sm flex flex-col items-center justify-center text-center min-h-[400px] gap-4 transition-all duration-300">
		<div class="h-16 w-16 rounded-2xl bg-emerald-50 dark:bg-emerald-950/30 text-emerald-500 flex items-center justify-center shadow-sm">
			<svg class="h-8 w-8 text-emerald-500" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
				<path stroke-linecap="round" stroke-linejoin="round" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
			</svg>
		</div>
		<div class="max-w-md space-y-1">
			<h2 class="text-xl font-bold text-zinc-900 dark:text-white">About AeriQ</h2>
			<p class="text-sm text-zinc-500 dark:text-zinc-400">
				AeriQ is an intelligent air quality tracking and forecast dashboard. Powered by advanced SvelteKit and LightGBM predictive models on our FastAPI backend.
			</p>
		</div>
		<div class="flex items-center gap-3 text-xs text-zinc-400 dark:text-zinc-500 font-semibold uppercase tracking-wider">
			<span>v1.0.0-Beta</span>
			<span>•</span>
			<span>FastAPI Backend</span>
			<span>•</span>
			<span>SvelteKit 5</span>
		</div>
	</div>
</div>
