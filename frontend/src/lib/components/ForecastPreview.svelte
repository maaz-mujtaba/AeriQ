<script>
	// Props using Svelte 5 runes
	let { baseAqi = 185 } = $props();

	// Dynamic mapper functions to ensure coherence
	/** @param {number} aqi */
	function getLabel(aqi) {
		if (aqi <= 50) return 'Good';
		if (aqi <= 100) return 'Moderate';
		if (aqi <= 150) return 'Sensitive Warn';
		if (aqi <= 200) return 'Unhealthy';
		if (aqi <= 300) return 'Very Unhealthy';
		return 'Hazardous';
	}

	/** @param {number} aqi */
	function getColor(aqi) {
		if (aqi <= 50) return '#10b981';
		if (aqi <= 100) return '#f59e0b';
		if (aqi <= 150) return '#f97316';
		if (aqi <= 200) return '#ef4444';
		if (aqi <= 300) return '#a855f7';
		return '#881337';
	}

	/** @param {number} aqi */
	function getBg(aqi) {
		if (aqi <= 50) return 'bg-emerald-500/10 text-emerald-600 dark:text-emerald-450';
		if (aqi <= 100) return 'bg-amber-500/10 text-amber-600 dark:text-amber-450';
		if (aqi <= 150) return 'bg-orange-500/10 text-orange-600 dark:text-orange-450';
		if (aqi <= 200) return 'bg-red-500/10 text-red-600 dark:text-red-450';
		if (aqi <= 300) return 'bg-purple-500/10 text-purple-600 dark:text-purple-450';
		return 'bg-rose-950/20 text-rose-800 dark:text-rose-450';
	}

	/** @param {number} aqi */
	function getIcon(aqi) {
		if (aqi <= 50) return 'sun';
		if (aqi <= 120) return 'cloud';
		return 'haze';
	}

	/** @param {number} aqi */
	function getTempRange(aqi) {
		if (aqi > 150) return { high: 34, low: 26 };
		if (aqi > 90) return { high: 28, low: 21 };
		if (aqi > 40) return { high: 22, low: 16 };
		return { high: 18, low: 11 };
	}

	// Build dynamic dataset
	let dataset = $derived.by(() => {
		const base = baseAqi;
		const days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'];
		const multipliers = [1.0, 1.05, 1.12, 0.95, 0.76, 0.52, 0.40];

		return days.map((day, i) => {
			const aqiVal = Math.max(Math.round(base * multipliers[i]), 10);
			const temps = getTempRange(aqiVal);
			return {
				day,
				aqi: aqiVal,
				label: getLabel(aqiVal),
				color: getColor(aqiVal),
				bgClass: getBg(aqiVal),
				icon: getIcon(aqiVal),
				tempHigh: temps.high,
				tempLow: temps.low
			};
		});
	});

	// Calculate weekly trend mini path
	let sparklinePath = $derived.by(() => {
		const len = dataset.length;
		const width = 280;
		const height = 40;
		const padding = 5;
		const maxAqi = Math.max(...dataset.map(d => d.aqi), 200);

		const coords = dataset.map((d, index) => {
			const x = padding + (index * (width - 2 * padding)) / (len - 1);
			const y = height - padding - (d.aqi * (height - 2 * padding)) / maxAqi;
			return `${x},${y}`;
		});

		return coords.length > 0 ? `M ${coords.join(' L ')}` : '';
	});
</script>

<div class="relative overflow-hidden bg-white/40 dark:bg-zinc-900/40 border border-white/20 dark:border-zinc-800/80 backdrop-blur-xl rounded-2xl p-6 shadow-md transition-all duration-300 flex flex-col justify-between h-full min-h-[300px]">
	<!-- Header -->
	<div class="flex items-center justify-between mb-4 z-10">
		<div class="space-y-1">
			<span class="text-xs font-bold text-zinc-400 dark:text-zinc-500 uppercase tracking-wider">Weekly Outlook</span>
			<h3 class="text-lg font-black text-zinc-900 dark:text-white">Next 7 Days AQI</h3>
		</div>

		<!-- Mini sparkline chart in header -->
		<div class="h-8 w-28 hidden xs:block">
			<svg class="h-full w-full" viewBox="0 0 280 40">
				{#if sparklinePath}
					<path d={sparklinePath} fill="none" stroke="#10b981" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" />
				{/if}
			</svg>
		</div>
	</div>

	<!-- Weekly List Rows -->
	<div class="space-y-2 z-10">
		{#each dataset as day}
			<div class="flex items-center justify-between py-1.5 border-b border-zinc-200/20 dark:border-zinc-800/20 last:border-0 hover:bg-zinc-50/50 dark:hover:bg-zinc-850/20 px-2 rounded-xl transition-colors">
				
				<!-- Day label -->
				<span class="text-sm font-bold text-zinc-800 dark:text-zinc-200 w-10">{day.day}</span>

				<!-- Weather Vector Icon -->
				<div class="h-5 w-5 text-zinc-400 dark:text-zinc-500 shrink-0">
					{#if day.icon === 'sun'}
						<svg class="h-full w-full text-amber-500" fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24">
							<path stroke-linecap="round" stroke-linejoin="round" d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364-6.364l-.707.707M6.343 17.657l-.707.707m0-12.728l.707.707m12.728 12.728l.707-.707M12 8a4 4 0 100 8 4 4 0 000-8z" />
						</svg>
					{:else if day.icon === 'cloud'}
						<svg class="h-full w-full text-zinc-400" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
							<path stroke-linecap="round" stroke-linejoin="round" d="M3 15a4 4 0 004 4h9a5 5 0 10-.1-9.999 5.002 5.002 0 10-9.78 2.096A4.001 4.001 0 003 15z" />
						</svg>
					{:else}
						<svg class="h-full w-full text-zinc-400 dark:text-zinc-600 animate-pulse" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
							<path stroke-linecap="round" stroke-linejoin="round" d="M4 6h16M4 10h16M4 14h16M4 18h16" />
						</svg>
					{/if}
				</div>

				<!-- High/Low Temperature range -->
				<span class="text-xs font-bold text-zinc-500 dark:text-zinc-400 w-16 text-center">
					{day.tempHigh}° <span class="text-[10px] text-zinc-350 dark:text-zinc-600 font-semibold">/ {day.tempLow}°</span>
				</span>

				<!-- Dynamic Warning Bullet + Label -->
				<div class="flex items-center gap-1.5 flex-1 justify-start ml-3">
					<span class="h-2.5 w-2.5 rounded-full shrink-0 border border-white dark:border-zinc-900" style="background-color: {day.color}"></span>
					<span class="text-[10px] font-bold text-zinc-500 dark:text-zinc-500 truncate max-w-[90px]">{day.label}</span>
				</div>

				<!-- Numeric AQI status badge -->
				<span class="text-xs font-black px-2.5 py-0.5 rounded-md {day.bgClass}">
					{day.aqi} AQI
				</span>
			</div>
		{/each}
	</div>

	<!-- Action Footer -->
	<div class="mt-4 z-10">
		<a
			href="/forecast"
			class="w-full flex items-center justify-center gap-1 px-4 py-2.5 bg-zinc-950 dark:bg-zinc-800 hover:bg-zinc-900 dark:hover:bg-zinc-700 active:scale-[0.99] text-white text-xs font-bold rounded-xl transition-all shadow-sm focus:outline-none"
		>
			View Full Forecast
			<svg class="h-3.5 w-3.5 text-zinc-400" fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24">
				<path stroke-linecap="round" stroke-linejoin="round" d="M9 5l7 7-7 7" />
			</svg>
		</a>
	</div>
</div>
