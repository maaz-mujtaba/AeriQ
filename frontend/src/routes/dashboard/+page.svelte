<script>
	import { onMount } from 'svelte';
	import { currentAQI, isLoading, errorMessage } from '$lib/stores/aqiStore.js';
	import { loadCurrentAQI } from '$lib/api.js';

	// Component imports
	import AQICard from '$lib/components/AQICard.svelte';
	import WeatherCard from '$lib/components/WeatherCard.svelte';
	import PollutantCard from '$lib/components/PollutantCard.svelte';
	import HealthCard from '$lib/components/HealthCard.svelte';
	import StatsCard from '$lib/components/StatsCard.svelte';

	// City selection and coordinate mapping
	let activeCityKey = $state('delhi');
	let isRefreshing = $state(false);

	// Lazy load components states
	/** @type {any} */
	let TrendChart = $state(null);
	/** @type {any} */
	let ForecastPreview = $state(null);

	// Live ticking clock state
	let currentTime = $state('');

	onMount(() => {
		const updateTime = () => {
			currentTime = new Date().toLocaleTimeString('en-US', {
				hour: '2-digit',
				minute: '2-digit',
				second: '2-digit',
				hour12: true
			});
		};
		updateTime();
		const interval = setInterval(updateTime, 1000);

		// Lazy load large rendering components
		Promise.all([
			import('$lib/components/TrendChart.svelte'),
			import('$lib/components/ForecastPreview.svelte')
		]).then(([tcModule, fpModule]) => {
			TrendChart = tcModule.default;
			ForecastPreview = fpModule.default;
		}).catch(err => {
			console.error('Failed to prefetch dynamic analytics panels:', err);
		});

		return () => clearInterval(interval);
	});

	const cityProfiles = {
		delhi: {
			name: 'New Delhi, India',
			lat: 28.6139,
			lon: 77.209,
			aqi: 185,
			weather: {
				temp: 32,
				feelsLike: 35,
				humidity: 65,
				wind: 12,
				windDir: 'NNE',
				press: 1008,
				visibility: 3.5,
				uvIndex: '8 (V. High)',
				sunrise: '05:35 AM',
				sunset: '07:12 PM',
				desc: 'Moderate Haze'
			},
			pollutants: [
				{ name: 'PM2.5', value: 120, unit: 'µg/m³', status: 'Poor', trendDelta: '+2.4%', trendDirection: 'up', path: 'M0 30 Q15 10, 30 25 T60 15 T90 35 T120 10' },
				{ name: 'PM10', value: 185, unit: 'µg/m³', status: 'Poor', trendDelta: '+3.1%', trendDirection: 'up', path: 'M0 25 Q15 5, 30 20 T60 10 T90 30 T120 15' },
				{ name: 'NO₂', value: 48, unit: 'µg/m³', status: 'Moderate', trendDelta: '-1.2%', trendDirection: 'down', path: 'M0 15 Q15 25, 30 15 T60 20 T90 10 T120 18' },
				{ name: 'O₃', value: 85, unit: 'µg/m³', status: 'Moderate', trendDelta: '+0.8%', trendDirection: 'up', path: 'M0 20 Q15 10, 30 18 T60 12 T90 22 T120 14' },
				{ name: 'CO', value: 1.8, unit: 'mg/m³', status: 'Good', trendDelta: '-2.0%', trendDirection: 'down', path: 'M0 10 Q15 12, 30 8 T60 14 T90 8 T120 11' }
			],
			station: 'Delhi Secretariat, 1.2km away',
			outdoorTime: '06:00 AM - 08:30 AM (Fair)',
			outdoorRating: 'Fair',
			healthRisk: 'High',
			healthRiskColor: 'text-red-500 bg-red-500/10 border-red-500/20',
			yesterdayAqi: 210,
			rank: '188/250',
			liveStatus: 'Active & Calibrated',
			health: [
				{ icon: 'mask', title: 'Wear Mask Outdoors', description: 'General public should wear N95 respirator masks when stepping outdoors to block fine PM2.5 particles.', type: 'warning', priority: 'High Priority', action: 'Equip standard N95 mask before leaving home.' },
				{ icon: 'windows', title: 'Keep Windows Closed', description: 'Close windows to prevent high density ambient haze from entering indoor environments.', type: 'warning', priority: 'High Priority', action: 'Lock external windows and activate indoor air filtration.' },
				{ icon: 'exercise', title: 'Avoid Outdoor Workouts', description: 'Heavy cardiovascular breathing outdoors will increase pollutant load in lungs.', type: 'warning', priority: 'High Priority', action: 'Perform lightweight bodyweight stretching exercises indoors.' },
				{ icon: 'water', title: 'Drink More Water', description: 'Elevate fluid levels to support natural throat mucosal clearing systems.', type: 'success', priority: 'Recommended', action: 'Aim for 3-4 liters of filtered room-temperature water today.' }
			]
		},
		newyork: {
			name: 'New York, USA',
			lat: 40.7128,
			lon: -74.006,
			aqi: 35,
			weather: {
				temp: 24,
				feelsLike: 23,
				humidity: 50,
				wind: 16,
				windDir: 'WNW',
				press: 1016,
				visibility: 10.0,
				uvIndex: '4 (Mod)',
				sunrise: '05:42 AM',
				sunset: '08:25 PM',
				desc: 'Clear Sky'
			},
			pollutants: [
				{ name: 'PM2.5', value: 8, unit: 'µg/m³', status: 'Good', trendDelta: '-0.5%', trendDirection: 'down', path: 'M0 10 Q15 8, 30 12 T60 7 T90 11 T120 6' },
				{ name: 'PM10', value: 15, unit: 'µg/m³', status: 'Good', trendDelta: '-1.0%', trendDirection: 'down', path: 'M0 15 Q15 12, 30 14 T60 10 T90 13 T120 9' },
				{ name: 'NO₂', value: 12, unit: 'µg/m³', status: 'Good', trendDelta: '+0.2%', trendDirection: 'up', path: 'M0 8 Q15 10, 30 7 T60 9 T90 6 T120 8' },
				{ name: 'O₃', value: 32, unit: 'µg/m³', status: 'Good', trendDelta: '-2.4%', trendDirection: 'down', path: 'M0 20 Q15 18, 30 22 T60 16 T90 19 T120 15' },
				{ name: 'CO', value: 0.4, unit: 'mg/m³', status: 'Good', trendDelta: '0.0%', trendDirection: 'flat', path: 'M0 5 Q15 4, 30 6 T60 3 T90 5 T120 3' }
			],
			station: 'Central Park West, 0.4km away',
			outdoorTime: '08:00 AM - 06:00 PM (Excellent)',
			outdoorRating: 'Excellent',
			healthRisk: 'Minimal',
			healthRiskColor: 'text-emerald-500 bg-emerald-500/10 border-emerald-500/20',
			yesterdayAqi: 38,
			rank: '12/250',
			liveStatus: 'Active & Calibrated',
			health: [
				{ icon: 'walking', title: 'Ideal for Walking', description: 'Air quality is pristine. Perfect conditions for walking, exploring parks, or standard outdoor strolls.', type: 'success', priority: 'Recommended', action: 'Plan an outdoor walk or hike in Central Park.' },
				{ icon: 'windows', title: 'Open Home Windows', description: 'Air is fresh. Open wide to ventilate indoor living spaces and clear stagnant particles.', type: 'success', priority: 'Recommended', action: 'Keep windows open for at least 4-6 hours today.' },
				{ icon: 'exercise', title: 'Outdoor Exercise Approved', description: 'Exceptional safety margins. Fine for running, cycling, or outdoor tennis matches.', type: 'success', priority: 'Recommended', action: 'Perform standard training outdoors without restrictions.' },
				{ icon: 'water', title: 'Maintain Normal Hydration', description: 'Drink water normally to align with your standard biological indices.', type: 'info', priority: 'Information', action: 'Keep standard hydration goals.' }
			]
		},
		london: {
			name: 'London, UK',
			lat: 51.5074,
			lon: -0.1278,
			aqi: 55,
			weather: {
				temp: 18,
				feelsLike: 17,
				humidity: 75,
				wind: 20,
				windDir: 'SW',
				press: 1012,
				visibility: 8.0,
				uvIndex: '2 (Low)',
				sunrise: '05:08 AM',
				sunset: '09:05 PM',
				desc: 'Light Drizzle'
			},
			pollutants: [
				{ name: 'PM2.5', value: 14, unit: 'µg/m³', status: 'Good', trendDelta: '+0.4%', trendDirection: 'up', path: 'M0 12 Q15 15, 30 10 T60 14 T90 9 T120 11' },
				{ name: 'PM10', value: 28, unit: 'µg/m³', status: 'Good', trendDelta: '+0.8%', trendDirection: 'up', path: 'M0 20 Q15 25, 30 18 T60 22 T90 15 T120 19' },
				{ name: 'NO₂', value: 26, unit: 'µg/m³', status: 'Good', trendDelta: '-0.3%', trendDirection: 'down', path: 'M0 18 Q15 22, 30 16 T60 20 T90 14 T120 17' },
				{ name: 'O₃', value: 52, unit: 'µg/m³', status: 'Moderate', trendDelta: '+1.5%', trendDirection: 'up', path: 'M0 25 Q15 30, 30 22 T60 28 T90 19 T120 24' },
				{ name: 'CO', value: 0.6, unit: 'mg/m³', status: 'Good', trendDelta: '0.0%', trendDirection: 'flat', path: 'M0 8 Q15 6, 30 9 T60 5 T90 7 T120 5' }
			],
			station: 'Westminster Green, 1.5km away',
			outdoorTime: '10:00 AM - 04:00 PM (Good)',
			outdoorRating: 'Good',
			healthRisk: 'Low',
			healthRiskColor: 'text-emerald-450 bg-emerald-500/5 border-emerald-500/10',
			yesterdayAqi: 52,
			rank: '42/250',
			liveStatus: 'Active & Calibrated',
			health: [
				{ icon: 'walking', title: 'Suitable for Walking', description: 'Air quality is acceptable. Safe to enjoy walking, though light drizzle is expected.', type: 'success', priority: 'Recommended', action: 'Safe to walk outside; bringing an umbrella is advised.' },
				{ icon: 'windows', title: 'Open Windows', description: 'Clean fresh air indexes are satisfactory. Safe to ventilate rooms for short cycles.', type: 'success', priority: 'Recommended', action: 'Open windows for 30 minutes to circulate air.' },
				{ icon: 'exercise', title: 'Moderate Outdoor Exercise', description: 'Outdoor exercises are fine, but sensitive groups should monitor symptoms.', type: 'info', priority: 'Information', action: 'Limit high intensity outdoor runs if you feel wheezing.' },
				{ icon: 'water', title: 'Drink Warm Fluid', description: 'Hydrating with warm tea or water comforts your throat in chilly damp weather.', type: 'info', priority: 'Information', action: 'Drink warm water regularly.' }
			]
		},
		tokyo: {
			name: 'Tokyo, Japan',
			lat: 35.6762,
			lon: 139.6503,
			aqi: 82,
			weather: {
				temp: 26,
				feelsLike: 25,
				humidity: 62,
				wind: 8,
				windDir: 'S',
				press: 1014,
				visibility: 7.5,
				uvIndex: '5 (Mod)',
				sunrise: '04:50 AM',
				sunset: '06:48 PM',
				desc: 'Partly Cloudy'
			},
			pollutants: [
				{ name: 'PM2.5', value: 26, unit: 'µg/m³', status: 'Moderate', trendDelta: '+1.2%', trendDirection: 'up', path: 'M0 18 Q15 22, 30 14 T60 20 T90 12 T120 16' },
				{ name: 'PM10', value: 42, unit: 'µg/m³', status: 'Good', trendDelta: '+0.5%', trendDirection: 'up', path: 'M0 25 Q15 30, 30 20 T60 26 T90 18 T120 22' },
				{ name: 'NO₂', value: 32, unit: 'µg/m³', status: 'Good', trendDelta: '-0.8%', trendDirection: 'down', path: 'M0 20 Q15 24, 30 16 T60 22 T90 14 T120 18' },
				{ name: 'O₃', value: 72, unit: 'µg/m³', status: 'Moderate', trendDelta: '+2.1%', trendDirection: 'up', path: 'M0 30 Q15 35, 30 25 T60 32 T90 22 T120 28' },
				{ name: 'CO', value: 0.8, unit: 'mg/m³', status: 'Good', trendDelta: '0.0%', trendDirection: 'flat', path: 'M0 10 Q15 8, 30 11 T60 7 T90 9 T120 7' }
			],
			station: 'Shinjuku Center, 0.8km away',
			outdoorTime: '06:00 AM - 11:00 AM (Good)',
			outdoorRating: 'Good',
			healthRisk: 'Moderate',
			healthRiskColor: 'text-amber-500 bg-amber-500/10 border-amber-500/20',
			yesterdayAqi: 78,
			rank: '88/250',
			liveStatus: 'Active & Calibrated',
			health: [
				{ icon: 'walking', title: 'Suitable Walking Time', description: 'Air quality is moderate. Outdoor walking is safe for most healthy adults.', type: 'success', priority: 'Recommended', action: 'Brisk walk around parks is safe today.' },
				{ icon: 'windows', title: 'Off-Peak Ventilation', description: 'Open windows during early morning or late evening hours to avoid vehicle soot.', type: 'info', priority: 'Information', action: 'Ventilate rooms between 06:00-08:00 AM.' },
				{ icon: 'exercise', title: 'Standard Workouts Approved', description: 'No severe warnings. Standard runs are fine, but keep away from heavy avenues.', type: 'success', priority: 'Recommended', action: 'Run in residential zones with trees.' },
				{ icon: 'water', title: 'Regular Hydration', description: 'Drink adequate water to help clear small particulates.', type: 'info', priority: 'Information', action: 'Keep water bottle at hand.' }
			]
		},
		sydney: {
			name: 'Sydney, Australia',
			lat: -33.8688,
			lon: 151.2093,
			aqi: 24,
			weather: {
				temp: 16,
				feelsLike: 15,
				humidity: 55,
				wind: 24,
				windDir: 'W',
				press: 1020,
				visibility: 10.0,
				uvIndex: '1 (Low)',
				sunrise: '06:55 AM',
				sunset: '05:02 PM',
				desc: 'Windy'
			},
			pollutants: [
				{ name: 'PM2.5', value: 5, unit: 'µg/m³', status: 'Good', trendDelta: '-0.2%', trendDirection: 'down', path: 'M0 5 Q15 3, 30 7 T60 4 T90 6 T120 3' },
				{ name: 'PM10', value: 12, unit: 'µg/m³', status: 'Good', trendDelta: '-0.4%', trendDirection: 'down', path: 'M0 10 Q15 8, 30 11 T60 7 T90 9 T120 6' },
				{ name: 'NO₂', value: 8, unit: 'µg/m³', status: 'Good', trendDelta: '0.0%', trendDirection: 'flat', path: 'M0 6 Q15 5, 30 7 T60 4 T90 6 T120 3' },
				{ name: 'O₃', value: 24, unit: 'µg/m³', status: 'Good', trendDelta: '-0.9%', trendDirection: 'down', path: 'M0 15 Q15 13, 30 18 T60 12 T90 15 T120 11' },
				{ name: 'CO', value: 0.3, unit: 'mg/m³', status: 'Good', trendDelta: '0.0%', trendDirection: 'flat', path: 'M0 3 Q15 2, 30 4 T60 2 T90 3 T120 2' }
			],
			station: 'Circular Quay, 0.6km away',
			outdoorTime: '07:00 AM - 05:00 PM (Excellent)',
			outdoorRating: 'Excellent',
			healthRisk: 'Minimal',
			healthRiskColor: 'text-emerald-500 bg-emerald-500/10 border-emerald-500/20',
			yesterdayAqi: 22,
			rank: '5/250',
			liveStatus: 'Active & Calibrated',
			health: [
				{ icon: 'walking', title: 'Pristine Walking Conditions', description: 'Sea breeze air is clean. Outstanding opportunity for outdoor walks.', type: 'success', priority: 'Recommended', action: 'Enjoy coastal walking pathways.' },
				{ icon: 'windows', title: 'Ventilate Openly', description: 'Excellent freshness. Keep windows open to ventilate rooms completely.', type: 'success', priority: 'Recommended', action: 'Open all windows for active air circulation.' },
				{ icon: 'exercise', title: 'Outdoor Exercises Encouraged', description: 'Pristine index values. Excellent for running or competitive outdoor sports.', type: 'success', priority: 'Recommended', action: 'Train outdoors normally.' },
				{ icon: 'water', title: 'Drink Water', description: 'Maintain standard hydration goals.', type: 'info', priority: 'Information', action: 'Drink water normally.' }
			]
		}
	};

	// Determine welcome greeting dynamically
	let greetingText = $derived.by(() => {
		const hour = new Date().getHours();
		if (hour < 12) return 'Good Morning';
		if (hour < 17) return 'Good Afternoon';
		return 'Good Evening';
	});

	// Dynamic Date formatting
	let formattedDate = $derived.by(() => {
		return new Date().toLocaleDateString('en-US', {
			weekday: 'long',
			year: 'numeric',
			month: 'long',
			day: 'numeric'
		});
	});

	// Derive the active mock profile
	let activeProfile = $derived(/** @type {any} */(cityProfiles)[activeCityKey]);

	// Bind data based on active stores or fall back to mock profile
	/** @type {any} */
	let typedAQI = $derived($currentAQI);

	let activeAQI = $derived(typedAQI ? typedAQI.aqi : activeProfile.aqi);
	let activeLocation = $derived(typedAQI ? `${typedAQI.city}, ${typedAQI.state || ''}` : activeProfile.name);
	let activeTemp = $derived(typedAQI ? typedAQI.temperature : activeProfile.weather.temp);
	let activeHumidity = $derived(typedAQI ? typedAQI.humidity : activeProfile.weather.humidity);
	let activeWind = $derived(typedAQI ? typedAQI.wind_speed : activeProfile.weather.wind);
	let activePressure = $derived(activeProfile.weather.press); // fallback pressure
	let activeDesc = $derived(
		typedAQI
			? activeAQI <= 50 ? 'Clear Sky' : activeAQI <= 100 ? 'Partly Cloudy' : activeAQI <= 150 ? 'Moderate Haze' : 'Dense Smog'
			: activeProfile.weather.desc
	);

	// Pollutants mapping
	let pollutantsList = $derived.by(() => {
		if (typedAQI) {
			return [
				{ name: 'PM2.5', value: typedAQI.pm25, unit: 'µg/m³', status: typedAQI.pm25 <= 30 ? 'Good' : typedAQI.pm25 <= 60 ? 'Moderate' : 'Poor', trendDelta: '+1.5%', trendDirection: 'up', path: 'M0 30 Q15 10, 30 25 T60 15 T90 35 T120 10' },
				{ name: 'PM10', value: typedAQI.pm10, unit: 'µg/m³', status: typedAQI.pm10 <= 50 ? 'Good' : typedAQI.pm10 <= 100 ? 'Moderate' : 'Poor', trendDelta: '+0.9%', trendDirection: 'up', path: 'M0 25 Q15 5, 30 20 T60 10 T90 30 T120 15' },
				{ name: 'NO₂', value: typedAQI.no2, unit: 'µg/m³', status: typedAQI.no2 <= 40 ? 'Good' : typedAQI.no2 <= 80 ? 'Moderate' : 'Poor', trendDelta: '-2.1%', trendDirection: 'down', path: 'M0 15 Q15 25, 30 15 T60 20 T90 10 T120 18' },
				{ name: 'O₃', value: typedAQI.o3, unit: 'µg/m³', status: typedAQI.o3 <= 50 ? 'Good' : typedAQI.o3 <= 100 ? 'Moderate' : 'Poor', trendDelta: '+0.5%', trendDirection: 'up', path: 'M0 20 Q15 10, 30 18 T60 12 T90 22 T120 14' },
				{ name: 'CO', value: typedAQI.co, unit: 'mg/m³', status: typedAQI.co <= 2.0 ? 'Good' : typedAQI.co <= 4.0 ? 'Moderate' : 'Poor', trendDelta: '0.0%', trendDirection: 'flat', path: 'M0 10 Q15 12, 30 8 T60 14 T90 8 T120 11' }
			];
		}
		return activeProfile.pollutants;
	});

	// Trigger simulated refresh
	async function handleRefresh() {
		isRefreshing = true;
		try {
			// Trigger store load if api returns data
			await loadCurrentAQI(activeProfile.lat, activeProfile.lon);
		} catch (err) {
			console.log('Unable to connect to live API. Using rich simulated profile data fallback.');
		} finally {
			// Brief smooth loading transition
			setTimeout(() => {
				isRefreshing = false;
			}, 600);
		}
	}



	// Listen to active tab shifts to sync api loading
	$effect(() => {
		loadCurrentAQI(activeProfile.lat, activeProfile.lon).catch(() => {});
	});
