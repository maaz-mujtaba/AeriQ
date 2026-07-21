<script>
	import AQIGauge from './AQIGauge.svelte';

	let {
		aqi = 0,
		location = 'New Delhi, India',
		lastUpdated = 'Just now'
	} = $props();

	// Derive specific gradient classes and shadow states based on AQI
	let theme = $derived.by(() => {
		if (aqi <= 50) {
			return {
				bgGradient: 'bg-gradient-to-br from-emerald-500/8 via-zinc-50/10 to-transparent border-emerald-500/20 dark:border-emerald-500/30 shadow-emerald-500/5',
				glowPulse: 'bg-emerald-400/20',
				textColor: 'text-emerald-600 dark:text-emerald-400',
				tagline: 'Fresh & Clean Air',
				badgeBg: 'bg-emerald-100 dark:bg-emerald-950/40 text-emerald-700 dark:text-emerald-400'
			};
		} else if (aqi <= 100) {
			return {
				bgGradient: 'bg-gradient-to-br from-amber-500/8 via-zinc-50/10 to-transparent border-amber-500/20 dark:border-amber-500/30 shadow-amber-500/5',
				glowPulse: 'bg-amber-400/20',
				textColor: 'text-amber-600 dark:text-amber-400',
				tagline: 'Moderate Air Quality',
				badgeBg: 'bg-amber-100 dark:bg-amber-950/40 text-amber-700 dark:text-amber-400'
			};
		} else if (aqi <= 150) {
			return {
				bgGradient: 'bg-gradient-to-br from-orange-500/8 via-zinc-50/10 to-transparent border-orange-500/20 dark:border-orange-500/30 shadow-orange-500/5',
				glowPulse: 'bg-orange-400/20',
				textColor: 'text-orange-600 dark:text-orange-400',
				tagline: 'Unhealthy for Sensitive Groups',
				badgeBg: 'bg-orange-100 dark:bg-orange-950/40 text-orange-700 dark:text-orange-400'
			};
		} else if (aqi <= 200) {
			return {
				bgGradient: 'bg-gradient-to-br from-red-500/8 via-zinc-50/10 to-transparent border-red-500/20 dark:border-red-500/30 shadow-red-500/5',
				glowPulse: 'bg-red-400/20',
				textColor: 'text-red-600 dark:text-red-400',
				tagline: 'Unhealthy Air Conditions',
				badgeBg: 'bg-red-100 dark:bg-red-950/40 text-red-700 dark:text-red-400'
			};
		} else if (aqi <= 300) {
			return {
				bgGradient: 'bg-gradient-to-br from-purple-500/8 via-zinc-50/10 to-transparent border-purple-500/20 dark:border-purple-500/30 shadow-purple-500/5',
				glowPulse: 'bg-purple-400/20',
				textColor: 'text-purple-600 dark:text-purple-400',
				tagline: 'Very Unhealthy Air Quality',
				badgeBg: 'bg-purple-100 dark:bg-purple-950/40 text-purple-700 dark:text-purple-400'
			};
		} else {
			return {
				bgGradient: 'bg-gradient-to-br from-rose-950/15 via-rose-900/2 to-transparent border-rose-900/20 dark:border-rose-900/30 shadow-rose-950/5',
				glowPulse: 'bg-rose-500/30',
				textColor: 'text-rose-800 dark:text-rose-450',
				tagline: 'Hazardous Conditions',
				badgeBg: 'bg-rose-200 dark:bg-rose-950/40 text-rose-800 dark:text-rose-450'
			};
		}
	});
</script>

