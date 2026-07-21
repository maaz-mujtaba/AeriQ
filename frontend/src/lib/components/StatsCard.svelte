<script>
	// Props using Svelte 5 runes
	let {
		title = 'Cities Monitored',
		value = '250+',
		trend = '+5% this week',
		trendType = 'up', // up, down, neutral
		icon = 'cities' // cities, accuracy, alerts, rank
	} = $props();

	// Select colors for trend pill
	let trendStyles = $derived.by(() => {
		if (trendType === 'up') {
			return 'bg-emerald-500/10 text-emerald-600 dark:text-emerald-400';
		} else if (trendType === 'down') {
			return 'bg-rose-500/10 text-rose-600 dark:text-rose-450';
		} else {
			return 'bg-zinc-150 dark:bg-zinc-800 text-zinc-600 dark:text-zinc-400';
		}
	});
</script>

<div class="relative overflow-hidden bg-white/70 dark:bg-zinc-900/70 backdrop-blur-xl border border-zinc-200/80 dark:border-zinc-800/80 rounded-2xl p-5 shadow-sm hover:shadow-md transition-all duration-200 flex items-center gap-4">
	<!-- Left side icon -->
	<div class="h-10 w-10 rounded-xl bg-zinc-50 dark:bg-zinc-800 border border-zinc-200/60 dark:border-zinc-700/60 flex items-center justify-center text-zinc-500 shrink-0">
		{#if icon === 'cities'}
			<svg class="h-5 w-5 text-emerald-500" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
				<path stroke-linecap="round" stroke-linejoin="round" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
			</svg>
		{:else if icon === 'accuracy'}
			<svg class="h-5 w-5 text-blue-500" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
				<path stroke-linecap="round" stroke-linejoin="round" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
			</svg>
		{:else if icon === 'alerts'}
			<svg class="h-5 w-5 text-amber-500" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
				<path stroke-linecap="round" stroke-linejoin="round" d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9" />
			</svg>
		{:else}
			<svg class="h-5 w-5 text-purple-500" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
				<path stroke-linecap="round" stroke-linejoin="round" d="M9 12l2 2 4-4M7.835 4.697a3.42 3.42 0 001.946-.806 3.42 3.42 0 014.438 0 3.42 3.42 0 001.946.806 3.42 3.42 0 013.138 3.138 3.42 3.42 0 00.806 1.946 3.42 3.42 0 010 4.438 3.42 3.42 0 00-.806 1.946 3.42 3.42 0 01-3.138 3.138 3.42 3.42 0 00-1.946.806 3.42 3.42 0 01-4.438 0 3.42 3.42 0 00-1.946-.806 3.42 3.42 0 01-3.138-3.138 3.42 3.42 0 00-.806-1.946 3.42 3.42 0 010-4.438 3.42 3.42 0 00.806-1.946 3.42 3.42 0 013.138-3.138z" />
			</svg>
		{/if}
	</div>

	<!-- Title, value & trend -->
	<div class="flex-1 space-y-0.5">
		<p class="text-[10px] font-bold text-zinc-400 dark:text-zinc-500 uppercase tracking-wider">{title}</p>
		<div class="flex items-baseline gap-2">
			<h4 class="text-xl font-extrabold text-zinc-900 dark:text-white tracking-tight">{value}</h4>
			<span class="text-[9px] font-bold px-1.5 py-0.5 rounded-full {trendStyles}">
				{trend}
			</span>
		</div>
	</div>
</div>
