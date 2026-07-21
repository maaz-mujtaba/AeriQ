<script>
	import { login } from '$lib/stores/authStore.js';

	// Props using Svelte 5 runes
	let {
		title = 'Dashboard Page',
		description = 'This segment requires an authorized account to access active telemetry streams.'
	} = $props();
</script>

<div class="space-y-6 animate-fade-in max-w-2xl mx-auto mt-8 select-none">
	<!-- Breadcrumbs and Header -->
	<div class="space-y-1">
		<div class="flex items-center gap-2 text-xs font-semibold text-zinc-455 dark:text-zinc-500 uppercase tracking-wider">
			<span>Security Gate</span>
			<span>/</span>
			<span class="text-rose-500 dark:text-rose-400">Authorization Required</span>
		</div>
		<h1 class="text-2xl sm:text-3xl font-black tracking-tight text-zinc-900 dark:text-white">
			{title}
		</h1>
		<p class="text-xs sm:text-sm font-semibold text-zinc-500 dark:text-zinc-400">
			Please sign in to unlock premium modules and personal trackers.
		</p>
	</div>

	<!-- Lock card block -->
	<div class="bg-white/40 dark:bg-zinc-900/40 border border-white/20 dark:border-zinc-805/85 backdrop-blur-xl rounded-2xl p-8 md:p-12 shadow-md flex flex-col items-center justify-center text-center min-h-[350px] gap-5 transition-all relative overflow-hidden">
		<!-- Blurred backing green glow -->
		<div class="absolute -top-16 -right-16 h-36 w-36 rounded-full bg-emerald-500/10 blur-3xl opacity-30 pointer-events-none"></div>

		<!-- Animated Lock SVG illustration -->
		<div class="h-16 w-16 rounded-2xl bg-rose-500/10 text-rose-550 flex items-center justify-center shadow-inner relative group select-none">
			<svg class="h-8 w-8 text-rose-500 transition-transform duration-300 group-hover:scale-110" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
				<path stroke-linecap="round" stroke-linejoin="round" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
			</svg>
		</div>

		<div class="max-w-md space-y-2">
			<h2 class="text-xl font-black text-zinc-900 dark:text-white">Sign In to Continue</h2>
			<p class="text-xs sm:text-sm font-medium text-zinc-500 dark:text-zinc-400 leading-relaxed">
				{description}
			</p>
		</div>

		<!-- Action triggers -->
		<div class="flex items-center gap-3 mt-2 flex-wrap justify-center">
			<button
				onclick={login}
				class="px-5 py-2.5 bg-emerald-500 hover:bg-emerald-600 active:scale-95 text-white text-xs font-bold rounded-xl shadow-md shadow-emerald-500/10 focus:outline-none transition-all flex items-center gap-1.5"
			>
				<svg class="h-4 w-4" fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24">
					<path stroke-linecap="round" stroke-linejoin="round" d="M11 16l-4-4m0 0l4-4m-4 4h14m-5 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
				</svg>
				Sign In Now
			</button>
		</div>
	</div>
</div>
