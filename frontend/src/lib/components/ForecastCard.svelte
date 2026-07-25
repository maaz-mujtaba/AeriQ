<script lang="ts">
	interface Props {
		day?: string;
		date?: string;
		aqi?: number;
		category?: string;
		color?: string;
		weatherIcon?: string;
		tempHigh?: number;
		tempLow?: number;
		humidity?: number;
		windSpeed?: number;
		rainChance?: number;
		sunrise?: string;
		sunset?: string;
		trendDirection?: string;
		healthMessage?: string;
		isSelected?: boolean;
		onclick?: (event: MouseEvent) => void;
	}

	let {
		day = 'TODAY',
		date = 'Jul 25',
		aqi = 82,
		category = 'Moderate',
		color = '#f59e0b',
		weatherIcon = 'sun',
		tempHigh = 34,
		tempLow = 27,
		humidity = 61,
		windSpeed = 10,
		rainChance = 10,
		sunrise = '5:42 AM',
		sunset = '7:11 PM',
		trendDirection = 'up',
		healthMessage = 'Good day for outdoor activity.',
		isSelected = false,
		onclick = () => {}
	}: Props = $props();

	// Badge styles matching dashboard category color bands
	let badgeStyles = $derived.by(() => {
		const cat = category.toLowerCase();
		if (cat === 'good') {
			return 'bg-emerald-500/10 text-emerald-700 dark:text-emerald-400 border border-emerald-500/10';
		} else if (cat === 'moderate' || cat === 'satisfactory') {
			return 'bg-amber-500/10 text-amber-700 dark:text-amber-450 border border-amber-500/10';
		} else if (cat === 'poor') {
			return 'bg-orange-500/10 text-orange-700 dark:text-orange-450 border border-orange-500/10';
		} else {
			return 'bg-red-500/10 text-red-700 dark:text-red-450 border border-red-500/10';
		}
	});

	// Dynamic highlight styles if selected
	let cardStyles = $derived(
		isSelected
			? 'border-emerald-500/60 dark:border-emerald-500/60 ring-2 ring-emerald-500/20 dark:ring-emerald-500/10 bg-white dark:bg-zinc-900 shadow-md scale-[1.02]'
			: 'border-white/20 dark:border-zinc-800/80 bg-white/40 dark:bg-zinc-900/40 hover:border-zinc-350 dark:hover:border-zinc-700 hover:bg-white dark:hover:bg-zinc-900 shadow-sm hover:shadow hover:-translate-y-1'
	);
</script>

<button
	{onclick}
	class="relative overflow-hidden rounded-2xl p-5 flex flex-col justify-between h-[300px] w-full text-left transition-all duration-300 backdrop-blur-xl select-none focus:outline-none cursor-pointer border {cardStyles}"
