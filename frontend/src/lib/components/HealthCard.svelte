<script>
	// Props using Svelte 5 runes
	let {
		icon = 'mask',
		title = 'Wear Mask Outdoors',
		description = 'Vulnerable individuals should wear N95 masks during heavy pollution spikes.',
		type = 'warning', // warning, success, info
		priority = 'High Priority',
		suggestedAction = 'Wear a tight-fitting N95 respirator mask whenever you step outside.'
	} = $props();

	// Select colors based on advice type
	let typeStyles = $derived.by(() => {
		if (type === 'warning') {
			return {
				bg: 'bg-white/40 dark:bg-zinc-900/40 text-red-700 dark:text-red-400 border-red-500/10 dark:border-red-900/20 hover:border-red-500/20',
				iconBg: 'bg-red-500/10 dark:bg-red-900/40 text-red-500',
				priorityBg: 'bg-red-100 dark:bg-red-950/40 text-red-700 dark:text-red-400'
			};
		} else if (type === 'success') {
			return {
				bg: 'bg-white/40 dark:bg-zinc-900/40 text-emerald-700 dark:text-emerald-400 border-emerald-500/10 dark:border-emerald-900/20 hover:border-emerald-500/20',
				iconBg: 'bg-emerald-500/10 dark:bg-emerald-900/40 text-emerald-500',
				priorityBg: 'bg-emerald-100 dark:bg-emerald-950/40 text-emerald-700 dark:text-emerald-400'
			};
		} else {
			return {
				bg: 'bg-white/40 dark:bg-zinc-900/40 text-blue-700 dark:text-blue-400 border-blue-500/10 dark:border-blue-900/20 hover:border-blue-500/20',
				iconBg: 'bg-blue-500/10 dark:bg-blue-900/40 text-blue-500',
				priorityBg: 'bg-blue-100 dark:bg-blue-950/40 text-blue-700 dark:text-blue-400'
			};
		}
	});
</script>

<div class="flex flex-col justify-between p-5 rounded-2xl border backdrop-blur-xl shadow-sm transition-all duration-300 hover:shadow-md hover:-translate-y-0.5 hover:bg-white/50 dark:hover:bg-zinc-900/60 {typeStyles.bg}">
	<div class="flex gap-4">
		<!-- Icon Bubble -->
		<div class="h-10 w-10 rounded-xl flex items-center justify-center shrink-0 shadow-sm {typeStyles.iconBg}">
			{#if icon === 'mask'}
				<svg class="h-5.5 w-5.5" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
					<path stroke-linecap="round" stroke-linejoin="round" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" />
				</svg>
			{:else if icon === 'water'}
				<svg class="h-5.5 w-5.5" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
					<path stroke-linecap="round" stroke-linejoin="round" d="M20 13V6a2 2 0 00-2-2H6a2 2 0 00-2 2v7m16 0a2 2 0 01-2 2H6a2 2 0 01-2-2m16 0V9a2 2 0 00-2-2H6a2 2 0 00-2 2v4h16z" />
					<path stroke-linecap="round" stroke-linejoin="round" d="M12 17c-1.1 0-2-.9-2-2h4c0 1.1-.9 2-2 2z" />
				</svg>
			{:else if icon === 'windows'}
				<svg class="h-5.5 w-5.5" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
					<path stroke-linecap="round" stroke-linejoin="round" d="M4 5a1 1 0 011-1h14a1 1 0 011 1v14a1 1 0 01-1 1H5a1 1 0 01-1-1V5zm8-1v16M4 12h16" />
				</svg>
			{:else if icon === 'exercise'}
				<svg class="h-5.5 w-5.5" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
					<path stroke-linecap="round" stroke-linejoin="round" d="M13 10V3L4 14h7v7l9-11h-7z" />
				</svg>
			{:else}
				<svg class="h-5.5 w-5.5" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
					<path stroke-linecap="round" stroke-linejoin="round" d="M13 16V6a1 1 0 00-1-1H4a1 1 0 00-1 1v10a1 1 0 001 1h8a1 1 0 001-1z" />
					<path stroke-linecap="round" stroke-linejoin="round" d="M12 9h4m-4 4h4" />
				</svg>
			{/if}
		</div>

		<!-- Text Area -->
		<div class="space-y-1.5">
			<!-- Priority Pill -->
			<span class="inline-block text-[9px] font-bold px-2 py-0.5 rounded-full {typeStyles.priorityBg}">
				{priority}
			</span>
			<h4 class="text-sm font-black text-zinc-950 dark:text-white leading-snug">{title}</h4>
			<p class="text-xs text-zinc-500 dark:text-zinc-400 leading-relaxed font-semibold">{description}</p>
		</div>
	</div>

	<!-- Suggested Action Section -->
	<div class="mt-4 pt-3 border-t border-zinc-200/40 dark:border-zinc-800/45 text-[11px] text-zinc-650 dark:text-zinc-300 leading-snug font-bold">
		<span class="text-[9px] font-black uppercase text-emerald-500 tracking-wider block mb-0.5">Suggested Action:</span>
		{suggestedAction}
	</div>
</div>
