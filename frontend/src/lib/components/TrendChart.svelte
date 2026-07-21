<script>
	// Props using Svelte 5 runes
	let { baseAqi = 185 } = $props();

	// Timeline Selector Range (24H, 7D, 30D)
	let activeRange = $state('24H');

	// Dynamically generate dataset matching base AQI of active city profile
	let dataset = $derived.by(() => {
		const base = baseAqi;
		if (activeRange === '24H') {
			return [
				{ time: '09:00', aqi: Math.max(Math.round(base * 0.70), 10) },
				{ time: '12:00', aqi: Math.max(Math.round(base * 0.85), 10) },
				{ time: '15:00', aqi: Math.max(Math.round(base), 10) },
				{ time: '18:00', aqi: Math.max(Math.round(base * 0.95), 10) },
				{ time: '21:00', aqi: Math.max(Math.round(base * 0.80), 10) },
				{ time: '00:00', aqi: Math.max(Math.round(base * 0.70), 10) },
				{ time: '03:00', aqi: Math.max(Math.round(base * 0.60), 10) },
				{ time: '06:00', aqi: Math.max(Math.round(base * 0.50), 10) }
			];
		} else if (activeRange === '7D') {
			return [
				{ time: 'Mon', aqi: Math.max(Math.round(base * 0.68), 10) },
				{ time: 'Tue', aqi: Math.max(Math.round(base * 0.75), 10) },
				{ time: 'Wed', aqi: Math.max(Math.round(base * 0.97), 10) },
				{ time: 'Thu', aqi: Math.max(Math.round(base * 0.89), 10) },
				{ time: 'Fri', aqi: Math.max(Math.round(base * 0.75), 10) },
				{ time: 'Sat', aqi: Math.max(Math.round(base * 0.50), 10) },
				{ time: 'Sun', aqi: Math.max(Math.round(base * 0.40), 10) }
			];
		} else {
			// 30 Days trend points
			return [
				{ time: 'Day 1', aqi: Math.max(Math.round(base * 0.60), 10) },
				{ time: 'Day 4', aqi: Math.max(Math.round(base * 0.70), 10) },
				{ time: 'Day 8', aqi: Math.max(Math.round(base * 0.80), 10) },
				{ time: 'Day 12', aqi: Math.max(Math.round(base * 0.92), 10) },
				{ time: 'Day 16', aqi: Math.max(Math.round(base * 0.82), 10) },
				{ time: 'Day 20', aqi: Math.max(Math.round(base * 0.68), 10) },
				{ time: 'Day 24', aqi: Math.max(Math.round(base * 0.60), 10) },
				{ time: 'Day 28', aqi: Math.max(Math.round(base * 0.50), 10) },
				{ time: 'Day 30', aqi: Math.max(Math.round(base * 0.38), 10) }
			];
		}
	});

	// SVG Dimensions
	const viewWidth = 600;
	const viewHeight = 220;
	const padLeft = 40;
	const padRight = 20;
	const padTop = 30;
	const padBottom = 35;

	// Calculate max AQI dynamically (min 200 for chart structure)
	let maxVal = $derived(Math.max(...dataset.map(d => d.aqi), 200));

	// Calculate absolute SVG drawing points
	let chartPoints = $derived.by(() => {
		const len = dataset.length;
		const widthSpan = viewWidth - padLeft - padRight;
		const heightSpan = viewHeight - padTop - padBottom;

		return dataset.map((d, index) => {
			const x = padLeft + (index * widthSpan) / (len - 1);
			const y = viewHeight - padBottom - (d.aqi * heightSpan) / maxVal;
			return { x, y, aqi: d.aqi, time: d.time };
		});
	});

	// Construct SVG Paths
	let linePath = $derived(chartPoints.length > 0 ? `M ${chartPoints[0].x} ${chartPoints[0].y} ` + chartPoints.slice(1).map(p => `L ${p.x} ${p.y}`).join(' ') : '');
	let areaPath = $derived(chartPoints.length > 0 ? `${linePath} L ${chartPoints[chartPoints.length - 1].x} ${viewHeight - padBottom} L ${chartPoints[0].x} ${viewHeight - padBottom} Z` : '');

	// Gridlines mapping (e.g. 50, 100, 150, 200)
	let gridlines = $derived.by(() => {
		const vals = [50, 100, 150, 200, 300];
		const heightSpan = viewHeight - padTop - padBottom;
		return vals.filter(v => v < maxVal).map(v => {
			const y = viewHeight - padBottom - (v * heightSpan) / maxVal;
			return { y, value: v };
		});
	});

	// Tooltip hover track states
	let hoveredIndex = $state(-1);
</script>

