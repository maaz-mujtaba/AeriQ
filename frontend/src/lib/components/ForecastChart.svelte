<script lang="ts">
	interface Props {
		items?: any[];
		field?: string;
		title?: string;
		description?: string;
		suffix?: string;
		lineColor?: string;
		areaGradientId?: string;
		selectedIndex?: number;
		onselect?: (idx: number) => void;
	}

	let {
		items = [],
		field = 'aqi', // aqi, temperature, humidity, rain_chance, wind_speed, pressure
		title = 'Forecast Trend',
		description = 'Predicted values over the next several days.',
		suffix = '',
		lineColor = '#10b981',
		areaGradientId = 'chart-gradient-id',
		selectedIndex = 0,
		onselect = (idx: number) => {}
	}: Props = $props();

	// SVG Dimensions
	const viewWidth = 600;
	const viewHeight = 220;
	const padLeft = 40;
	const padRight = 20;
	const padTop = 30;
	const padBottom = 35;

	// Extract values based on field
	let values = $derived(items.map((d: any) => {
		if (field === 'rain_chance') {
			return d.rain_chance !== undefined ? d.rain_chance : Math.round(d.chance_of_improvement / 2);
		}
		return d[field] !== undefined ? d[field] : 0;
	}));

	let minVal = $derived.by(() => {
		if (values.length === 0) return 0;
		if (field === 'pressure') {
			return Math.min(...values) - 2;
		}
		return 0;
	});

	let maxVal = $derived.by(() => {
		if (values.length === 0) return 100;
		const m = Math.max(...values);
		if (field === 'pressure') {
			return m + 2;
		}
		if (field === 'aqi') {
			return Math.max(m, 150);
		}
		if (field === 'humidity' || field === 'rain_chance') {
			return 100;
		}
		return Math.max(m, 20);
	});

	interface ChartPoint {
		x: number;
		y: number;
		value: number;
		day: string;
		date: string;
		category?: string;
		color?: string;
	}

	// Calculate absolute drawing coordinates
	let chartPoints: ChartPoint[] = $derived.by(() => {
		const len = items.length;
		if (len === 0) return [];
		const widthSpan = viewWidth - padLeft - padRight;
		const heightSpan = viewHeight - padTop - padBottom;
		const valSpan = maxVal - minVal;

		return items.map((d: any, index: number) => {
			const val = values[index];
			const x = padLeft + (index * widthSpan) / (len - 1);
			const y = viewHeight - padBottom - ((val - minVal) * heightSpan) / (valSpan || 1);
			return { x, y, value: val, day: d.day, date: d.date, category: d.aqi_category, color: d.aqi_color || lineColor };
		});
	});

	// Smooth cubic bezier path generator
	function getBezierPath(points: ChartPoint[]): string {
		if (points.length === 0) return '';
		let d = `M ${points[0].x} ${points[0].y}`;
		for (let i = 0; i < points.length - 1; i++) {
			const p0 = points[i];
			const p1 = points[i + 1];
			// Control points for smooth horizontal curve
			const cp1x = p0.x + (p1.x - p0.x) / 3;
			const cp1y = p0.y;
			const cp2x = p0.x + 2 * (p1.x - p0.x) / 3;
			const cp2y = p1.y;
			d += ` C ${cp1x} ${cp1y}, ${cp2x} ${cp2y}, ${p1.x} ${p1.y}`;
		}
		return d;
	}

	let linePath = $derived(getBezierPath(chartPoints));
	let areaPath = $derived(chartPoints.length > 0 ? `${linePath} L ${chartPoints[chartPoints.length - 1].x} ${viewHeight - padBottom} L ${chartPoints[0].x} ${viewHeight - padBottom} Z` : '');

	// Gridlines mapping (dashed line helpers)
	let gridlines = $derived.by(() => {
		const heightSpan = viewHeight - padTop - padBottom;
		const valSpan = maxVal - minVal;
		
		let steps = [0.25, 0.5, 0.75];
		return steps.map(pct => {
			const val = minVal + valSpan * pct;
			const y = viewHeight - padBottom - (val - minVal) * heightSpan / (valSpan || 1);
			return { y, value: Math.round(val) };
		});
	});

	let hoveredIndex = $state(-1);
</script>

