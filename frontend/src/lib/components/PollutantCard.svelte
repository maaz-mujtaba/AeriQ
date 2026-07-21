<script>
	import { untrack } from 'svelte';

	let {
		name = 'PM2.5',
		value = 0,
		unit = 'µg/m³',
		status = 'Good',
		trendDelta = '+2.4%',
		trendDirection = 'up', // up, down, flat
		sparklinePath = 'M0 25 Q15 5, 30 20 T60 10 T90 30 T120 15'
	} = $props();

	// Animated count-up state
	let displayValue = $state(0);

	$effect(() => {
		const end = parseFloat(value.toString()) || 0;
		const start = untrack(() => parseFloat(displayValue.toString()) || 0);
		const duration = 800; // ms
		
		/** @type {number | null} */
		let startTime = null;
		/** @type {number | null} */
		let animId = null;

		/** @param {number} timestamp */
		function animate(timestamp) {
			if (startTime === null) startTime = timestamp;
			const elapsed = timestamp - startTime;
			const progress = Math.min(elapsed / duration, 1);
			const ease = progress * (2 - progress); // easeOutQuad
			const rawVal = start + (end - start) * ease;
			
			if (name.toUpperCase() === 'CO') {
				displayValue = parseFloat(rawVal.toFixed(1));
			} else {
				displayValue = Math.round(rawVal);
			}

			if (progress < 1) {
				animId = requestAnimationFrame(animate);
			}
		}
		animId = requestAnimationFrame(animate);

		return () => {
			if (animId !== null) cancelAnimationFrame(animId);
		};
	});

	// Select color matching the status
	let statusTheme = $derived.by(() => {
		const s = status.toLowerCase();
		if (s === 'good') {
			return {
				bg: 'bg-emerald-500/10 text-emerald-600 dark:text-emerald-400',
				sparklineColor: '#10b981',
				border: 'hover:border-emerald-500/30 dark:hover:border-emerald-500/30',
				glow: 'from-emerald-500/5 to-transparent shadow-emerald-500/2'
			};
		} else if (s === 'moderate') {
			return {
				bg: 'bg-amber-500/10 text-amber-600 dark:text-amber-400',
				sparklineColor: '#f59e0b',
				border: 'hover:border-amber-500/30 dark:hover:border-amber-500/30',
				glow: 'from-amber-500/5 to-transparent shadow-amber-500/2'
			};
		} else {
			return {
				bg: 'bg-red-500/10 text-red-600 dark:text-red-400',
				sparklineColor: '#ef4444',
				border: 'hover:border-red-500/30 dark:hover:border-red-500/30',
				glow: 'from-red-500/5 to-transparent shadow-red-500/2'
			};
		}
	});
</script>

<div class="relative overflow-hidden bg-white/40 dark:bg-zinc-900/40 border border-white/20 dark:border-zinc-800/80 rounded-2xl p-5 shadow-sm transition-all duration-300 hover:-translate-y-1 hover:shadow-md hover:bg-white dark:hover:bg-zinc-900 {statusTheme.border} flex flex-col justify-between h-[180px]">
	<!-- Ambient subtle card background glow -->
	<div class="absolute -top-12 -right-12 h-20 w-20 rounded-full bg-emerald-500/5 blur-2xl opacity-35 pointer-events-none"></div>

	<!-- Header: Name & Status -->
	<div class="flex items-center justify-between z-10">
		<div class="flex items-center gap-2">
			<!-- Colored indicator status ring -->
			<span class="h-2 w-2 rounded-full ring-4 ring-current {statusTheme.bg.split(' ')[1]}"></span>
			<span class="text-sm font-bold text-zinc-800 dark:text-zinc-200 tracking-tight">{name}</span>
		</div>
		<span class="text-[9px] font-bold px-2.5 py-0.5 rounded-full {statusTheme.bg}">
			{status}
		</span>
	</div>

	<!-- Value & Unit -->
	<div class="my-2 z-10">
		<h4 class="text-3xl font-black text-zinc-900 dark:text-white tracking-tight flex items-baseline">
			{displayValue}
			<span class="text-xs font-bold text-zinc-400 dark:text-zinc-500 ml-1">{unit}</span>
		</h4>
		
		<!-- 24-Hour Trend Indicator -->
		<div class="flex items-center gap-1.5 mt-1 text-[10px] font-bold">
			{#if trendDirection === 'up'}
				<span class="text-rose-500 flex items-center gap-0.5">
					<svg class="h-3 w-3" fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24">
						<path stroke-linecap="round" stroke-linejoin="round" d="M4.5 19.5l15-15m0 0H8.25m11.25 0v11.25" />
					</svg>
					{trendDelta}
				</span>
				<span class="text-zinc-400 dark:text-zinc-500">vs 24h ago</span>
			{:else if trendDirection === 'down'}
				<span class="text-emerald-500 flex items-center gap-0.5">
					<svg class="h-3 w-3" fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24">
						<path stroke-linecap="round" stroke-linejoin="round" d="M19.5 4.5l-15 15m0 0h11.25m-11.25 0V8.25" />
					</svg>
					{trendDelta}
				</span>
				<span class="text-zinc-400 dark:text-zinc-500">vs 24h ago</span>
			{:else}
				<span class="text-zinc-400 dark:text-zinc-500">Stable</span>
			{/if}
		</div>
	</div>

	<!-- Sparkline Chart -->
	<div class="h-10 w-full mt-1 relative z-10 select-none">
		<svg class="w-full h-full" viewBox="0 0 120 40" preserveAspectRatio="none">
			<!-- Wavy line -->
			<path
				d={sparklinePath}
				fill="none"
				stroke={statusTheme.sparklineColor}
				stroke-width="2.2"
				stroke-linecap="round"
				class="transition-all duration-700"
			/>
			<!-- Gradient under sparkline -->
			<path
				d="{sparklinePath} L120 40 L0 40 Z"
				fill="url(#sparkline-gradient-{name})"
				opacity="0.06"
			/>

			<!-- SVG Definitions -->
			<defs>
				<linearGradient id="sparkline-gradient-{name}" x1="0" y1="0" x2="0" y2="1">
					<stop offset="0%" stop-color={statusTheme.sparklineColor} />
					<stop offset="100%" stop-color={statusTheme.sparklineColor} stop-opacity="0" />
				</linearGradient>
			</defs>
		</svg>
	</div>
</div>