>
	<!-- Ambient top right card background glow -->
	<div
		class="absolute -top-12 -right-12 h-24 w-24 rounded-full blur-3xl opacity-20 pointer-events-none transition-all duration-300"
		style="background-color: {color};"
	></div>

	<!-- Top Section: Day label & High/Low Temp -->
	<div class="flex items-start justify-between w-full">
		<div class="space-y-0.5">
			<h4 class="text-sm font-black tracking-tight text-zinc-900 dark:text-white uppercase truncate">{day}</h4>
			<p class="text-[9px] text-zinc-400 dark:text-zinc-500 font-bold uppercase tracking-wider">{date}</p>
		</div>
		
		<!-- Large Weather Icon -->
		<div class="h-10 w-10 text-zinc-400 dark:text-zinc-500 shrink-0">
			{#if weatherIcon === 'sun'}
				<svg class="h-full w-full text-amber-500 animate-spin" style="animation-duration: 20s;" fill="none" stroke="currentColor" stroke-width="2.2" viewBox="0 0 24 24">
					<path stroke-linecap="round" stroke-linejoin="round" d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364-6.364l-.707.707M6.343 17.657l-.707.707m0-12.728l.707.707m12.728 12.728l.707-.707M12 8a4 4 0 100 8 4 4 0 000-8z" />
				</svg>
			{:else if weatherIcon === 'cloud'}
				<svg class="h-full w-full text-zinc-450 dark:text-zinc-400" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
					<path stroke-linecap="round" stroke-linejoin="round" d="M3 15a4 4 0 004 4h9a5 5 0 10-.1-9.999 5.002 5.002 0 10-9.78 2.096A4.001 4.001 0 003 15z" />
				</svg>
			{:else if weatherIcon === 'rain'}
				<svg class="h-full w-full text-blue-500" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
					<path stroke-linecap="round" stroke-linejoin="round" d="M3 15a4 4 0 004 4h9a5 5 0 10-.1-9.999 5.002 5.002 0 10-9.78 2.096A4.001 4.001 0 003 15z" />
					<path stroke-linecap="round" stroke-linejoin="round" d="M12 12v6M8 14v4M16 14v4" />
				</svg>
			{:else if weatherIcon === 'haze'}
				<svg class="h-full w-full text-zinc-400 dark:text-zinc-550 animate-pulse" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
					<path stroke-linecap="round" stroke-linejoin="round" d="M4 6h16M4 10h16M4 14h16M4 18h16" />
				</svg>
			{:else}
				<svg class="h-full w-full text-teal-500" fill="none" stroke="currentColor" stroke-width="2.2" viewBox="0 0 24 24">
					<path stroke-linecap="round" stroke-linejoin="round" d="M9.59 4.59A2 2 0 1111 8H2m10.59 11.41A2 2 0 1014 16H2m15.73-8.27A2.5 2.5 0 1119.5 12H2" />
				</svg>
			{/if}
		</div>
	</div>

	<!-- Weather temperature range values -->
	<div class="w-full">
		<p class="text-xs font-bold text-zinc-400 dark:text-zinc-500 uppercase tracking-wide leading-none">Temp Range</p>
		<p class="text-xl font-black text-zinc-800 dark:text-zinc-200 mt-1">
			{tempHigh}°C <span class="text-xs font-bold text-zinc-400 dark:text-zinc-650">/ {tempLow}°C</span>
		</p>
	</div>

	<!-- Center Section: AQI and Badge -->
	<div class="space-y-1 w-full">
		<div class="flex items-baseline gap-1.5">
			<span class="text-2xl sm:text-3xl font-black tracking-tight leading-none text-zinc-900 dark:text-white">{aqi}</span>
			<span class="text-[9px] text-zinc-400 dark:text-zinc-500 font-bold uppercase tracking-wider">AQI</span>
			
			<!-- Small trend arrow -->
			<div class="ml-1 select-none flex items-center">
				{#if trendDirection === 'up'}
					<svg class="h-3.5 w-3.5 text-red-500 animate-pulse" fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24">
						<path stroke-linecap="round" stroke-linejoin="round" d="M4.5 19.5l15-15m0 0H8.25m11.25 0v11.25" />
					</svg>
				{:else if trendDirection === 'down'}
					<svg class="h-3.5 w-3.5 text-emerald-500 animate-pulse" fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24">
						<path stroke-linecap="round" stroke-linejoin="round" d="M4.5 4.5l15 15m0 0V8.25m0 11.25H8.25" />
					</svg>
				{:else}
					<svg class="h-3.5 w-3.5 text-zinc-400" fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24">
						<path stroke-linecap="round" stroke-linejoin="round" d="M19.5 12h-15" />
					</svg>
				{/if}
			</div>
		</div>
		<span class="inline-block text-[8px] font-black uppercase px-2 py-0.5 rounded tracking-wider leading-none {badgeStyles}">
			{category}
		</span>
	</div>

	<!-- Small health tip message -->
	<p class="text-[10px] text-zinc-500 dark:text-zinc-400 italic line-clamp-1 w-full font-medium">
		{healthMessage}
	</p>

	<!-- Bottom Section: Quick stats (Sunrise, Sunset, Rain, Hum, Wind) -->
	<div class="w-full pt-3 border-t border-zinc-200/40 dark:border-zinc-800/40 grid grid-cols-3 gap-1 text-center text-[9px] font-bold text-zinc-400">
		<div>
			<p class="text-[7.5px] uppercase tracking-wider text-zinc-400 dark:text-zinc-550">Rain</p>
			<p class="text-zinc-700 dark:text-zinc-300 truncate mt-0.5">{rainChance}%</p>
		</div>
		<div>
			<p class="text-[7.5px] uppercase tracking-wider text-zinc-400 dark:text-zinc-550">Wind</p>
			<p class="text-zinc-700 dark:text-zinc-300 truncate mt-0.5">{windSpeed} km/h</p>
		</div>
		<div>
			<p class="text-[7.5px] uppercase tracking-wider text-zinc-400 dark:text-zinc-550">Sun</p>
			<p class="text-zinc-700 dark:text-zinc-300 truncate mt-0.5" title="Sunrise/Sunset: {sunrise} / {sunset}">
				{sunrise.split(' ')[0]}
			</p>
		</div>
	</div>
</button>
