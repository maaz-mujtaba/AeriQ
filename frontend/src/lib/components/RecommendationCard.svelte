<script>
	let {
		aqi = 82,
		category = 'Moderate'
	} = $props();

	// Derived advisors based on active AQI/category
	let adviceDetails = $derived.by(() => {
		const val = aqi;
		const cat = category.toLowerCase();
		
		if (val <= 50 || cat === 'good') {
			return {
				level: 'Minimal Risk',
				general: 'Excellent air quality. Perfect for outdoor activities.',
				outdoor: 'Fully recommended. Great day to spend time outside.',
				mask: 'Not needed. Safe to breathe standard outdoor air.',
				exercise: 'Approved. Enjoy heavy runs or cardiovascular training.',
				sensitive: 'No advisory. Safe for all demographic groups.',
				color: '#10b981',
				bgClass: 'bg-emerald-500/10 text-emerald-705 dark:text-emerald-400 border-emerald-500/20',
				iconColorClass: 'text-emerald-500',
				indicatorClass: 'bg-emerald-500'
			};
		} else if (val <= 100 || cat === 'moderate' || cat === 'satisfactory') {
			return {
				level: 'Low/Moderate Risk',
				general: 'Sensitive groups should reduce prolonged outdoor exposure.',
				outdoor: 'Safe for most. Sensitive individuals should monitor throat indices.',
				mask: 'Optional. Wear standard masks if sensitive to dust.',
				exercise: 'Brisk walk approved. Keep away from highway lanes.',
				sensitive: 'Caution advised. Asthmatic users should hold inhalers.',
				color: '#f59e0b',
				bgClass: 'bg-amber-500/10 text-amber-705 dark:text-amber-400 border-amber-500/20',
				iconColorClass: 'text-amber-500',
				indicatorClass: 'bg-amber-500'
			};
		} else if (val <= 200 || cat === 'poor' || cat === 'moderate_poor') {
			return {
				level: 'Elevated Risk',
				general: 'Wear a mask outdoors. Reduce physical activity.',
				outdoor: 'Limit exposure. Stay inside during peak smog periods.',
				mask: 'Recommended. Equip standard N95 particulate mask before exit.',
				exercise: 'Reduced. Perform stretching and warmups inside.',
				sensitive: 'High alert. Children and elderly should remain in indoor zones.',
				color: '#ef4444',
				bgClass: 'bg-orange-500/10 text-orange-755 dark:text-orange-400 border-orange-500/20',
				iconColorClass: 'text-orange-500',
				indicatorClass: 'bg-orange-500'
			};
		} else if (val <= 300 || cat === 'very_poor' || cat === 'very poor') {
			return {
				level: 'Severe Risk',
				general: 'Avoid outdoor activities. Keep windows closed.',
				outdoor: 'Avoid exposure. Carry out operations from indoor spaces.',
				mask: 'Mandatory. Tight-fitting N95 mask required for any exit.',
				exercise: 'Strictly prohibited outdoors. Restrict to light indoor activities.',
				sensitive: 'Hazard warning. Sensitive users must stay in purified air settings.',
				color: '#a855f7',
				bgClass: 'bg-red-500/10 text-red-700 dark:text-red-400 border-red-500/20',
				iconColorClass: 'text-red-500',
				indicatorClass: 'bg-red-500'
			};
		} else {
			// Hazardous / Severe / 300+
			return {
				level: 'Hazardous Danger',
				general: 'Stay indoors. Use an air purifier if available.',
				outdoor: 'Avoid completely. Stay locked indoors.',
				mask: 'Critical. Do not step out without heavy respiratory shields.',
				exercise: 'No exercise. Relax and rest indoors to conserve clean lung volume.',
				sensitive: 'Emergency status. Keep air purifiers at maximum speed.',
				color: '#881337',
				bgClass: 'bg-rose-950/20 text-rose-800 dark:text-rose-450 border-rose-900/20',
				iconColorClass: 'text-rose-600 dark:text-rose-400',
				indicatorClass: 'bg-rose-900'
			};
		}
	});