<div class="relative overflow-hidden bg-white/40 dark:bg-zinc-900/40 border border-white/20 dark:border-zinc-800/80 backdrop-blur-xl rounded-2xl p-6 shadow-md transition-all duration-500 flex flex-col justify-between min-h-[300px] {theme.bgGradient}">
	
	<!-- Wavy breeze lines in background -->
	<div class="absolute inset-0 pointer-events-none z-0 opacity-15 dark:opacity-[0.06] text-emerald-500 dark:text-emerald-400">
		<svg class="h-full w-full" viewBox="0 0 450 200" fill="none" stroke="currentColor" stroke-width="1.5">
			<path d="M-20 80 Q60 50, 180 80 T380 60 T500 90" stroke-linecap="round" />
			<path d="M-20 110 Q80 80, 200 110 T400 70 T500 120" stroke-linecap="round" />
		</svg>
	</div>

	<!-- Ambient glow -->
	<div class="absolute -top-12 -left-12 h-32 w-32 rounded-full blur-3xl opacity-30 pointer-events-none {theme.glowPulse}"></div>

	<!-- Content split layout -->
	<div class="relative z-10 flex flex-col md:flex-row items-center gap-6 md:gap-8">
		<!-- Gauge Section -->
		<div class="shrink-0 flex items-center justify-center">
			<AQIGauge {aqi} />
		</div>

		<!-- Details Section -->
		<div class="flex-1 space-y-4 text-center md:text-left">
			<div class="space-y-1">
				<div class="flex items-center justify-center md:justify-start gap-1 text-zinc-400 dark:text-zinc-500 text-xs font-bold uppercase tracking-wider">
					<svg class="h-3.5 w-3.5 text-emerald-500" fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24">
						<path stroke-linecap="round" stroke-linejoin="round" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
						<path stroke-linecap="round" stroke-linejoin="round" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
					</svg>
					{location}
				</div>
				<h2 class="text-xl sm:text-2xl font-black tracking-tight text-zinc-900 dark:text-white leading-tight">
					{theme.tagline}
				</h2>
			</div>

			<!-- Dynamic description info -->
			<div class="grid grid-cols-2 gap-3 text-xs">
				<div class="p-3 rounded-xl bg-white/40 dark:bg-zinc-800/10 border border-zinc-200/50 dark:border-zinc-800/40">
					<p class="text-zinc-400 dark:text-zinc-500 font-bold uppercase text-[9px] tracking-wide">Last Updated</p>
					<p class="font-extrabold text-zinc-800 dark:text-zinc-200 mt-0.5">{lastUpdated}</p>
				</div>
				<div class="p-3 rounded-xl bg-white/40 dark:bg-zinc-800/10 border border-zinc-200/50 dark:border-zinc-800/40">
					<p class="text-zinc-400 dark:text-zinc-500 font-bold uppercase text-[9px] tracking-wide">Primary Pollutant</p>
					<p class="font-extrabold text-zinc-800 dark:text-zinc-200 mt-0.5">PM2.5</p>
				</div>
			</div>

			<!-- Recommendation Badge -->
			<div class="p-3.5 rounded-xl border border-zinc-200/50 dark:border-zinc-800 bg-white/30 dark:bg-zinc-900/30 text-xs font-semibold text-zinc-600 dark:text-zinc-300 flex items-center gap-2.5 shadow-sm">
				<svg class="h-4.5 w-4.5 text-emerald-500 shrink-0" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
					<path stroke-linecap="round" stroke-linejoin="round" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" />
				</svg>
				<span>
					{#if aqi <= 50}
						Air quality is excellent. Indoor ventilation is highly recommended.
					{:else if aqi <= 100}
						Air quality is acceptable. Ventilate rooms during off-peak traffic hours.
					{:else}
						Close windows to avoid dust build-up. Wear N95 respirator masks outdoors.
					{/if}
				</span>
			</div>
		</div>
	</div>

	<!-- Interactive Scale Legend -->
	<div class="relative z-10 flex items-center gap-1.5 w-full mt-4 pt-4 border-t border-zinc-200/50 dark:border-zinc-800/40 text-[9px] font-bold text-zinc-400 select-none overflow-x-auto pb-1 scrollbar-none">
		<span class="shrink-0 uppercase tracking-wide mr-1 dark:text-zinc-500">AQI Scale:</span>
		<span class="flex items-center gap-1 px-2 py-0.5 rounded transition-all duration-300 {aqi <= 50 ? 'bg-emerald-500 text-white shadow-md scale-105' : 'bg-emerald-500/10 text-emerald-600 dark:text-emerald-400/80'}">0-50 Good</span>
		<span class="flex items-center gap-1 px-2 py-0.5 rounded transition-all duration-300 {aqi > 50 && aqi <= 100 ? 'bg-amber-500 text-white shadow-md scale-105' : 'bg-amber-500/10 text-amber-600 dark:text-amber-400/80'}">51-100 Mod</span>
		<span class="flex items-center gap-1 px-2 py-0.5 rounded transition-all duration-300 {aqi > 100 && aqi <= 150 ? 'bg-orange-500 text-white shadow-md scale-105' : 'bg-orange-500/10 text-orange-600 dark:text-orange-400/80'}">101-150 Sens</span>
		<span class="flex items-center gap-1 px-2 py-0.5 rounded transition-all duration-300 {aqi > 150 && aqi <= 200 ? 'bg-red-500 text-white shadow-md scale-105' : 'bg-red-500/10 text-red-600 dark:text-red-400/80'}">151-200 Unh</span>
		<span class="flex items-center gap-1 px-2 py-0.5 rounded transition-all duration-300 {aqi > 200 && aqi <= 300 ? 'bg-purple-500 text-white shadow-md scale-105' : 'bg-purple-500/10 text-purple-600 dark:text-purple-400/80'}">201-300 Very Unh</span>
		<span class="flex items-center gap-1 px-2 py-0.5 rounded transition-all duration-300 {aqi > 300 ? 'bg-rose-900 text-white shadow-md scale-105' : 'bg-rose-950/20 text-rose-800 dark:text-rose-400'}">301+ Haz</span>
	</div>
</div>
