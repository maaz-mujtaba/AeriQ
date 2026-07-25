<script lang="ts">
	interface Props {
		forecastItems?: any[];
		selectedIndex?: number;
		onselect?: (idx: number) => void;
	}

	let {
		forecastItems = [],
		selectedIndex = 0,
		onselect = (idx: number) => {}
	}: Props = $props();

	// Help mapper for health advice mapping
	function getHealthMessage(aqiVal: number): string {
		if (aqiVal <= 50) return 'Perfect for outdoor activity.';
		if (aqiVal <= 100) return 'Sensitive groups use caution.';
		if (aqiVal <= 150) return 'Reduce outdoor exercise.';
		if (aqiVal <= 200) return 'Wear mask outside.';
		return 'Avoid outdoor actions entirely.';
	}

	// Category styling helper
	function getCategoryBadgeClass(category: string): string {
		const cat = category.toLowerCase();
		if (cat === 'good') {
			return 'bg-emerald-500/10 text-emerald-705 dark:text-emerald-450 border border-emerald-500/10';
		} else if (cat === 'moderate' || cat === 'satisfactory') {
			return 'bg-amber-500/10 text-amber-755 dark:text-amber-450 border border-amber-500/10';
		} else if (cat === 'poor') {
			return 'bg-orange-500/10 text-orange-705 dark:text-orange-400 border border-orange-500/10';
		} else {
			return 'bg-red-500/10 text-red-705 dark:text-red-400 border border-red-500/10';
		}
	}
</script>

<div class="relative overflow-hidden bg-white/40 dark:bg-zinc-900/40 border border-white/20 dark:border-zinc-800/80 backdrop-blur-xl rounded-2xl p-6 shadow-md transition-all duration-300 w-full select-none animate-slide-up">
	
	<!-- Header -->
	<div class="space-y-1 mb-4">
		<span class="text-xs font-bold text-zinc-400 dark:text-zinc-500 uppercase tracking-wider">Metrics Breakdown</span>
		<h3 class="text-lg font-black text-zinc-900 dark:text-white">Detailed Forecast Table</h3>
	</div>

	<!-- Scrollable Table Container -->
	<div class="overflow-x-auto w-full">
		<table class="w-full text-left border-collapse text-xs font-semibold text-zinc-650 dark:text-zinc-400 min-w-[900px]">
			<thead>
				<tr class="border-b border-zinc-200/50 dark:border-zinc-800/80 text-zinc-400 dark:text-zinc-500 uppercase tracking-wider text-[9px] font-extrabold select-none">
					<th class="py-3 px-4">Day</th>
					<th class="py-3 px-4">Weather</th>
					<th class="py-3 px-4 text-center">High</th>
					<th class="py-3 px-4 text-center">Low</th>
					<th class="py-3 px-4 text-center">AQI</th>
					<th class="py-3 px-4">Category</th>
					<th class="py-3 px-4 text-center">Humidity</th>
					<th class="py-3 px-4 text-center">Wind</th>
					<th class="py-3 px-4 text-center">Pressure</th>
					<th class="py-3 px-4 text-center">Rain</th>
					<th class="py-3 px-4 text-center">UV</th>
					<th class="py-3 px-4">Health Advice</th>
				</tr>
			</thead>
			<tbody class="divide-y divide-zinc-200/20 dark:divide-zinc-800/40">
				{#each forecastItems as item, idx}
					<tr
						onclick={() => onselect(idx)}
						class="hover:bg-zinc-50/50 dark:hover:bg-zinc-850/20 transition-all duration-150 cursor-pointer
							{selectedIndex === idx
								? 'bg-emerald-500/5 dark:bg-emerald-500/5 font-extrabold text-zinc-900 dark:text-white border-l-2 border-emerald-500'
								: 'border-l-2 border-transparent text-zinc-700 dark:text-zinc-350'}"
					>
						<!-- Day & Date -->
						<td class="py-3.5 px-4 font-black">
							<span class="block text-sm">{item.day}</span>
							<span class="text-[9px] text-zinc-450 dark:text-zinc-550 font-extrabold uppercase tracking-wide">{item.date}</span>
						</td>

						<!-- Weather condition with mini icon -->
						<td class="py-3.5 px-4 font-bold flex items-center gap-1.5 mt-1">
							{#if item.weather_icon === 'sun'}
								<span class="text-amber-500 text-sm">☀</span>
							{:else if item.weather_icon === 'cloud'}
								<span class="text-zinc-400 text-sm">☁</span>
							{:else if item.weather_icon === 'rain'}
								<span class="text-blue-500 text-sm">🌧</span>
							{:else if item.weather_icon === 'haze'}
								<span class="text-zinc-400 text-sm">🌫</span>
							{:else}
								<span class="text-teal-500 text-sm">💨</span>
							{/if}
							<span>{item.weather_desc}</span>
						</td>

						<!-- High Temp -->
						<td class="py-3.5 px-4 text-center font-bold text-zinc-850 dark:text-zinc-200">
							{item.temp_high || Math.round(item.temperature + 3)}°C
						</td>

						<!-- Low Temp -->
						<td class="py-3.5 px-4 text-center font-bold text-zinc-450 dark:text-zinc-500">
							{item.temp_low || Math.round(item.temperature - 4)}°C
						</td>

						<!-- AQI -->
						<td class="py-3.5 px-4 text-center text-sm font-black" style="color: {item.aqi_color};">
							{item.aqi}
						</td>

						<!-- Category Badge -->
						<td class="py-3.5 px-4">
							<span class="inline-block text-[8px] font-black uppercase px-2 py-0.5 rounded border {getCategoryBadgeClass(item.aqi_category)}">
								{item.aqi_category}
							</span>
						</td>

						<!-- Humidity -->
						<td class="py-3.5 px-4 text-center">
							{item.humidity}%
						</td>

						<!-- Wind -->
						<td class="py-3.5 px-4 text-center">
							{item.wind_speed} <span class="text-[9px] text-zinc-450 font-semibold">km/h</span>
						</td>

						<!-- Pressure -->
						<td class="py-3.5 px-4 text-center truncate">
							{item.pressure} <span class="text-[9px] text-zinc-450 font-semibold">hPa</span>
						</td>

						<!-- Rain Chance -->
						<td class="py-3.5 px-4 text-center text-blue-500 font-bold">
							{item.rain_chance !== undefined ? item.rain_chance : Math.round(item.chance_of_improvement / 2)}%
						</td>

						<!-- UV -->
						<td class="py-3.5 px-4 text-center truncate">
							{item.uv_index ? item.uv_index.split(' ')[0] : '3'}
						</td>

						<!-- Health Advice -->
						<td class="py-3.5 px-4 italic font-medium text-zinc-500 dark:text-zinc-450 leading-relaxed max-w-[200px] truncate" title={item.health_advice || getHealthMessage(item.aqi)}>
							{item.health_advice || getHealthMessage(item.aqi)}
						</td>
					</tr>
				{/each}
			</tbody>
		</table>
	</div>
</div>
