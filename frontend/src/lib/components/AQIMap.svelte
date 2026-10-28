<script>
	/** @typedef {{city: string, state: string, latitude: number, longitude: number, aqi: number, mainPollutant: string, pm25: number|null, pm10: number|null, no2: number|null, so2: number|null, co: number|null, o3: number|null, lastUpdated: string}} CityAQI */
	import { onMount, onDestroy } from 'svelte';
	import { aqiCategories, getAqiColor, getAqiCategory } from '$lib/data/aqiMockData.js';
	import { getCities, predictCityAQI } from '$lib/api.js';

	/** @type {HTMLElement | null} */
	let mapContainer = null;
	/** @type {any} */
	let map = null;
	/** @type {{ marker: any, data: CityAQI }[]} */
	let markers = [];
	let searchQuery = $state('');
	/** @type {CityAQI | null} */
	let selectedCity = $state(null);
	let searchError = $state('');
	let isLegendOpen = $state(true);
	/** @type {CityAQI[]} */
	let aqiMockData = $state([]);
	let loading = $state(true);
	let dataError = $state('');

	// Leaflet instance (loaded dynamically to avoid SSR issues)
	/** @type {any} */
	let L = null;

	onMount(async () => {
		// Dynamically import Leaflet (browser-only)
		const leaflet = await import('leaflet');
		L = leaflet.default || leaflet;

		// Import Leaflet CSS
		const link = document.createElement('link');
		link.rel = 'stylesheet';
		link.href = 'https://unpkg.com/leaflet@1.9.4/dist/leaflet.css';
		document.head.appendChild(link);

		// Wait a tick for CSS to load
		await new Promise((r) => setTimeout(r, 100));

		initMap();
		loadCityReadings();
	});

	onDestroy(() => {
		if (map) {
			map.remove();
			map = null;
		}
	});

	function initMap() {
		if (!mapContainer || !L || map) return;

		// Initialize map centered on India
		map = L.map(mapContainer, {
			center: [22.5, 78.9],
			zoom: 5,
			zoomControl: false,
			attributionControl: true
		});

		// Add zoom control to bottom-right
		L.control.zoom({ position: 'bottomright' }).addTo(map);

		// Add tile layer (CartoDB Positron for clean look)
		L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
			attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap contributors</a>',
			maxZoom: 19
		}).addTo(map);

		// Check for dark mode and use dark tiles
		if (document.documentElement.classList.contains('dark')) {
		map.eachLayer((/** @type {any} */ layer) => {
				if (layer instanceof L.TileLayer) {
					map.removeLayer(layer);
				}
			});
			L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
				attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap contributors</a>',
				maxZoom: 19
			}).addTo(map);
		}

		// Add AQI markers
		addMarkers();
	}

	async function loadCityReadings() {
		loading = true;
		dataError = '';
		try {
			const { cities = [] } = await getCities();
			// Keep the initial map responsive while still using live backend readings.
			/** @type {{ name: string }[]} */
			const candidates = cities.slice(0, 12);
			const results = await Promise.allSettled(candidates.map(({ name }) => predictCityAQI(name)));
			aqiMockData = results.flatMap((result) => {
				if (result.status !== 'fulfilled' || !Number.isFinite(result.value?.aqi)) return [];
				const value = result.value;
				return [{
				city: value.city, state: value.state, latitude: value.latitude, longitude: value.longitude,
				aqi: value.aqi, mainPollutant: 'PM2.5', pm25: value.pm25, pm10: value.pm10, no2: value.no2,
				so2: value.so2, co: value.co, o3: value.o3,
				lastUpdated: value.timestamp ? new Date(value.timestamp).toLocaleString() : 'Recently'
				}];
			});
			if (!aqiMockData.length) throw new Error('Live AQI readings are unavailable right now. Please try again later.');
			if (results.some((result) => result.status === 'rejected')) dataError = 'Some cities could not be loaded; showing available live readings.';
			if (map) addMarkers();
		} catch (error) { dataError = error instanceof Error ? error.message : 'Unable to load live city data.'; }
		finally { loading = false; }
	}

	function addMarkers() {
		if (!map || !L) return;
		markers.forEach(({ marker }) => marker.remove());
		markers = [];

		aqiMockData.forEach((cityData) => {
			const color = getAqiColor(cityData.aqi);

			// Create a circular marker using divIcon
			const icon = L.divIcon({
				className: 'aqi-marker-icon',
				html: `<div style="
					width: 36px;
					height: 36px;
					border-radius: 50%;
					background: ${color};
					border: 3px solid white;
					box-shadow: 0 2px 8px rgba(0,0,0,0.3), 0 0 0 1px rgba(0,0,0,0.1);
					display: flex;
					align-items: center;
					justify-content: center;
					color: white;
					font-weight: 700;
					font-size: 11px;
					font-family: 'Inter', sans-serif;
					text-shadow: 0 1px 2px rgba(0,0,0,0.3);
					cursor: pointer;
					transition: transform 0.15s ease;
				">${cityData.aqi}</div>`,
				iconSize: [36, 36],
				iconAnchor: [18, 18]
			});

			const marker = L.marker([cityData.latitude, cityData.longitude], { icon }).addTo(map);

			marker.on('click', () => {
				selectCity(cityData);
				map.setView([cityData.latitude, cityData.longitude], 8, { animate: true });
			});

			// Tooltip on hover
			marker.bindTooltip(cityData.city, {
				direction: 'top',
				offset: [0, -20],
				className: 'aqi-tooltip'
			});

			markers.push({ marker, data: cityData });
		});
	}

	/** @param {CityAQI} cityData */
	function selectCity(cityData) {
		selectedCity = cityData;
		searchError = '';
	}

	function handleSearch() {
		searchError = '';
		const query = searchQuery.trim().toLowerCase();

		if (!query) {
			searchError = 'Please enter a city name.';
			return;
		}

		const found = aqiMockData.find((c) => c.city.toLowerCase() === query || `${c.city}, ${c.state}`.toLowerCase() === query);

		if (found) {
			selectCity(found);
			if (map) {
				map.setView([found.latitude, found.longitude], 10, { animate: true });
			}
			// Highlight the marker with a brief pulse
			const markerEntry = markers.find((m) => m.data.city === found.city);
			if (markerEntry) {
				const el = markerEntry.marker.getElement();
				if (el) {
					el.style.transform += ' scale(1.3)';
					setTimeout(() => {
						el.style.transform = el.style.transform.replace(' scale(1.3)', '');
					}, 600);
				}
			}
		} else {
			searchError = 'City not found.';
			selectedCity = null;
		}
	}

	/** @param {KeyboardEvent} e */
	function handleSearchKeydown(e) {
		if (e.key === 'Enter') {
			handleSearch();
		}
	}

	function closeDetails() {
		selectedCity = null;
	}

	/** @param {number} aqi */
	function getCategoryBadgeClasses(aqi) {
		if (aqi <= 50) return 'bg-green-100 text-green-700 dark:bg-green-950/40 dark:text-green-400';
		if (aqi <= 100) return 'bg-yellow-100 text-yellow-700 dark:bg-yellow-950/40 dark:text-yellow-400';
		if (aqi <= 150) return 'bg-orange-100 text-orange-700 dark:bg-orange-950/40 dark:text-orange-400';
		if (aqi <= 200) return 'bg-red-100 text-red-700 dark:bg-red-950/40 dark:text-red-400';
		if (aqi <= 300) return 'bg-purple-100 text-purple-700 dark:bg-purple-950/40 dark:text-purple-400';
		return 'bg-rose-100 text-rose-800 dark:bg-rose-950/40 dark:text-rose-400';
	}
