<script lang="ts">
	import ForecastCard from './ForecastCard.svelte';

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
		if (aqiVal <= 50) return 'Good day for outdoor activity.';
		if (aqiVal <= 100) return 'Ventilation recommended.';
		if (aqiVal <= 150) return 'Sensitive groups use caution.';
		if (aqiVal <= 200) return 'Reduce outdoor exercise.';
		return 'Stay indoors to avoid exposure.';
	}
</script>

<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-6 select-none relative animate-slide-up">
	{#each forecastItems as item, idx}
		<ForecastCard
			day={item.day}
			date={item.date}
			aqi={item.aqi}
			category={item.aqi_category}
			color={item.aqi_color}
			weatherIcon={item.weather_icon}
			tempHigh={item.temp_high || Math.round(item.temperature + 3)}
			tempLow={item.temp_low || Math.round(item.temperature - 4)}
			humidity={item.humidity}
			windSpeed={item.wind_speed}
			rainChance={item.rain_chance !== undefined ? item.rain_chance : Math.round(item.chance_of_improvement / 2)}
			sunrise={item.sunrise || '5:42 AM'}
			sunset={item.sunset || '7:11 PM'}
			trendDirection={item.trend_direction}
			healthMessage={item.health_advice || getHealthMessage(item.aqi)}
			isSelected={selectedIndex === idx}
			onclick={() => onselect(idx)}
		/>
	{/each}
</div>
