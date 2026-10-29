<script lang="ts">
	import { forecastData, weatherHourly } from '$lib/stores/aqiStore.js';
	import { getCurrentAQI, getModelStatus, loadAQIForecast, loadWeatherHourly } from '$lib/api.js';

	// Component imports
	import ForecastChart from '$lib/components/ForecastChart.svelte';
	import ForecastGrid from '$lib/components/ForecastGrid.svelte';
	import WeatherSummary from '$lib/components/WeatherSummary.svelte';
	import RecommendationCard from '$lib/components/RecommendationCard.svelte';
	import ForecastTable from '$lib/components/ForecastTable.svelte';
	import AQIGauge from '$lib/components/AQIGauge.svelte';

	// Coordinate mapping matching Dashboard city profiles
	const cityProfiles = {
		delhi: { name: 'New Delhi, India', lat: 28.6139, lon: 77.209 },
		newyork: { name: 'New York, USA', lat: 40.7128, lon: -74.006 },
		london: { name: 'London, UK', lat: 51.5074, lon: -0.1278 },
		tokyo: { name: 'Tokyo, Japan', lat: 35.6762, lon: 139.6503 },
		sydney: { name: 'Sydney, Australia', lat: -33.8688, lon: 151.2093 }
	};

	// Tab configuration for weather trends
	const weatherTabConfigs = {
		temperature: { label: 'Temperature', field: 'temperature', suffix: '°C', color: '#06b6d4', gradient: 'temp-grad' },
		humidity: { label: 'Humidity', field: 'humidity', suffix: '%', color: '#3b82f6', gradient: 'hum-grad' },
		rainfall: { label: 'Rainfall', field: 'rain_chance', suffix: '%', color: '#6366f1', gradient: 'rain-grad' },
		wind_speed: { label: 'Wind Speed', field: 'wind_speed', suffix: ' km/h', color: '#8b5cf6', gradient: 'wind-grad' },
		pressure: { label: 'Pressure', field: 'pressure', suffix: ' hPa', color: '#ec4899', gradient: 'press-grad' }
	};

	// Page local states
	let activeCityKey: keyof typeof cityProfiles = $state('delhi');
	let selectedIndex = $state(0); // Selected forecast day (Tomorrow, Sunday, etc.)
	let activeWeatherTab: keyof typeof weatherTabConfigs = $state('temperature'); // Weather trends active tab
	let isRefreshing = $state(false);
	let forecastLoading = $state(true);
	let forecastError = $state('');
	let modelError = $state('');
	let modelStatus: { is_loaded: boolean; model_type?: string; n_estimators?: number; feature_names?: string[]; has_scaler?: boolean } | null = $state(null);
	let forecastMeta: { prediction_method?: string; model_loaded?: boolean; source?: string } | null = $state(null);
	let lastSyncedAt = $state('');
	let currentReading: { aqi?: number; aqi_category?: string; pm25?: number; timestamp?: string; prediction_source?: string } | null = $state(null);
	let currentReadingError = $state('');

	const weatherTabKeys = Object.keys(weatherTabConfigs) as Array<keyof typeof weatherTabConfigs>;

	let activeProfile = $derived(cityProfiles[activeCityKey]);
	let activeForecastItems = $derived($forecastData || []);

	// The API response is the source of displayed forecast values; no synthetic AQI defaults.
	let selectedDayData = $derived(activeForecastItems[selectedIndex] || null);

	let pollutantsList = $derived.by(() => {
		const input = selectedDayData?.pollutants || {};
		return [
			{ name: 'PM2.5', value: input.pm25, limit: 30, unit: 'ug/m3' },
			{ name: 'PM10', value: input.pm10, limit: 60, unit: 'ug/m3' },
			{ name: 'NO2', value: input.no2, limit: 40, unit: 'ug/m3' },
			{ name: 'SO2', value: input.so2, limit: 40, unit: 'ug/m3' },
			{ name: 'CO', value: input.co == null ? null : input.co / 1000, limit: 2.0, unit: 'mg/m3' },
			{ name: 'O3', value: input.o3, limit: 100, unit: 'ug/m3' }
		].map((item) => ({
			...item,
			status: item.value == null ? 'Unavailable' : item.value <= item.limit * 0.75 ? 'Good' : item.value <= item.limit ? 'Moderate' : 'High'
		}));
	});

	async function refreshForecast(latitude: number, longitude: number) {
		forecastLoading = true;
		forecastError = '';
		modelError = '';
		const [forecastResult, _weatherResult, modelResult, currentResult] = await Promise.allSettled([
			loadAQIForecast(latitude, longitude),
			loadWeatherHourly(latitude, longitude),
			getModelStatus(),
			getCurrentAQI(latitude, longitude)
		]);
		if (forecastResult.status === 'fulfilled') {
			forecastMeta = forecastResult.value;
			lastSyncedAt = new Date().toLocaleTimeString();
		} else {
			forecastMeta = null;
			forecastError = forecastResult.reason instanceof Error ? forecastResult.reason.message : 'Forecast data is unavailable.';
		}
		if (modelResult.status === 'fulfilled') modelStatus = modelResult.value;
		else modelError = modelResult.reason instanceof Error ? modelResult.reason.message : 'Model status is unavailable.';
		if (currentResult.status === 'fulfilled') { currentReading = currentResult.value; currentReadingError = ''; }
		else { currentReading = null; currentReadingError = currentResult.reason instanceof Error ? currentResult.reason.message : 'Current air quality is unavailable.'; }
		forecastLoading = false;
	}

	async function handleRefresh() {
		isRefreshing = true;
		try { await refreshForecast(activeProfile.lat, activeProfile.lon); }
		finally { isRefreshing = false; }
	}

	$effect(() => {
		void refreshForecast(activeProfile.lat, activeProfile.lon);
	});

	// Reset selected index when city key shifts
	$effect(() => {
		activeCityKey;
		selectedIndex = 0;
	});