</script>

<div class="aqi-map-wrapper relative w-full">
	{#if loading}<p class="mb-3 text-sm text-zinc-500">Loading live AQI readings…</p>{/if}
	{#if dataError}<p role="status" class="mb-3 text-sm text-amber-600 dark:text-amber-400">{dataError}</p>{/if}
	<!-- Search Bar -->
	<div class="mb-4 flex flex-col sm:flex-row gap-2">
		<div class="relative flex-1">
			<svg class="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-zinc-400 dark:text-zinc-500" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
				<path stroke-linecap="round" stroke-linejoin="round" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
			</svg>
			<input
				type="text"
				bind:value={searchQuery}
				onkeydown={handleSearchKeydown}
				placeholder="Search for a city..."
				class="w-full pl-10 pr-4 py-2.5 bg-white dark:bg-zinc-900 border border-zinc-200/80 dark:border-zinc-800/80 rounded-xl text-sm text-zinc-900 dark:text-zinc-100 placeholder-zinc-400 dark:placeholder-zinc-500 focus:outline-none focus:ring-2 focus:ring-emerald-500/30 focus:border-emerald-500 transition-all"
			/>
		</div>
		<button
			onclick={handleSearch}
			class="px-5 py-2.5 bg-emerald-500 hover:bg-emerald-600 active:scale-95 text-white text-sm font-semibold rounded-xl transition-all shadow-md shadow-emerald-500/10 focus:outline-none cursor-pointer"
		>
			Search
		</button>
	</div>

	{#if searchError}
		<div class="mb-3 px-4 py-2.5 bg-red-50 dark:bg-red-950/20 border border-red-200/60 dark:border-red-800/40 rounded-xl text-sm text-red-600 dark:text-red-400 font-medium">
			{searchError}
		</div>
	{/if}

	<!-- Map + Details Layout -->
	<div class="flex flex-col lg:flex-row gap-4">
		<!-- Map Container -->
		<div class="flex-1 relative">
			<div
				bind:this={mapContainer}
				class="w-full rounded-2xl border border-zinc-200/80 dark:border-zinc-800/80 shadow-sm overflow-hidden"
				style="height: 520px; z-index: 1;"
			></div>

			<!-- AQI Legend (overlaid on map) -->
			<div class="absolute bottom-4 left-4 z-[1000]">
				<button
					onclick={() => (isLegendOpen = !isLegendOpen)}
					class="flex items-center gap-1.5 px-3 py-1.5 bg-white/95 dark:bg-zinc-900/95 backdrop-blur-sm border border-zinc-200/80 dark:border-zinc-800/80 rounded-lg shadow-md text-xs font-semibold text-zinc-700 dark:text-zinc-300 hover:bg-zinc-50 dark:hover:bg-zinc-800 transition-all cursor-pointer"
				>
					<svg class="h-3.5 w-3.5" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
						<path stroke-linecap="round" stroke-linejoin="round" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
					</svg>
					AQI Legend
					<svg class="h-3 w-3 transition-transform duration-200 {isLegendOpen ? 'rotate-180' : ''}" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
						<path stroke-linecap="round" stroke-linejoin="round" d="M19 9l-7 7-7-7" />
					</svg>
				</button>

				{#if isLegendOpen}
					<div class="mt-1.5 bg-white/95 dark:bg-zinc-900/95 backdrop-blur-sm border border-zinc-200/80 dark:border-zinc-800/80 rounded-xl shadow-lg p-3 space-y-1.5 min-w-[200px]">
						{#each aqiCategories as cat}
							<div class="flex items-center gap-2.5">
								<div class="h-3.5 w-3.5 rounded-full shrink-0 shadow-sm" style="background: {cat.color};"></div>
								<span class="text-xs text-zinc-700 dark:text-zinc-300 font-medium">{cat.label}</span>
								<span class="text-xs text-zinc-400 dark:text-zinc-500 ml-auto">{cat.range}</span>
							</div>
						{/each}
					</div>
				{/if}
			</div>
		</div>

		<!-- City Details Panel -->
		{#if selectedCity}
			<div class="w-full lg:w-80 shrink-0">
				<div class="bg-white dark:bg-zinc-900 border border-zinc-200/80 dark:border-zinc-800/80 rounded-2xl shadow-sm overflow-hidden transition-all duration-300">
					<!-- Header -->
					<div class="p-4 border-b border-zinc-100 dark:border-zinc-800/60">
						<div class="flex items-center justify-between">
							<div>
								<h3 class="text-lg font-bold text-zinc-900 dark:text-white">{selectedCity.city}</h3>
								<p class="text-xs text-zinc-500 dark:text-zinc-400">{selectedCity.state}</p>
							</div>
							<button
								aria-label="Close city details"
								onclick={closeDetails}
								class="p-1.5 rounded-lg hover:bg-zinc-100 dark:hover:bg-zinc-800 text-zinc-400 hover:text-zinc-600 dark:hover:text-zinc-300 transition-colors cursor-pointer"
							>
								<svg class="h-4 w-4" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
									<path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12" />
								</svg>
							</button>
						</div>
					</div>

					<!-- AQI Value -->
					<div class="p-4 flex items-center gap-4 border-b border-zinc-100 dark:border-zinc-800/60">
						<div
							class="h-16 w-16 rounded-2xl flex items-center justify-center text-white font-extrabold text-xl shadow-lg"
							style="background: {getAqiColor(selectedCity.aqi)};"
						>
							{selectedCity.aqi}
						</div>
						<div>
							<span class="inline-block px-2.5 py-1 rounded-lg text-xs font-semibold {getCategoryBadgeClasses(selectedCity.aqi)}">
								{getAqiCategory(selectedCity.aqi)}
							</span>
							<p class="text-xs text-zinc-500 dark:text-zinc-400 mt-1">Main Pollutant: <span class="font-semibold text-zinc-700 dark:text-zinc-300">{selectedCity.mainPollutant}</span></p>
						</div>
					</div>

					<!-- Pollutant Details -->
					<div class="p-4 space-y-2.5">
						<h4 class="text-xs font-semibold text-zinc-400 dark:text-zinc-500 uppercase tracking-wider">Pollutants</h4>
						<div class="grid grid-cols-2 gap-2">
							{#each [
								{ label: 'PM2.5', value: selectedCity.pm25, unit: 'µg/m³' },
								{ label: 'PM10', value: selectedCity.pm10, unit: 'µg/m³' },
								{ label: 'NO₂', value: selectedCity.no2, unit: 'ppb' },
								{ label: 'SO₂', value: selectedCity.so2, unit: 'ppb' },
								{ label: 'CO', value: selectedCity.co, unit: 'ppm' },
								{ label: 'O₃', value: selectedCity.o3, unit: 'ppb' }
							] as pollutant}
								<div class="bg-zinc-50 dark:bg-zinc-800/40 rounded-xl px-3 py-2.5">
									<p class="text-[10px] font-semibold text-zinc-400 dark:text-zinc-500 uppercase tracking-wide">{pollutant.label}</p>
									<p class="text-sm font-bold text-zinc-900 dark:text-white mt-0.5">{pollutant.value} <span class="text-[10px] font-normal text-zinc-400 dark:text-zinc-500">{pollutant.unit}</span></p>
								</div>
							{/each}
						</div>
					</div>

					<!-- Last Updated -->
					<div class="px-4 pb-4">
						<div class="flex items-center gap-1.5 text-[10px] text-zinc-400 dark:text-zinc-500">
							<svg class="h-3 w-3" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
								<path stroke-linecap="round" stroke-linejoin="round" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
							</svg>
							Last updated: {selectedCity.lastUpdated}
						</div>
					</div>
				</div>
			</div>
		{/if}
	</div>
	<p class="mt-2 text-xs text-zinc-500">Air-quality data: <a class="underline" href="https://open-meteo.com/" target="_blank" rel="noreferrer">Open-Meteo</a> using CAMS atmospheric composition forecasts.</p>
</div>

<style>
	/* Override Leaflet tooltip styles to match AeriQ */
	:global(.aqi-tooltip) {
		background: white;
		border: 1px solid #e4e4e7;
		border-radius: 8px;
		padding: 4px 10px;
		font-family: 'Inter', sans-serif;
		font-size: 12px;
		font-weight: 600;
		color: #18181b;
		box-shadow: 0 2px 8px rgba(0, 0, 0, 0.12);
	}

	:global(.dark .aqi-tooltip) {
		background: #18181b;
		border-color: #3f3f46;
		color: #fafafa;
	}

	:global(.aqi-tooltip::before) {
		border-top-color: white !important;
	}

	:global(.dark .aqi-tooltip::before) {
		border-top-color: #18181b !important;
	}

	/* Remove default Leaflet marker icon styles for our custom div icons */
	:global(.aqi-marker-icon) {
		background: none !important;
		border: none !important;
	}

	/* Hover scale on markers */
	:global(.aqi-marker-icon > div:hover) {
		transform: scale(1.15) !important;
	}

	/* Leaflet attribution styling */
	:global(.leaflet-control-attribution) {
		font-family: 'Inter', sans-serif !important;
		font-size: 10px !important;
		background: rgba(255, 255, 255, 0.85) !important;
		border-radius: 6px !important;
		padding: 2px 6px !important;
	}

	:global(.dark .leaflet-control-attribution) {
		background: rgba(24, 24, 27, 0.85) !important;
		color: #a1a1aa !important;
	}

	:global(.dark .leaflet-control-attribution a) {
		color: #6ee7b7 !important;
	}

	/* Zoom control dark mode */
	:global(.dark .leaflet-control-zoom a) {
		background-color: #18181b !important;
		color: #fafafa !important;
		border-color: #3f3f46 !important;
	}

	:global(.dark .leaflet-control-zoom a:hover) {
		background-color: #27272a !important;
	}
</style>