<div class="relative overflow-hidden bg-white/40 dark:bg-zinc-900/40 border border-white/20 dark:border-zinc-800/80 backdrop-blur-xl rounded-2xl p-6 shadow-md transition-all duration-300 flex flex-col justify-between h-[360px] w-full">
	
	<!-- Header Details -->
	<div class="flex flex-col sm:flex-row sm:items-center justify-between gap-3 mb-4 z-10">
		<div class="space-y-1">
			<span class="text-xs font-bold text-zinc-400 dark:text-zinc-500 uppercase tracking-wider">Historical & Predictive Projections</span>
			<h3 class="text-lg font-black text-zinc-900 dark:text-white">{title}</h3>
			<p class="text-xs text-zinc-500 dark:text-zinc-400">{description}</p>
		</div>
		
		<!-- Indicator of selected day -->
		{#if selectedIndex !== -1 && items[selectedIndex]}
			<div class="flex items-center gap-2 p-1.5 px-3 bg-zinc-100 dark:bg-zinc-800/80 border border-zinc-200/50 dark:border-zinc-700/50 rounded-xl max-w-fit shadow-sm">
				{#if field === 'aqi'}
					<span class="h-2 w-2 rounded-full" style="background-color: {items[selectedIndex].aqi_color};"></span>
				{/if}
				<span class="text-[10px] font-bold text-zinc-650 dark:text-zinc-300">
					{items[selectedIndex].day}: <span class="font-black text-zinc-900 dark:text-white">{values[selectedIndex]}{suffix}</span>
				</span>
			</div>
		{/if}
	</div>

	<!-- Vector Line Graph Container -->
	<div class="relative w-full flex-1 min-h-0 select-none z-10 py-2">
		<svg class="w-full h-full" viewBox="0 0 {viewWidth} {viewHeight}" preserveAspectRatio="none">
			<!-- SVG Definitions: Gradients -->
			<defs>
				<linearGradient id={areaGradientId} x1="0" y1="0" x2="0" y2="1">
					<stop offset="0%" stop-color={lineColor} stop-opacity="0.25" />
					<stop offset="100%" stop-color={lineColor} stop-opacity="0.0" />
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
					y={line.y + 3.5}
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
				<path d={areaPath} fill="url(#{areaGradientId})" class="transition-all duration-700" />
			{/if}

			<!-- Main Graph Line -->
			{#if linePath}
				<path
					d={linePath}
					fill="none"
					stroke={lineColor}
					stroke-width="3.2"
					stroke-linecap="round"
					stroke-linejoin="round"
					class="transition-all duration-700"
				/>
			{/if}

			<!-- Data point dot connectors (glow circles) -->
			{#each chartPoints as point, idx}
				<!-- Outer hover expand ring or selected state ring -->
				<circle
					cx={point.x}
					cy={point.y}
					r={selectedIndex === idx || hoveredIndex === idx ? 8 : 4}
					fill={field === 'aqi' ? point.color : lineColor}
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
					{point.day}
				</text>
			{/each}

			<!-- Interactive Hover Slices (Invisible vertical bars for easy tooltips and clicks) -->
			{#each chartPoints as point, idx}
				<rect
					x={point.x - (viewWidth - padLeft - padRight) / (items.length - 1) / 2}
					y={padTop}
					width={(viewWidth - padLeft - padRight) / (items.length - 1)}
					height={viewHeight - padTop - padBottom}
					fill="transparent"
					class="cursor-pointer"
					role="presentation"
					onmouseenter={() => (hoveredIndex = idx)}
					onmouseleave={() => (hoveredIndex = -1)}
					onclick={() => onselect(idx)}
				/>
			{/each}
		</svg>
	</div>

	<!-- Interactive Tooltip Overlay -->
	{#if hoveredIndex !== -1 && chartPoints[hoveredIndex]}
		<div class="absolute bottom-4 left-1/2 transform -translate-x-1/2 bg-zinc-900 text-white text-[10px] px-3 py-1.5 rounded-xl shadow-md flex items-center gap-2 border border-zinc-800 pointer-events-none z-20">
			{#if field === 'aqi'}
				<span class="h-1.5 w-1.5 rounded-full" style="background-color: {chartPoints[hoveredIndex].color};"></span>
				<span class="font-black text-white">{chartPoints[hoveredIndex].value} AQI</span>
				<span class="text-zinc-500">|</span>
				<span class="font-bold text-zinc-300 uppercase">{chartPoints[hoveredIndex].category}</span>
			{:else}
				<span class="font-black text-white">{chartPoints[hoveredIndex].value}{suffix}</span>
			{/if}
			<span class="text-zinc-500">|</span>
			<span class="font-bold text-zinc-300">{chartPoints[hoveredIndex].day}</span>
		</div>
	{/if}
</div>