<div class="relative overflow-hidden bg-white/40 dark:bg-zinc-900/40 border border-white/20 dark:border-zinc-800/80 backdrop-blur-xl rounded-2xl p-6 shadow-md transition-all duration-300 flex flex-col justify-between h-full min-h-[300px]">
	<!-- Header -->
	<div class="flex flex-col sm:flex-row sm:items-center justify-between gap-3 mb-4 z-10">
		<div class="space-y-1">
			<span class="text-xs font-bold text-zinc-400 dark:text-zinc-500 uppercase tracking-wider">Predictive Trend</span>
			<h3 class="text-lg font-black text-zinc-900 dark:text-white">Air Quality Chart</h3>
		</div>
		
		<!-- Time Selector Buttons -->
		<div class="flex items-center gap-1 p-0.5 bg-zinc-100 dark:bg-zinc-800 rounded-lg select-none max-w-fit border border-zinc-200/50 dark:border-zinc-700/50">
			<button
				onclick={() => { activeRange = '24H'; hoveredIndex = -1; }}
				class="px-2.5 py-1 text-[10px] font-bold rounded transition-all focus:outline-none {activeRange === '24H' ? 'bg-white dark:bg-zinc-900 text-emerald-600 dark:text-emerald-450 shadow-sm' : 'text-zinc-400 dark:text-zinc-500 hover:text-zinc-700 dark:hover:text-zinc-300'}"
			>
				24H
			</button>
			<button
				onclick={() => { activeRange = '7D'; hoveredIndex = -1; }}
				class="px-2.5 py-1 text-[10px] font-bold rounded transition-all focus:outline-none {activeRange === '7D' ? 'bg-white dark:bg-zinc-900 text-emerald-600 dark:text-emerald-450 shadow-sm' : 'text-zinc-400 dark:text-zinc-500 hover:text-zinc-700 dark:hover:text-zinc-300'}"
			>
				7D
			</button>
			<button
				onclick={() => { activeRange = '30D'; hoveredIndex = -1; }}
				class="px-2.5 py-1 text-[10px] font-bold rounded transition-all focus:outline-none {activeRange === '30D' ? 'bg-white dark:bg-zinc-900 text-emerald-600 dark:text-emerald-450 shadow-sm' : 'text-zinc-400 dark:text-zinc-500 hover:text-zinc-700 dark:hover:text-zinc-300'}"
			>
				30D
			</button>
		</div>
	</div>

	<!-- Vector Line Graph Container -->
	<div class="relative w-full flex-1 min-h-0 select-none z-10 py-2">
		<svg class="w-full h-full" viewBox="0 0 {viewWidth} {viewHeight}" preserveAspectRatio="none">
			<!-- SVG Definitions: Gradients & Shadows -->
			<defs>
				<linearGradient id="chart-area-gradient-{activeRange}" x1="0" y1="0" x2="0" y2="1">
					<stop offset="0%" stop-color="#10b981" stop-opacity="0.25" />
					<stop offset="100%" stop-color="#10b981" stop-opacity="0.0" />
				</linearGradient>
			</defs>

			<!-- Horizontal Gridlines -->
			{#each gridlines as line}
				<line
					x1={padLeft}
					y1={line.y}
					x2={viewWidth - padRight}
					y2={line.y}
					stroke="currentColor"
					class="text-zinc-200 dark:text-zinc-800/60"
					stroke-width="1"
					stroke-dasharray="4,4"
				/>
				<text
					x={padLeft - 10}
					y={line.y + 4}
					text-anchor="end"
					class="fill-zinc-400 text-[10px] font-bold"
				>
					{line.value}
				</text>
			{/each}

			<!-- Bottom axis boundary line -->
			<line
				x1={padLeft}
				y1={viewHeight - padBottom}
				x2={viewWidth - padRight}
				y2={viewHeight - padBottom}
				stroke="currentColor"
				class="text-zinc-200 dark:text-zinc-800"
				stroke-width="1.5"
			/>

			<!-- Gradient Area Fill -->
			{#if areaPath}
				<path d={areaPath} fill="url(#chart-area-gradient-{activeRange})" class="transition-all duration-700" />
			{/if}

			<!-- Main Graph Line -->
			{#if linePath}
				<path
					d={linePath}
					fill="none"
					stroke="#10b981"
					stroke-width="3.2"
					stroke-linecap="round"
					stroke-linejoin="round"
					class="transition-all duration-700"
				/>
			{/if}

			<!-- Data point dot connectors (glow circles) -->
			{#each chartPoints as point, idx}
				<!-- Outer hover expand ring -->
				<circle
					cx={point.x}
					cy={point.y}
					r={hoveredIndex === idx ? 8 : 4}
					fill="#10b981"
					stroke="white"
					stroke-width="2.5"
					class="transition-all duration-300 cursor-pointer drop-shadow-sm"
				/>
			{/each}

			<!-- X Axis labels -->
			{#each chartPoints as point}
				<text
					x={point.x}
					y={viewHeight - 12}
					text-anchor="middle"
					class="fill-zinc-400 dark:fill-zinc-500 text-[10px] font-bold"
				>
					{point.time}
				</text>
			{/each}

			<!-- Interactive Hover Slices (Invisible vertical bars for easy tooltips) -->
			{#each chartPoints as point, idx}
				<rect
					x={point.x - (viewWidth - padLeft - padRight) / (dataset.length - 1) / 2}
					y={padTop}
					width={(viewWidth - padLeft - padRight) / (dataset.length - 1)}
					height={viewHeight - padTop - padBottom}
					fill="transparent"
					class="cursor-pointer"
					role="presentation"
					onmouseenter={() => (hoveredIndex = idx)}
					onmouseleave={() => (hoveredIndex = -1)}
				/>
			{/each}
		</svg>
	</div>

	<!-- Interactive Tooltip Overlay -->
	{#if hoveredIndex !== -1}
		<div class="absolute bottom-4 left-1/2 transform -translate-x-1/2 bg-zinc-900 text-white text-[10px] px-3 py-1.5 rounded-xl shadow-md flex items-center gap-2 border border-zinc-800 pointer-events-none z-20">
			<span class="font-black text-emerald-400">{dataset[hoveredIndex].aqi} AQI</span>
			<span class="text-zinc-500">|</span>
			<span class="font-bold text-zinc-300">{dataset[hoveredIndex].time}</span>
		</div>
	{/if}
</div>
