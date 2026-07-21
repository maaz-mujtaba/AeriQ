<script>
	import { untrack } from 'svelte';

	let { aqi = 0 } = $props();

	// Arc measurements
	const radius = 40;
	const circumference = Math.PI * radius; // ~125.66

	// Count-up animation state
	let displayAQI = $state(0);

	$effect(() => {
		const end = aqi;
		const start = untrack(() => displayAQI);
		const duration = 1000; // ms
		
		/** @type {number | null} */
		let startTime = null;
		/** @type {number | null} */
		let animId = null;

		/** @param {number} timestamp */
		function animate(timestamp) {
			if (startTime === null) startTime = timestamp;
			const elapsed = timestamp - startTime;
			const progress = Math.min(elapsed / duration, 1);
			const ease = progress * (2 - progress); // easeOutQuad
			displayAQI = Math.round(start + (end - start) * ease);

			if (progress < 1) {
				animId = requestAnimationFrame(animate);
			}
		}
		animId = requestAnimationFrame(animate);

		return () => {
			if (animId !== null) cancelAnimationFrame(animId);
		};
	});

	// Derive properties based on active AQI rating
	let statusInfo = $derived.by(() => {
		if (aqi <= 50) {
			return {
				colorClass: 'text-emerald-500 dark:text-emerald-400',
				strokeColor: '#10b981',
				bgColor: 'bg-emerald-500/10',
				label: 'Good',
				desc: 'Air quality is satisfactory, and air pollution poses little or no risk.'
			};
		} else if (aqi <= 100) {
			return {
				colorClass: 'text-amber-500 dark:text-amber-400',
				strokeColor: '#f59e0b',
				bgColor: 'bg-amber-500/10',
				label: 'Moderate',
				desc: 'Air quality is acceptable; however, there may be risk for some people.'
			};
		} else if (aqi <= 150) {
			return {
				colorClass: 'text-orange-500 dark:text-orange-400',
				strokeColor: '#f97316',
				bgColor: 'bg-orange-500/10',
				label: 'Sensitive Warning',
				desc: 'Members of sensitive groups may experience health effects.'
			};
		} else if (aqi <= 200) {
			return {
				colorClass: 'text-red-500 dark:text-red-400',
				strokeColor: '#ef4444',
				bgColor: 'bg-red-500/10',
				label: 'Unhealthy',
				desc: 'Everyone may begin to experience health effects; sensitive groups may experience more serious health effects.'
			};
		} else if (aqi <= 300) {
			return {
				colorClass: 'text-purple-500 dark:text-purple-400',
				strokeColor: '#a855f7',
				bgColor: 'bg-purple-500/10',
				label: 'Very Unhealthy',
				desc: 'Health alert: Everyone may experience more serious health effects.'
			};
		} else {
			return {
				colorClass: 'text-rose-900 dark:text-rose-400',
				strokeColor: '#881337',
				bgColor: 'bg-rose-950/20',
				label: 'Hazardous',
				desc: 'Health warning of emergency conditions: Everyone is more likely to be affected.'
			};
		}
	});

	// Map AQI to progress percentage (0 - 500)
	let progressPercentage = $derived(Math.min(Math.max(aqi, 0), 500) / 500);
	// Invert because offset measures remaining space
	let strokeOffset = $derived(circumference * (1 - progressPercentage));
</script>

<div class="flex flex-col items-center justify-center p-2 select-none">
	<div class="relative w-44 h-28 flex items-center justify-center">
		<!-- SVG Gauge -->
		<svg class="w-full h-full" viewBox="0 0 100 65">
			<!-- Background Track -->
			<path
				d="M 10 50 A 40 40 0 0 1 90 50"
				fill="none"
				stroke="currentColor"
				class="text-zinc-100 dark:text-zinc-800/80"
				stroke-width="7"
				stroke-linecap="round"
			/>
			<!-- Animated Progress Arc -->
			<path
				d="M 10 50 A 40 40 0 0 1 90 50"
				fill="none"
				stroke={statusInfo.strokeColor}
				stroke-width="7.5"
				stroke-linecap="round"
				stroke-dasharray={circumference}
				stroke-dashoffset={strokeOffset}
				class="transition-all duration-1000 ease-out"
			/>
		</svg>

		<!-- Center text overlay -->
		<div class="absolute bottom-1 flex flex-col items-center text-center">
			<span class="text-3xl font-extrabold tracking-tight text-zinc-900 dark:text-white leading-none">
				{displayAQI}
			</span>
			<span class="text-[10px] font-bold mt-1.5 px-2 py-0.5 rounded-full {statusInfo.bgColor} {statusInfo.colorClass}">
				{statusInfo.label}
			</span>
		</div>
	</div>

	<!-- Info Description block below gauge -->
	<p class="text-[10px] text-center text-zinc-400 dark:text-zinc-500 font-semibold px-4 mt-1 leading-relaxed">
		{statusInfo.desc}
	</p>
</div>