</script>

<div class="space-y-8 select-none relative animate-fade-in">
	<!-- Glass Loading Spinner Overlay -->
	{#if isRefreshing || $isLoading}
		<div class="fixed inset-0 bg-white/30 dark:bg-zinc-950/30 backdrop-blur-sm z-50 flex items-center justify-center transition-all duration-300">
			<div class="flex flex-col items-center gap-3 p-6 bg-white dark:bg-zinc-900 border border-zinc-100 dark:border-zinc-800 rounded-2xl shadow-xl animate-scale-up">
				<svg class="h-8 w-8 text-emerald-500 animate-spin" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="3">
					<circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
					<path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
				</svg>
				<span class="text-xs font-bold text-zinc-600 dark:text-zinc-300">Syncing Air Quality...</span>
			</div>
		</div>
	{/if}

	<!-- ==================== SECTION 1: Greeting Header ==================== -->
	<div class="flex flex-col md:flex-row md:items-center justify-between gap-4 border-b border-zinc-200/40 dark:border-zinc-800 pb-5 z-10 relative">
		<div class="space-y-1">
			<div class="flex items-center gap-2 text-xs font-bold text-zinc-400 dark:text-zinc-500 uppercase tracking-wider">
				<span>Analytics Hub</span>
				<span>/</span>
				<span class="text-emerald-500 dark:text-emerald-400">Dashboard</span>
			</div>
			<h1 class="text-2xl sm:text-3xl font-black tracking-tight text-zinc-900 dark:text-white flex items-center gap-2">
				{greetingText} 👋
			</h1>
			<p class="text-xs sm:text-sm font-semibold text-zinc-500 dark:text-zinc-400">
				Welcome back. Here is your live air quality update for <span class="font-black text-zinc-850 dark:text-zinc-200">{activeLocation}</span>.
			</p>
			<!-- Ticking Clock display -->
			<div class="flex items-center gap-2 text-xs font-bold text-zinc-450 dark:text-zinc-500 mt-1">
				<svg class="h-3.5 w-3.5" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
					<path stroke-linecap="round" stroke-linejoin="round" d="M12 6v6h4.5m4.5 0a9 9 0 11-18 0 9 9 0 0118 0z" />
				</svg>
				<span>{formattedDate}</span>
				<span>•</span>
				<span class="text-emerald-500 dark:text-emerald-400 tabular-nums">{currentTime || '--:--:--'}</span>
			</div>
		</div>

		<!-- Action Buttons -->
		<div class="flex items-center gap-2 flex-wrap">
			<!-- Share Action -->
			<button class="px-3.5 py-2.5 bg-white/40 dark:bg-zinc-900/45 border border-zinc-200 dark:border-zinc-800 rounded-xl text-xs font-bold text-zinc-700 dark:text-zinc-300 hover:text-zinc-950 dark:hover:text-zinc-150 hover:bg-white dark:hover:bg-zinc-800 shadow-sm focus:outline-none flex items-center gap-1.5 active:scale-95 transition-all">
				<svg class="h-3.5 w-3.5 text-zinc-400" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
					<path stroke-linecap="round" stroke-linejoin="round" d="M8.684 10.742l5.052-2.526M8.684 13.258l5.052 2.526M21 8a3 3 0 11-6 0 3 3 0 016 0zm-6 8a3 3 0 11-6 0 3 3 0 016 0zM6 12a3 3 0 11-6 0 3 3 0 016 0z" />
				</svg>
				Share
			</button>
			<!-- Refresh Trigger -->
			<button
				onclick={handleRefresh}
				class="px-3.5 py-2.5 bg-white/40 dark:bg-zinc-900/45 border border-zinc-200 dark:border-zinc-800 rounded-xl text-xs font-bold text-zinc-700 dark:text-zinc-300 hover:text-zinc-950 dark:hover:text-zinc-150 hover:bg-white dark:hover:bg-zinc-800 shadow-sm focus:outline-none flex items-center gap-1.5 active:scale-95 transition-all"
			>
				<svg class="h-3.5 w-3.5 text-zinc-400" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
					<path stroke-linecap="round" stroke-linejoin="round" d="M4 4v5h.582m15.356 2A8.001 8.001 0 1121.21 7.89H18" />
				</svg>
				Refresh Data
			</button>
			<!-- Add Widget (UI ONLY) -->
			<button class="px-3.5 py-2.5 bg-zinc-950 dark:bg-zinc-800 hover:bg-zinc-900 dark:hover:bg-zinc-700 text-white rounded-xl text-xs font-bold shadow-sm focus:outline-none flex items-center gap-1.5 active:scale-95 transition-all">
				<svg class="h-3.5 w-3.5 text-zinc-400" fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24">
					<path stroke-linecap="round" stroke-linejoin="round" d="M12 4v16m8-8H4" />
				</svg>
				Add Widget
			</button>
		</div>
	</div>

	<!-- Interactive Tab Selector to change mock datasets -->
	<div class="flex items-center gap-1.5 p-1 bg-zinc-200/50 dark:bg-zinc-900 rounded-xl max-w-fit overflow-x-auto select-none border border-zinc-200/50 dark:border-zinc-800/50 z-10 relative">
		<button onclick={() => activeCityKey = 'delhi'} class="px-3.5 py-1.5 text-xs font-bold rounded-lg transition-all focus:outline-none {activeCityKey === 'delhi' ? 'bg-white dark:bg-zinc-800 text-emerald-600 dark:text-emerald-450 shadow-sm scale-[1.02]' : 'text-zinc-500 hover:text-zinc-800 dark:hover:text-zinc-200'}">
			New Delhi
		</button>
		<button onclick={() => activeCityKey = 'newyork'} class="px-3.5 py-1.5 text-xs font-bold rounded-lg transition-all focus:outline-none {activeCityKey === 'newyork' ? 'bg-white dark:bg-zinc-800 text-emerald-600 dark:text-emerald-450 shadow-sm scale-[1.02]' : 'text-zinc-500 hover:text-zinc-800 dark:hover:text-zinc-200'}">
			New York
		</button>
		<button onclick={() => activeCityKey = 'london'} class="px-3.5 py-1.5 text-xs font-bold rounded-lg transition-all focus:outline-none {activeCityKey === 'london' ? 'bg-white dark:bg-zinc-800 text-emerald-600 dark:text-emerald-450 shadow-sm scale-[1.02]' : 'text-zinc-500 hover:text-zinc-800 dark:hover:text-zinc-200'}">
			London
		</button>
		<button onclick={() => activeCityKey = 'tokyo'} class="px-3.5 py-1.5 text-xs font-bold rounded-lg transition-all focus:outline-none {activeCityKey === 'tokyo' ? 'bg-white dark:bg-zinc-800 text-emerald-600 dark:text-emerald-450 shadow-sm scale-[1.02]' : 'text-zinc-500 hover:text-zinc-800 dark:hover:text-zinc-200'}">
			Tokyo
		</button>
		<button onclick={() => activeCityKey = 'sydney'} class="px-3.5 py-1.5 text-xs font-bold rounded-lg transition-all focus:outline-none {activeCityKey === 'sydney' ? 'bg-white dark:bg-zinc-800 text-emerald-600 dark:text-emerald-450 shadow-sm scale-[1.02]' : 'text-zinc-500 hover:text-zinc-800 dark:hover:text-zinc-200'}">
			Sydney
		</button>
	</div>

	<!-- ==================== SECTION 2 & 3: Hero AQI & Weather ==================== -->
	<div class="grid grid-cols-1 lg:grid-cols-3 gap-6 z-10 relative">
		<!-- Hero AQI Card -->
		<div class="lg:col-span-2">
			<AQICard aqi={activeAQI} location={activeLocation} lastUpdated="Just now" />
		</div>
		<!-- Weather Card -->
		<div>
			<WeatherCard
				temperature={activeTemp}
				humidity={activeHumidity}
				windSpeed={activeWind}
				pressure={activePressure}
				description={activeDesc}
				feelsLike={activeProfile.weather.feelsLike}
				windDir={activeProfile.weather.windDir}
				visibility={activeProfile.weather.visibility}
				uvIndex={activeProfile.weather.uvIndex}
				sunrise={activeProfile.weather.sunrise}
				sunset={activeProfile.weather.sunset}
			/>
		</div>
	</div>

	<!-- ==================== SECTION 4: Pollutant Cards ==================== -->
	<div class="space-y-3 z-10 relative animate-slide-up">
		<h3 class="text-xs font-bold text-zinc-400 dark:text-zinc-500 uppercase tracking-wider">Breakdown of Pollutants</h3>
		<div class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-5 gap-4">
			{#each pollutantsList as poll}
				<PollutantCard
					name={poll.name}
					value={poll.value}
					unit={poll.unit}
					status={poll.status}
					trendDelta={poll.trendDelta}
					trendDirection={poll.trendDirection}
					sparklinePath={poll.path}
				/>
			{/each}
		</div>
	</div>

	<!-- ==================== NEW SECTION: Diagnostic Analysis Widgets ==================== -->
	<div class="space-y-3 z-10 relative">
		<h3 class="text-xs font-bold text-zinc-400 dark:text-zinc-500 uppercase tracking-wider">Diagnostic Analysis</h3>
		<div class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-4">
			<!-- Widget 1: Nearest Monitoring Station -->
			<div class="bg-white/40 dark:bg-zinc-900/40 border border-white/20 dark:border-zinc-800/80 backdrop-blur-xl rounded-2xl p-4 shadow-sm space-y-2.5 flex flex-col justify-between hover:shadow hover:border-emerald-500/20 dark:hover:border-zinc-700 transition-all duration-300">
				<div class="flex items-center justify-between text-zinc-400">
					<span class="text-[9px] font-bold uppercase tracking-wider">Nearest Station</span>
					<svg class="h-4.5 w-4.5 text-emerald-500" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
						<path stroke-linecap="round" stroke-linejoin="round" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
					</svg>
				</div>
				<div class="space-y-0.5">
					<p class="text-xs font-black text-zinc-800 dark:text-zinc-200 truncate leading-snug">{activeProfile.station.split(',')[0]}</p>
					<p class="text-[10px] text-zinc-400 dark:text-zinc-500 font-semibold">{activeProfile.station.split(',')[1]}</p>
				</div>
				<span class="text-[9px] font-extrabold text-emerald-500 uppercase tracking-wider flex items-center gap-1.5 leading-none">
					<span class="h-1.5 w-1.5 rounded-full bg-emerald-500 animate-pulse"></span>
					Online
				</span>
			</div>

			<!-- Widget 2: Best Outdoor activities window -->
			<div class="bg-white/40 dark:bg-zinc-900/40 border border-white/20 dark:border-zinc-800/80 backdrop-blur-xl rounded-2xl p-4 shadow-sm space-y-2.5 flex flex-col justify-between hover:shadow hover:border-emerald-500/20 dark:hover:border-zinc-700 transition-all duration-300">
				<div class="flex items-center justify-between text-zinc-400">
					<span class="text-[9px] font-bold uppercase tracking-wider">Best Window</span>
					<svg class="h-4.5 w-4.5 text-emerald-500" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
						<path stroke-linecap="round" stroke-linejoin="round" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
					</svg>
				</div>
				<div class="space-y-0.5">
					<p class="text-xs font-black text-zinc-800 dark:text-zinc-200 leading-snug">{activeProfile.outdoorTime.split('(')[0]}</p>
					<p class="text-[10px] text-zinc-450 dark:text-zinc-500 font-semibold">Quality: <span class="font-bold text-emerald-500">{activeProfile.outdoorRating}</span></p>
				</div>
				<div class="w-full bg-zinc-200/50 dark:bg-zinc-800 h-1 rounded-full overflow-hidden leading-none">
					<div class="bg-emerald-500 h-1 rounded-full transition-all duration-700" style="width: {activeAQI <= 50 ? '100%' : activeAQI <= 100 ? '70%' : activeAQI <= 150 ? '45%' : '15%'}"></div>
				</div>
			</div>

			<!-- Widget 3: Today's Health Risk -->
			<div class="bg-white/40 dark:bg-zinc-900/40 border border-white/20 dark:border-zinc-800/80 backdrop-blur-xl rounded-2xl p-4 shadow-sm space-y-2.5 flex flex-col justify-between hover:shadow hover:border-emerald-500/20 dark:hover:border-zinc-700 transition-all duration-300">
				<div class="flex items-center justify-between text-zinc-400">
					<span class="text-[9px] font-bold uppercase tracking-wider">Health Risk</span>
					<svg class="h-4.5 w-4.5 text-emerald-500" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
						<path stroke-linecap="round" stroke-linejoin="round" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
					</svg>
				</div>
				<div class="space-y-0.5">
					<p class="text-xs font-black text-zinc-850 dark:text-zinc-200 leading-snug">{activeProfile.healthRisk}</p>
					<p class="text-[10px] text-zinc-400 dark:text-zinc-500 font-semibold">{activeAQI <= 100 ? 'Low exposure risk' : 'Elevated risk levels'}</p>
				</div>
				<span class="text-[9px] font-extrabold uppercase tracking-wider leading-none {activeAQI <= 100 ? 'text-emerald-500' : 'text-amber-500'}">
					{activeAQI <= 100 ? 'Safe margins' : 'Caution advised'}
				</span>
			</div>

			<!-- Widget 4: Yesterday vs Today AQI -->
			<div class="bg-white/40 dark:bg-zinc-900/40 border border-white/20 dark:border-zinc-800/80 backdrop-blur-xl rounded-2xl p-4 shadow-sm space-y-2.5 flex flex-col justify-between hover:shadow hover:border-emerald-500/20 dark:hover:border-zinc-700 transition-all duration-300">
				<div class="flex items-center justify-between text-zinc-400">
					<span class="text-[9px] font-bold uppercase tracking-wider">AQI Compare</span>
					<svg class="h-4.5 w-4.5 text-emerald-500" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
						<path stroke-linecap="round" stroke-linejoin="round" d="M7 12l3-3 3 3 4-4M8 21h8a3 3 0 003-3V6a3 3 0 00-3-3H8a3 3 0 00-3 3v12a3 3 0 003 3z" />
					</svg>
				</div>
				<div class="space-y-0.5">
					<p class="text-xs font-black text-zinc-800 dark:text-zinc-200 leading-snug">{activeProfile.yesterdayAqi} <span class="text-[9px] text-zinc-400 font-semibold">vs</span> {activeAQI}</p>
					<p class="text-[9px] font-black uppercase tracking-wider mt-0.5 {activeAQI <= activeProfile.yesterdayAqi ? 'text-emerald-500' : 'text-red-500'}">
						{activeAQI <= activeProfile.yesterdayAqi ? 'Improving' : 'Worsening'}
					</p>
				</div>
				<span class="text-[9px] font-extrabold text-zinc-450 dark:text-zinc-550 leading-none">
					{Math.abs(Math.round(((activeAQI - activeProfile.yesterdayAqi) / activeProfile.yesterdayAqi) * 100))}% shift vs yesterday
				</span>
			</div>

			<!-- Widget 5: Air Quality Ranking -->
			<div class="bg-white/40 dark:bg-zinc-900/40 border border-white/20 dark:border-zinc-800/80 backdrop-blur-xl rounded-2xl p-4 shadow-sm space-y-2.5 flex flex-col justify-between hover:shadow hover:border-emerald-500/20 dark:hover:border-zinc-700 transition-all duration-300">
				<div class="flex items-center justify-between text-zinc-400">
					<span class="text-[9px] font-bold uppercase tracking-wider">Global Rank</span>
					<svg class="h-4.5 w-4.5 text-emerald-500" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
						<path stroke-linecap="round" stroke-linejoin="round" d="M9 12l2 2 4-4M7.835 4.697a3.42 3.42 0 001.946-.806 3.42 3.42 0 014.438 0 3.42 3.42 0 001.946.806 3.42 3.42 0 013.138 3.138 3.42 3.42 0 00.806 1.946 3.42 3.42 0 010 4.438 3.42 3.42 0 00-.806 1.946 3.42 3.42 0 01-3.138 3.138 3.42 3.42 0 00-1.946.806 3.42 3.42 0 01-4.438 0 3.42 3.42 0 00-1.946-.806 3.42 3.42 0 01-3.138-3.138 3.42 3.42 0 00-.806-1.946 3.42 3.42 0 010-4.438 3.42 3.42 0 00.806-1.946 3.42 3.42 0 013.138-3.138z" />
					</svg>
				</div>
				<div class="space-y-0.5">
					<p class="text-xs font-black text-zinc-800 dark:text-zinc-200 leading-snug">Rank {activeProfile.rank}</p>
					<p class="text-[10px] text-zinc-400 dark:text-zinc-500 font-semibold">Of 250 Indian Cities</p>
				</div>
				<span class="text-[9px] font-extrabold uppercase text-zinc-450 dark:text-zinc-550 leading-none">
					{activeAQI <= 50 ? 'Top 5% clean' : activeAQI <= 100 ? 'Top 35% clean' : 'Lower 40% rank'}
				</span>
			</div>

			<!-- Widget 6: Live Connection Calibrated status -->
			<div class="bg-white/40 dark:bg-zinc-900/40 border border-white/20 dark:border-zinc-800/80 backdrop-blur-xl rounded-2xl p-4 shadow-sm space-y-2.5 flex flex-col justify-between hover:shadow hover:border-emerald-500/20 dark:hover:border-zinc-700 transition-all duration-300">
				<div class="flex items-center justify-between text-zinc-400">
					<span class="text-[9px] font-bold uppercase tracking-wider">Sync Status</span>
					<svg class="h-4.5 w-4.5 text-emerald-500" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
						<path stroke-linecap="round" stroke-linejoin="round" d="M9 3v2m6-2v2M9 19v2m6-2v2M5 9H3m2 6H3m18-6h-2m2 6h-2M7 19h10a2 2 0 002-2V7a2 2 0 00-2-2H7a2 2 0 00-2 2v10a2 2 0 002 2zM9 9h6v6H9V9z" />
					</svg>
				</div>
				<div class="space-y-0.5">
					<p class="text-xs font-black text-zinc-800 dark:text-zinc-200 leading-snug">{activeProfile.liveStatus}</p>
					<p class="text-[10px] text-zinc-400 dark:text-zinc-500 font-semibold">Secured (TLS v1.3)</p>
				</div>
				<span class="text-[9px] font-extrabold text-emerald-500 uppercase tracking-wider leading-none">
					Latency: 24ms
				</span>
			</div>

		</div>
	</div>

	<!-- ==================== SECTION 5 & 6: Trend & Forecast Preview ==================== -->
	<div class="grid grid-cols-1 lg:grid-cols-2 gap-6 z-10 relative items-stretch">
		<!-- 24-Hour Trend -->
		<div class="flex flex-col h-full items-stretch">
			{#if TrendChart}
				<TrendChart baseAqi={activeAQI} />
			{:else}
				<div class="h-full min-h-[400px] animate-pulse bg-zinc-200/50 dark:bg-zinc-800/20 border border-zinc-200/40 dark:border-zinc-800/40 rounded-2xl"></div>
			{/if}
		</div>
		<!-- 7-Day Forecast -->
		<div class="flex flex-col h-full items-stretch">
			{#if ForecastPreview}
				<ForecastPreview baseAqi={activeAQI} />
			{:else}
				<div class="h-full min-h-[400px] animate-pulse bg-zinc-200/50 dark:bg-zinc-800/20 border border-zinc-200/40 dark:border-zinc-800/40 rounded-2xl"></div>
			{/if}
		</div>
	</div>

	<!-- ==================== SECTION 7: Health Recommendations ==================== -->
	<div class="space-y-4 z-10 relative animate-slide-up">
		<h3 class="text-xs font-bold text-zinc-400 dark:text-zinc-500 uppercase tracking-wider">Health Recommendations</h3>
		<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
			{#each activeProfile.health as advice}
				<HealthCard
					icon={advice.icon}
					title={advice.title}
					description={advice.description}
					type={advice.type}
					priority={advice.priority}
					suggestedAction={advice.action}
				/>
			{/each}
		</div>
	</div>

	<!-- ==================== SECTION 8: Quick Stats ==================== -->
	<div class="grid grid-cols-2 lg:grid-cols-4 gap-4 z-10 relative">
		<StatsCard title="Cities Monitored" value="250+" trend="+8 this week" trendType="up" icon="cities" />
		<StatsCard title="Prediction Accuracy" value="94.2%" trend="+0.4% since v1.2" trendType="up" icon="accuracy" />
		<StatsCard title="Alerts Sent" value="1,280" trend="-12% vs yesterday" trendType="down" icon="alerts" />
		<StatsCard title="Air Quality Rank" value="#18" trend="Top 10% clean globally" trendType="neutral" icon="rank" />
	</div>

	<!-- ==================== SECTION 9: Footer Banner ==================== -->
	<div class="relative overflow-hidden bg-gradient-to-br from-emerald-500/10 to-teal-500/5 dark:from-emerald-950/20 dark:to-transparent border border-emerald-500/10 dark:border-zinc-800/80 rounded-2xl p-6 shadow-sm flex flex-col md:flex-row items-center justify-between gap-4 z-10 relative">
		<!-- Leaf background SVGs for eco-theme details -->
		<div class="absolute -bottom-10 -right-10 h-32 w-32 text-emerald-500/10 opacity-30 select-none pointer-events-none">
			<svg class="h-full w-full" fill="currentColor" viewBox="0 0 24 24">
				<path d="M17 8C8 10 9 21 9 21s11-1 12-10c.5-4.5-3.5-3.5-4-3zm-6 7.5c-3-1.5-4.5-5.5-4.5-5.5S11.5 9 13.5 12c1 1.5-1 2.5-2.5 1.5z" />
			</svg>
		</div>

		<div class="flex items-center gap-4 text-center md:text-left">
			<div class="h-12 w-12 rounded-xl bg-emerald-500 text-white flex items-center justify-center shadow-md shadow-emerald-500/20 shrink-0">
				<svg class="h-6 w-6" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
					<path stroke-linecap="round" stroke-linejoin="round" d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364-6.364l-.707.707M6.343 17.657l-.707.707m0-12.728l.707.707m12.728 12.728l.707-.707M12 8a4 4 0 100 8 4 4 0 000-8z" />
				</svg>
			</div>
			<div class="space-y-0.5">
				<h4 class="text-sm font-black text-zinc-950 dark:text-white">Breathe Better. Live Better.</h4>
				<p class="text-xs text-zinc-500 dark:text-zinc-400">Join over 10,000+ citizens securing live updates, and secure your health.</p>
			</div>
		</div>
		<button class="px-4.5 py-2.5 bg-emerald-500 hover:bg-emerald-600 active:scale-95 text-white text-xs font-bold rounded-xl shadow-md shadow-emerald-500/10 focus:outline-none transition-all">
			Join Newsletter
		</button>
	</div>
</div>

<style>
	/* Global fade-in and slide-up animations */
	.animate-fade-in {
		animation: fadeIn 0.6s cubic-bezier(0.4, 0, 0.2, 1) forwards;
	}

	.animate-slide-up {
		animation: slideUp 0.6s cubic-bezier(0.4, 0, 0.2, 1) forwards;
	}

	.animate-scale-up {
		animation: scaleUp 0.4s cubic-bezier(0.34, 1.56, 0.64, 1) forwards;
	}

	@keyframes fadeIn {
		from {
			opacity: 0;
		}
		to {
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
</style>