</script>

<div class="relative overflow-hidden bg-white/40 dark:bg-zinc-900/40 border border-white/20 dark:border-zinc-800/80 backdrop-blur-xl rounded-2xl p-6 shadow-md transition-all duration-300 flex flex-col justify-between h-full min-h-[300px]">
	<!-- Ambient top right card background glow -->
	<div
		class="absolute -top-12 -right-12 h-24 w-24 rounded-full blur-3xl opacity-20 pointer-events-none transition-all duration-300"
		style="background-color: {adviceDetails.color};"
	></div>

	<div class="space-y-4">
		<!-- Header -->
		<div class="space-y-1">
			<span class="text-xs font-bold text-zinc-400 dark:text-zinc-500 uppercase tracking-wider">Environmental Intelligence</span>
			<h3 class="text-lg font-black text-zinc-900 dark:text-white">Health Advisory</h3>
		</div>

		<!-- Risk Level Banner -->
		<div class="flex items-center gap-2 p-2 px-3.5 rounded-xl text-xs font-extrabold uppercase tracking-wide border {adviceDetails.bgClass}">
			<span class="h-2 w-2 rounded-full animate-ping shrink-0 {adviceDetails.indicatorClass}"></span>
			Risk Factor: {adviceDetails.level} (AQI {aqi})
		</div>

		<!-- General Advice (Section 7) -->
		<div class="p-3 bg-white/50 dark:bg-zinc-800/10 border border-zinc-200/40 dark:border-zinc-800/40 rounded-xl space-y-1">
			<span class="text-[9px] font-black uppercase text-emerald-500 tracking-wider">Health Recommendations</span>
			<p class="text-sm font-black text-zinc-900 dark:text-white">{adviceDetails.general}</p>
		</div>

		<!-- Multi Advisory Breakdown (Section 1 Card 3) -->
		<div class="grid grid-cols-1 xs:grid-cols-2 gap-2 text-xs">
			<div class="p-2.5 bg-white/40 dark:bg-zinc-800/5 border border-zinc-250/20 dark:border-zinc-850 rounded-xl space-y-0.5">
				<p class="text-zinc-400 dark:text-zinc-550 font-bold uppercase text-[8px] tracking-wider leading-none">Outdoor Activity</p>
				<p class="font-extrabold text-zinc-850 dark:text-zinc-200 leading-snug">{adviceDetails.outdoor}</p>
			</div>

			<div class="p-2.5 bg-white/40 dark:bg-zinc-800/5 border border-zinc-250/20 dark:border-zinc-850 rounded-xl space-y-0.5">
				<p class="text-zinc-400 dark:text-zinc-550 font-bold uppercase text-[8px] tracking-wider leading-none">Mask Advice</p>
				<p class="font-extrabold text-zinc-850 dark:text-zinc-200 leading-snug">{adviceDetails.mask}</p>
			</div>

			<div class="p-2.5 bg-white/40 dark:bg-zinc-800/5 border border-zinc-250/20 dark:border-zinc-850 rounded-xl space-y-0.5">
				<p class="text-zinc-400 dark:text-zinc-550 font-bold uppercase text-[8px] tracking-wider leading-none">Exercise Limits</p>
				<p class="font-extrabold text-zinc-850 dark:text-zinc-200 leading-snug">{adviceDetails.exercise}</p>
			</div>

			<div class="p-2.5 bg-white/40 dark:bg-zinc-800/5 border border-zinc-250/20 dark:border-zinc-850 rounded-xl space-y-0.5">
				<p class="text-zinc-400 dark:text-zinc-550 font-bold uppercase text-[8px] tracking-wider leading-none">Vulnerable Groups</p>
				<p class="font-extrabold text-zinc-850 dark:text-zinc-200 leading-snug">{adviceDetails.sensitive}</p>
			</div>
		</div>
	</div>
</div>