</script>

<div class="space-y-8 select-none relative animate-fade-in">
	
	<!-- Glass Loading Spinner Overlay -->
	{#if isRefreshing || forecastLoading}
		<div class="fixed inset-0 bg-white/30 dark:bg-zinc-950/30 backdrop-blur-sm z-50 flex items-center justify-center transition-all duration-300">
			<div class="flex flex-col items-center gap-3 p-6 bg-white dark:bg-zinc-900 border border-zinc-100 dark:border-zinc-800 rounded-2xl shadow-xl animate-scale-up">
				<svg class="h-8 w-8 text-emerald-500 animate-spin" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="3">
					<circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
					<path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
				</svg>
				<span class="text-xs font-bold text-zinc-600 dark:text-zinc-300">Syncing Projections...</span>
			</div>
		</div>
	{/if}

	<!-- ==================== HEADER SECTION ==================== -->
	<div class="flex flex-col md:flex-row md:items-center justify-between gap-4 border-b border-zinc-200/40 dark:border-zinc-800 pb-5 z-10 relative">
		<div class="space-y-1">
			<div class="flex items-center gap-2 text-xs font-bold text-zinc-400 dark:text-zinc-500 uppercase tracking-wider">
				<span>Environmental Intelligence</span>
				<span>/</span>
				<span class="text-emerald-500 dark:text-emerald-400">Forecast</span>
			</div>
			<h1 class="text-2xl sm:text-3xl font-black tracking-tight text-zinc-900 dark:text-white">
				Forecast
			</h1>
			<p class="text-xs sm:text-sm font-semibold text-zinc-500 dark:text-zinc-400">
				View predicted air quality and weather forecasts for the upcoming days in <span class="font-black text-zinc-850 dark:text-zinc-200">{activeProfile.name}</span>.
			</p>
		</div>

		<!-- Location Selector and Refresh controls -->
		<div class="flex items-center gap-2 flex-wrap">
			<div class="flex items-center gap-1.5 p-1 bg-zinc-200/50 dark:bg-zinc-900 rounded-xl select-none border border-zinc-200/50 dark:border-zinc-800/50 shadow-sm">
				<button
					onclick={() => activeCityKey = 'delhi'}
					class="px-2.5 py-1.5 text-xs font-bold rounded-lg transition-all focus:outline-none {activeCityKey === 'delhi' ? 'bg-white dark:bg-zinc-800 text-emerald-600 dark:text-emerald-450 shadow-sm' : 'text-zinc-550 hover:text-zinc-800 dark:hover:text-zinc-200'}"
				>
					Delhi
				</button>
				<button
					onclick={() => activeCityKey = 'newyork'}
					class="px-2.5 py-1.5 text-xs font-bold rounded-lg transition-all focus:outline-none {activeCityKey === 'newyork' ? 'bg-white dark:bg-zinc-800 text-emerald-600 dark:text-emerald-450 shadow-sm' : 'text-zinc-550 hover:text-zinc-800 dark:hover:text-zinc-200'}"
				>
					NY
				</button>
				<button
					onclick={() => activeCityKey = 'london'}
					class="px-2.5 py-1.5 text-xs font-bold rounded-lg transition-all focus:outline-none {activeCityKey === 'london' ? 'bg-white dark:bg-zinc-800 text-emerald-600 dark:text-emerald-450 shadow-sm' : 'text-zinc-550 hover:text-zinc-800 dark:hover:text-zinc-200'}"
				>
					London
				</button>
				<button
					onclick={() => activeCityKey = 'tokyo'}
					class="px-2.5 py-1.5 text-xs font-bold rounded-lg transition-all focus:outline-none {activeCityKey === 'tokyo' ? 'bg-white dark:bg-zinc-800 text-emerald-600 dark:text-emerald-450 shadow-sm' : 'text-zinc-550 hover:text-zinc-800 dark:hover:text-zinc-200'}"
				>
					Tokyo
				</button>
				<button
					onclick={() => activeCityKey = 'sydney'}
					class="px-2.5 py-1.5 text-xs font-bold rounded-lg transition-all focus:outline-none {activeCityKey === 'sydney' ? 'bg-white dark:bg-zinc-800 text-emerald-600 dark:text-emerald-450 shadow-sm' : 'text-zinc-550 hover:text-zinc-800 dark:hover:text-zinc-200'}"
				>
					Sydney
				</button>
			</div>

			<button
				onclick={handleRefresh}
				class="px-3 py-2.5 bg-white/40 dark:bg-zinc-900/45 border border-zinc-200 dark:border-zinc-800 rounded-xl text-xs font-bold text-zinc-700 dark:text-zinc-300 hover:text-zinc-950 dark:hover:text-zinc-150 hover:bg-white dark:hover:bg-zinc-800 shadow-sm focus:outline-none flex items-center gap-1.5 active:scale-95 transition-all"
			>
				<svg class="h-3.5 w-3.5 text-zinc-400" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
					<path stroke-linecap="round" stroke-linejoin="round" d="M4 4v5h.582m15.356 2A8.001 8.001 0 1121.21 7.89H18" />
				</svg>
				Refresh
			</button>
		</div>
	</div>

	<div class="grid gap-4 sm:grid-cols-2">
		<section class="rounded-2xl border border-zinc-200 bg-white/70 p-4 dark:border-zinc-800 dark:bg-zinc-900/70" aria-live="polite">
			<div class="flex items-center justify-between gap-3">
				<div>
					<p class="text-[10px] font-bold uppercase tracking-widest text-zinc-400">Prediction Engine</p>
					<h2 class="mt-1 text-sm font-bold text-zinc-900 dark:text-white">
						{modelStatus?.is_loaded ? (modelStatus.model_type || 'Machine learning model') : modelStatus ? 'CPCB fallback active' : 'Checking model status...'}
					</h2>
				</div>
				<span class="rounded-full px-2.5 py-1 text-[10px] font-bold {modelStatus?.is_loaded ? 'bg-emerald-100 text-emerald-700 dark:bg-emerald-950/40 dark:text-emerald-300' : modelStatus ? 'bg-amber-100 text-amber-700 dark:bg-amber-950/40 dark:text-amber-300' : 'bg-zinc-100 text-zinc-600 dark:bg-zinc-800 dark:text-zinc-300'}">
					{modelStatus?.is_loaded ? 'MODEL LOADED' : modelStatus ? 'FALLBACK MODE' : 'CHECKING'}
				</span>
			</div>
			<p class="mt-2 text-xs text-zinc-500 dark:text-zinc-400">
				{#if modelStatus?.is_loaded}
					{modelStatus.n_estimators ? `${modelStatus.n_estimators} decision trees` : 'Random forest'} · {modelStatus.feature_names?.length || 0} input features · {modelStatus.has_scaler ? 'scaled inputs' : 'unscaled inputs'}
				{:else if modelStatus}
					The trained model is unavailable; AQI uses the CPCB PM2.5 formula.
				{:else}
					{modelError || 'Connecting to the model service.'}
				{/if}
			</p>
		</section>
		<section class="rounded-2xl border border-zinc-200 bg-white/70 p-4 dark:border-zinc-800 dark:bg-zinc-900/70">
			<p class="text-[10px] font-bold uppercase tracking-widest text-zinc-400">Forecast computation</p>
			<p class="mt-1 text-sm font-bold text-zinc-900 dark:text-white">
				{selectedDayData?.prediction_source === 'ml_model' ? 'ML prediction' : selectedDayData?.prediction_source === 'cpcb_fallback' ? 'CPCB fallback prediction' : forecastMeta?.prediction_method || 'Awaiting forecast'}
			</p>
			<p class="mt-2 text-xs text-zinc-500 dark:text-zinc-400">The model uses hourly pollutant history and weather features. Forecast AQI is averaged from hourly predictions; current AQI is shown separately.</p>
		</section>
	</div>
	{#if forecastError}
		<div role="alert" class="rounded-xl border border-amber-300 bg-amber-50 px-4 py-3 text-sm text-amber-800 dark:border-amber-900 dark:bg-amber-950/30 dark:text-amber-200">Forecast unavailable: {forecastError}</div>
	{/if}

	<!-- ==================== SECTION 1: Today Overview ==================== -->
	{#if selectedDayData}
	<div class="grid grid-cols-1 lg:grid-cols-3 gap-6 z-10 relative animate-slide-up">
		
		<!-- CARD 1: Today's AQI -->
		<div class="relative overflow-hidden bg-white/40 dark:bg-zinc-900/40 border border-white/20 dark:border-zinc-800/80 backdrop-blur-xl rounded-2xl p-6 shadow-md transition-all duration-300 flex items-center justify-between min-h-[300px] hover:border-emerald-500/20">
			<!-- Background breeze SVG -->
			<div class="absolute inset-0 pointer-events-none z-0 opacity-10 text-emerald-500">
				<svg class="h-full w-full" viewBox="0 0 450 200" fill="none" stroke="currentColor" stroke-width="1.5">
					<path d="M-20 80 Q60 50, 180 80 T380 60 T500 90" stroke-linecap="round" />
				</svg>
			</div>

			<div class="space-y-4 z-10 w-full flex justify-between gap-3">
				<div class="flex flex-col justify-between h-full space-y-4">
					<div class="space-y-1">
						<span class="text-xs font-bold text-zinc-400 dark:text-zinc-500 uppercase tracking-wider">Air Index</span>
						<h3 class="text-xl font-black text-zinc-900 dark:text-white">Current AQI estimate</h3>
					</div>

					<div class="space-y-1.5">
						<div class="flex items-baseline gap-2">
							<span class="text-4xl font-black text-zinc-900 dark:text-white tracking-tight leading-none">
								{currentReading?.aqi ?? '—'}
							</span>
							<span class="text-[10px] text-zinc-400 font-bold uppercase tracking-wider">AQI</span>
							<span class="text-xs font-black text-emerald-500 flex items-center">
								{#if selectedDayData.trend_direction === 'up'}
									↑ Stable
								{:else if selectedDayData.trend_direction === 'down'}
									↓ Improving
								{:else}
									→ Consistent
								{/if}
							</span>
						</div>
					</div>

					<div class="grid grid-cols-2 gap-2 text-[10px] font-bold text-zinc-400">
						<div>
							<p class="uppercase text-[8px] tracking-wider text-zinc-400 dark:text-zinc-550">Primary</p>
							<p class="text-zinc-800 dark:text-zinc-200 font-extrabold mt-0.5">PM2.5</p>
						</div>
						<div>
							<p class="uppercase text-[8px] tracking-wider text-zinc-400 dark:text-zinc-550">PM2.5</p>
							<p class="text-zinc-850 dark:text-zinc-200 mt-0.5 truncate">{currentReading?.pm25 == null ? 'Unavailable' : `${currentReading.pm25} µg/m³`}</p>
						</div>
					</div>
				</div>

				<!-- Small Gauge on right -->
				<div class="shrink-0 flex items-center justify-center">
					<AQIGauge aqi={currentReading?.aqi ?? 0} />
				</div>
			</div>
		</div>

		<!-- CARD 2: Today's Weather -->
		<div>
			<WeatherSummary
				temperature={selectedDayData.temperature}
				feelsLike={selectedDayData.temp_high - 1}
				condition={selectedDayData.weather_desc}
				weatherIcon={selectedDayData.weather_icon}
				humidity={selectedDayData.humidity}
				windSpeed={selectedDayData.wind_speed}
				pressure={selectedDayData.pressure}
				visibility={selectedDayData.visibility}
				uvIndex={selectedDayData.uv_index?.split?.(' ')[0] || 'N/A'}
			/>
		</div>

		<!-- CARD 3: Health Advisory -->
		<div>
			<RecommendationCard
				aqi={currentReading?.aqi ?? selectedDayData.aqi}
				category={currentReading?.aqi_category ?? selectedDayData.aqi_category}
			/>
		</div>
	</div>
	{:else if !forecastLoading}
		<div class="rounded-2xl border border-zinc-200 bg-white/60 p-8 text-center dark:border-zinc-800 dark:bg-zinc-900/60">
			<h2 class="font-bold text-zinc-900 dark:text-white">No AQI prediction to display</h2>
			<p class="mt-2 text-sm text-zinc-500 dark:text-zinc-400">The forecast service did not return usable pollutant data for {activeProfile.name}. Refresh to try again.</p>
		</div>
	{/if}

	<!-- ==================== SECTION 2: Hourly Forecast ==================== -->
	<div class="space-y-3 z-10 relative">
		<h3 class="text-xs font-bold text-zinc-400 dark:text-zinc-500 uppercase tracking-wider">
			Hourly Forecast (Next 24 Hours)
		</h3>
		
		<div class="flex overflow-x-auto gap-4 pb-3 scrollbar-thin scrollbar-thumb-zinc-200 dark:scrollbar-thumb-zinc-800 scrollbar-track-transparent">
			{#if $weatherHourly.length === 0}
				<div class="w-full rounded-2xl border border-zinc-200/40 p-5 text-sm text-zinc-500 dark:border-zinc-800/40">{forecastLoading ? 'Loading hourly weather...' : 'Hourly weather data is unavailable.'}</div>
			{:else}
				{#each $weatherHourly as hour}
					<div class="p-4 bg-white/40 dark:bg-zinc-900/40 border border-white/20 dark:border-zinc-800/80 backdrop-blur-xl rounded-2xl flex flex-col items-center justify-between min-w-[105px] text-center shadow-sm hover:shadow hover:bg-white dark:hover:bg-zinc-900 transition-all duration-300">
						<!-- Time -->
						<span class="text-xs font-black text-zinc-900 dark:text-white leading-none">{hour.time}</span>
						
						<!-- Weather Icon -->
						<div class="h-6 w-6 text-zinc-400 dark:text-zinc-500 my-2">
							{#if hour.weather_icon === 'sun'}
								<span class="text-amber-500 text-base leading-none">☀</span>
							{:else if hour.weather_icon === 'cloud'}
								<span class="text-zinc-400 text-base leading-none">☁</span>
							{:else if hour.weather_icon === 'rain'}
								<span class="text-blue-500 text-base leading-none">🌧</span>
							{:else if hour.weather_icon === 'haze'}
								<span class="text-zinc-400 text-base leading-none">🌫</span>
							{:else}
								<span class="text-teal-500 text-base leading-none">💨</span>
							{/if}
						</div>

						<!-- Temperature -->
						<span class="text-sm font-black text-zinc-800 dark:text-zinc-200 leading-none">{hour.temperature}°</span>

						<!-- AQI -->
						<span class="text-[8px] font-black px-2 py-0.5 rounded bg-zinc-100 dark:bg-zinc-850 text-zinc-650 dark:text-zinc-350 mt-1.5 leading-none">
							{hour.aqi == null ? 'AQI unavailable' : `AQI ${hour.aqi}`}
						</span>

						<!-- Stats -->
						<div class="text-[8px] font-extrabold text-zinc-400 mt-2.5 space-y-0.5 leading-none select-none">
							<p>H: {hour.humidity}%</p>
							<p>W: {hour.wind_speed} km/h</p>
							<p class="text-blue-500">R: {hour.rain_chance}%</p>
						</div>
					</div>
				{/each}
			{/if}
		</div>
	</div>

	<!-- ==================== SECTION 3: Multi-Day Forecast Grid ==================== -->
	<div class="space-y-3 z-10 relative">
		<h3 class="text-xs font-bold text-zinc-400 dark:text-zinc-500 uppercase tracking-wider">
			3-Day Outlook Grid
		</h3>
		<ForecastGrid
			forecastItems={activeForecastItems}
			selectedIndex={selectedIndex}
			onselect={(idx: number) => selectedIndex = idx}
		/>
	</div>

	<!-- ==================== SECTION 4 & 5: Trend Charts side-by-side ==================== -->
	<div class="grid grid-cols-1 lg:grid-cols-2 gap-6 z-10 relative items-stretch">
		
		<!-- Section 4: AQI Trend Chart -->
		<div>
			<ForecastChart
				items={activeForecastItems}
				field="aqi"
				title="AQI Forecast Trend"
				description="Predicted AQI over the next several days."
				suffix=" AQI"
				lineColor="#10b981"
				areaGradientId="aqi-trend-gradient"
				selectedIndex={selectedIndex}
				onselect={(idx: number) => selectedIndex = idx}
			/>
		</div>

		<!-- Section 5: Weather Trends Chart with tabs switcher -->
		<div class="flex flex-col justify-between bg-white/40 dark:bg-zinc-900/40 border border-white/20 dark:border-zinc-800/80 backdrop-blur-xl rounded-2xl p-6 shadow-md transition-all duration-300 h-[360px] w-full">
			<div class="flex flex-col sm:flex-row sm:items-center justify-between gap-3 mb-2 z-10 w-full">
				<div class="space-y-1">
					<span class="text-xs font-bold text-zinc-400 dark:text-zinc-500 uppercase tracking-wider">Atmospheric Trends</span>
					<h3 class="text-lg font-black text-zinc-900 dark:text-white">Weather Trends</h3>
				</div>
				
				<!-- Tabs Selector -->
				<div class="flex items-center gap-1 p-0.5 bg-zinc-150 dark:bg-zinc-800 rounded-lg select-none border border-zinc-200/50 dark:border-zinc-700/50 max-w-fit flex-wrap">
					{#each weatherTabKeys as tabKey}
						<button
							onclick={() => activeWeatherTab = tabKey}
							class="px-2 py-1 text-[9px] font-bold rounded transition-all focus:outline-none
								{activeWeatherTab === tabKey
									? 'bg-white dark:bg-zinc-900 text-emerald-600 dark:text-emerald-450 shadow-xs'
									: 'text-zinc-405 dark:text-zinc-500 hover:text-zinc-700 dark:hover:text-zinc-300'}"
						>
							{weatherTabConfigs[tabKey].label.split(' ')[0]}
						</button>
					{/each}
				</div>
			</div>

			<!-- Dynamic line chart instanced based on active tab -->
			<div class="flex-1 w-full relative min-h-0 select-none">
				<ForecastChart
					items={activeForecastItems}
					field={weatherTabConfigs[activeWeatherTab].field}
					title={weatherTabConfigs[activeWeatherTab].label + " Outlook"}
					description={"Projections for daily " + weatherTabConfigs[activeWeatherTab].label.toLowerCase() + "."}
					suffix={weatherTabConfigs[activeWeatherTab].suffix}
					lineColor={weatherTabConfigs[activeWeatherTab].color}
					areaGradientId={weatherTabConfigs[activeWeatherTab].gradient}
					selectedIndex={selectedIndex}
					onselect={(idx: number) => selectedIndex = idx}
				/>
			</div>
		</div>
	</div>

	<!-- ==================== SECTION 6: Air Quality Breakdown ==================== -->
	<div class="space-y-3 z-10 relative animate-slide-up">
		<h3 class="text-xs font-bold text-zinc-400 dark:text-zinc-500 uppercase tracking-wider">
			Air Quality Breakdown{selectedDayData ? ` (${selectedDayData.day} daily forecast inputs)` : ''}
		</h3>
		<div class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-4">
			{#each pollutantsList as poll}
				{@const pct = poll.value == null ? 0 : Math.min(100, Math.round((poll.value / poll.limit) * 100))}
				<div class="bg-white/40 dark:bg-zinc-900/40 border border-white/20 dark:border-zinc-800/80 backdrop-blur-xl rounded-2xl p-4.5 shadow-sm space-y-3 flex flex-col justify-between hover:shadow hover:bg-white dark:hover:bg-zinc-900 transition-all duration-300">
					<!-- Header: Name & Status -->
					<div class="flex items-center justify-between">
						<span class="text-xs font-bold text-zinc-850 dark:text-zinc-200">{poll.name}</span>
						<span class="text-[8px] font-black uppercase px-2 py-0.5 rounded {poll.status === 'Good' ? 'bg-emerald-500/10 text-emerald-700 dark:text-emerald-400 border border-emerald-500/10' : poll.status === 'Moderate' ? 'bg-amber-500/10 text-amber-700 dark:text-amber-400 border border-amber-500/10' : poll.status === 'Unavailable' ? 'bg-zinc-500/10 text-zinc-500' : 'bg-red-500/10 text-red-700 dark:text-red-400 border border-red-500/10'}">
							{poll.status}
						</span>
					</div>

					<!-- Value, limit and unit -->
					<div class="space-y-0.5">
						<p class="text-2xl font-black text-zinc-900 dark:text-white">
							{poll.value == null ? 'N/A' : poll.value.toFixed(1)}
							<span class="text-[10px] font-bold text-zinc-400 dark:text-zinc-500">{poll.unit}</span>
						</p>
						<p class="text-[8px] text-zinc-400 dark:text-zinc-550 font-bold uppercase tracking-wider">{poll.value == null ? 'No measurement returned' : `Reference: ${poll.limit} ${poll.unit}`}</p>
					</div>

					<!-- Progress Indicator -->
					<div class="w-full bg-zinc-200/50 dark:bg-zinc-800 h-1.5 rounded-full overflow-hidden leading-none">
						<div class="h-full rounded-full transition-all duration-500 {pct > 100 ? 'bg-red-500' : pct > 75 ? 'bg-amber-500' : 'bg-emerald-500'}" style="width: {pct}%"></div>
					</div>

					<!-- Mini Trend Sparkline -->
					<div class="flex items-center justify-between pt-1 border-t border-zinc-200/20 dark:border-zinc-800/20 text-[8px] font-bold text-zinc-400">
						<span>Mini Trend</span>
						<svg class="h-4.5 w-12 {pct > 75 ? 'text-amber-500' : 'text-emerald-500'}" viewBox="0 0 50 10">
							<path d="M0,5 Q12,{pct > 100 ? '9' : '2'} 25,{pct > 75 ? '8' : '3'} T50,{pct > 100 ? '1' : '6'}" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" />
						</svg>
					</div>
				</div>
			{/each}
		</div>
	</div>

	<!-- ==================== SECTION 8: Detailed Forecast Table ==================== -->
	<div class="z-10 relative">
		<ForecastTable
			forecastItems={activeForecastItems}
			selectedIndex={selectedIndex}
			onselect={(idx: number) => selectedIndex = idx}
		/>
	</div>

	<!-- ==================== SECTION 9: Map Preview ==================== -->
	<div class="bg-white/40 dark:bg-zinc-900/40 border border-white/20 dark:border-zinc-800/80 backdrop-blur-xl rounded-2xl p-6 shadow-md transition-all duration-300 grid grid-cols-1 md:grid-cols-3 gap-6 items-center z-10 relative">
		<div class="md:col-span-2 space-y-2 text-center md:text-left">
			<span class="text-xs font-bold text-zinc-400 dark:text-zinc-500 uppercase tracking-wider">Visual Radar</span>
			<h3 class="text-lg font-black text-zinc-900 dark:text-white">Regional Map Preview</h3>
			<p class="text-xs text-zinc-500 dark:text-zinc-400">
				Monitor microclimatic pollution hotspots and PM2.5 dispersion across neighborhood sensors in real time.
			</p>
			
			<div class="pt-2">
				<a
					href="/map"
					class="px-4 py-2.5 bg-emerald-500 hover:bg-emerald-600 active:scale-95 text-white text-xs font-bold rounded-xl shadow-md shadow-emerald-500/10 focus:outline-none transition-all inline-flex items-center gap-1.5"
				>
					Open Full AQI Map
					<svg class="h-3.5 w-3.5 text-emerald-100" fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24">
						<path stroke-linecap="round" stroke-linejoin="round" d="M9 5l7 7-7 7" />
					</svg>
				</a>
			</div>
		</div>

		<!-- Mini Map Placeholder with hotspots -->
		<div class="relative h-[150px] w-full bg-zinc-100 dark:bg-zinc-950 border border-zinc-200/50 dark:border-zinc-800 rounded-xl overflow-hidden shadow-inner flex items-center justify-center">
			<!-- Abstract Grid / Map Lines representation -->
			<div class="absolute inset-0 opacity-15 dark:opacity-10 pointer-events-none" style="background-image: radial-gradient(circle, currentColor 1px, transparent 1px); background-size: 10px 10px;"></div>
			
			<!-- Radar Scanning Sweep line -->
			<div class="absolute inset-0 bg-gradient-to-r from-emerald-500/0 via-emerald-500/10 to-emerald-500/0 h-full w-1/3 animate-pulse pointer-events-none" style="animation-duration: 4s;"></div>

			<!-- Hotspot Indicators -->
			<div class="absolute top-[25%] left-[30%] flex items-center justify-center">
				<span class="absolute h-4 w-4 rounded-full bg-emerald-500/40 animate-ping"></span>
				<span class="h-2 w-2 rounded-full bg-emerald-500"></span>
				<span class="absolute -top-3 text-[7px] font-bold text-zinc-400 dark:text-zinc-500 bg-white/80 dark:bg-zinc-900/80 px-1 rounded shadow-xs">Station 1</span>
			</div>
			
			<div class="absolute top-[60%] left-[70%] flex items-center justify-center">
				<span class="absolute h-4 w-4 rounded-full bg-red-500/40 animate-ping" style="animation-delay: 1s;"></span>
				<span class="h-2 w-2 rounded-full bg-red-500"></span>
				<span class="absolute -top-3 text-[7px] font-bold text-zinc-400 dark:text-zinc-500 bg-white/80 dark:bg-zinc-900/80 px-1 rounded shadow-xs">Smog Hotspot</span>
			</div>

			<div class="absolute top-[45%] left-[55%] flex items-center justify-center">
				<span class="absolute h-4 w-4 rounded-full bg-amber-500/40 animate-ping" style="animation-delay: 2s;"></span>
				<span class="h-2 w-2 rounded-full bg-amber-500"></span>
				<span class="absolute -top-3 text-[7px] font-bold text-zinc-400 dark:text-zinc-500 bg-white/80 dark:bg-zinc-900/80 px-1 rounded shadow-xs">Residential</span>
			</div>

			<span class="text-[9px] font-black text-zinc-350 dark:text-zinc-650 uppercase tracking-widest pointer-events-none">Radar Active</span>
		</div>
	</div>

	<!-- ==================== SECTION 10: Data Source Footer ==================== -->
	<div class="p-4 bg-zinc-100 dark:bg-zinc-900/45 border border-zinc-200/50 dark:border-zinc-800/80 rounded-xl flex flex-col sm:flex-row items-center justify-between gap-3 text-[10px] font-bold text-zinc-450 dark:text-zinc-500 z-10 relative">
		<div class="flex items-center gap-2">
			<svg class="h-4 w-4 text-emerald-500" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
				<path stroke-linecap="round" stroke-linejoin="round" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
			</svg>
			<span>Data: <a class="underline" href="https://open-meteo.com/" target="_blank" rel="noreferrer">Open-Meteo</a> and CAMS forecasts, processed with {forecastMeta?.prediction_method || 'the configured AQI prediction method'}.</span>
		</div>
		<span class="text-zinc-400">Last Synced: {lastSyncedAt || 'Not yet synced'}</span>
	</div>
</div>

<style>
	/* Animation declarations matching Dashboard layout exactly */
	.animate-fade-in {
		animation: fadeIn 0.6s cubic-bezier(0.4, 0, 0.2, 1) forwards;
	}

	.animate-scale-up {
		animation: scaleUp 0.4s cubic-bezier(0.34, 1.56, 0.64, 1) forwards;
	}

	.animate-slide-up {
		animation: slideUp 0.6s cubic-bezier(0.4, 0, 0.2, 1) forwards;
	}

	@keyframes fadeIn {
		from { opacity: 0; }
		to { opacity: 1; }
	}

	@keyframes scaleUp {
		from {
			transform: scale(0.95);
			opacity: 0;
		}
		to {
			transform: scale(1);
			opacity: 1;
		}
	}

	@keyframes slideUp {
		from {
			transform: translateY(16px);
			opacity: 0;
		}
		to {
			transform: translateY(0);
			opacity: 1;
		}
	}
</style>
