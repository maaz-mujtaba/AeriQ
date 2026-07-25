<script>
	let {
		temperature = 32,
		feelsLike = 35,
		condition = 'Sunny',
		weatherIcon = 'sun',
		humidity = 60,
		windSpeed = 10,
		pressure = 1010,
		visibility = 10,
		uvIndex = 'Moderate'
	} = $props();
</script>

<div class="relative overflow-hidden bg-white/40 dark:bg-zinc-900/40 border border-white/20 dark:border-zinc-800/80 backdrop-blur-xl rounded-2xl p-6 shadow-md transition-all duration-300 flex flex-col justify-between h-full min-h-[300px]">
	<!-- Ambient decoration light glow -->
	<div class="absolute -top-16 -right-16 h-36 w-36 rounded-full bg-sky-500/10 dark:bg-sky-500/5 blur-3xl opacity-40"></div>

	<!-- Top: Weather Summary & Large Icon -->
	<div class="flex items-center justify-between pb-4 border-b border-zinc-200/40 dark:border-zinc-800/40">
		<div class="space-y-1">
			<span class="text-xs font-bold text-zinc-400 dark:text-zinc-500 uppercase tracking-wider">Meteorology</span>
			<h3 class="text-3xl sm:text-4xl font-black text-zinc-900 dark:text-white tracking-tight flex items-start">
				{temperature}<span class="text-lg font-extrabold text-emerald-500 mt-1">°C</span>
			</h3>
			<p class="text-xs font-bold text-zinc-700 dark:text-zinc-300 flex items-center gap-1.5">
				<span class="h-2 w-2 rounded-full bg-emerald-500"></span>
				{condition}
			</p>
			<p class="text-[10px] text-zinc-450 dark:text-zinc-500 font-bold uppercase tracking-wide">
				Feels Like {feelsLike}°C
			</p>
		</div>

		<!-- Large Weather Icon -->
		<div class="h-14 w-14 text-amber-500 dark:text-amber-400 shrink-0 select-none">
			{#if weatherIcon === 'sun'}
				<svg class="h-full w-full animate-spin" style="animation-duration: 15s;" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
					<path stroke-linecap="round" stroke-linejoin="round" d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364-6.364l-.707.707M6.343 17.657l-.707.707m0-12.728l.707.707m12.728 12.728l.707-.707M12 8a4 4 0 100 8 4 4 0 000-8z" />
				</svg>
			{:else if weatherIcon === 'cloud'}
				<svg class="h-full w-full text-zinc-450 dark:text-zinc-550 animate-pulse" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
					<path stroke-linecap="round" stroke-linejoin="round" d="M3 15a4 4 0 004 4h9a5 5 0 10-.1-9.999 5.002 5.002 0 10-9.78 2.096A4.001 4.001 0 003 15z" />
				</svg>
			{:else if weatherIcon === 'rain'}
				<svg class="h-full w-full text-blue-550" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
					<path stroke-linecap="round" stroke-linejoin="round" d="M3 15a4 4 0 004 4h9a5 5 0 10-.1-9.999 5.002 5.002 0 10-9.78 2.096A4.001 4.001 0 003 15z" />
					<path stroke-linecap="round" stroke-linejoin="round" d="M12 12v6M8 14v4M16 14v4" />
				</svg>
			{:else if weatherIcon === 'haze'}
				<svg class="h-full w-full text-zinc-400 dark:text-zinc-550 animate-pulse" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
					<path stroke-linecap="round" stroke-linejoin="round" d="M4 6h16M4 10h16M4 14h16M4 18h16" />
				</svg>
			{:else}
				<svg class="h-full w-full text-teal-500" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
					<path stroke-linecap="round" stroke-linejoin="round" d="M9.59 4.59A2 2 0 1111 8H2m10.59 11.41A2 2 0 1014 16H2m15.73-8.27A2.5 2.5 0 1119.5 12H2" />
				</svg>
			{/if}
		</div>
	</div>

	<!-- Weather Grid Details -->
	<div class="grid grid-cols-2 xs:grid-cols-3 gap-2.5 mt-4">
		<!-- Humidity -->
		<div class="p-2.5 bg-white/40 dark:bg-zinc-800/10 border border-zinc-200/40 dark:border-zinc-800/40 rounded-xl">
			<p class="text-zinc-400 dark:text-zinc-500 font-bold uppercase text-[8px] tracking-wider leading-none">Humidity</p>
			<p class="text-xs font-black text-zinc-800 dark:text-zinc-200 mt-1">{humidity}%</p>
		</div>

		<!-- Wind -->
		<div class="p-2.5 bg-white/40 dark:bg-zinc-800/10 border border-zinc-200/40 dark:border-zinc-800/40 rounded-xl">
			<p class="text-zinc-400 dark:text-zinc-500 font-bold uppercase text-[8px] tracking-wider leading-none">Wind</p>
			<p class="text-xs font-black text-zinc-800 dark:text-zinc-200 mt-1 truncate">{windSpeed} km/h</p>
		</div>

		<!-- Pressure -->
		<div class="p-2.5 bg-white/40 dark:bg-zinc-800/10 border border-zinc-200/40 dark:border-zinc-800/40 rounded-xl">
			<p class="text-zinc-400 dark:text-zinc-500 font-bold uppercase text-[8px] tracking-wider leading-none">Pressure</p>
			<p class="text-xs font-black text-zinc-800 dark:text-zinc-200 mt-1 truncate">{pressure} hPa</p>
		</div>

		<!-- Visibility -->
		<div class="p-2.5 bg-white/40 dark:bg-zinc-800/10 border border-zinc-200/40 dark:border-zinc-800/40 rounded-xl">
			<p class="text-zinc-400 dark:text-zinc-500 font-bold uppercase text-[8px] tracking-wider leading-none">Visibility</p>
			<p class="text-xs font-black text-zinc-800 dark:text-zinc-200 mt-1 truncate">{visibility} km</p>
		</div>

		<!-- UV Index -->
		<div class="p-2.5 bg-white/40 dark:bg-zinc-800/10 border border-zinc-200/40 dark:border-zinc-800/40 rounded-xl col-span-2 xs:col-span-1">
			<p class="text-zinc-400 dark:text-zinc-500 font-bold uppercase text-[8px] tracking-wider leading-none">UV Index</p>
			<p class="text-xs font-black text-zinc-800 dark:text-zinc-200 mt-1 truncate">{uvIndex}</p>
		</div>
	</div>
</div>
