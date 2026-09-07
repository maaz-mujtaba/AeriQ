<script>
	import { login } from '$lib/stores/authStore.js';

	// Props using Svelte 5 runes
	let {
		title = 'Dashboard Page',
		description = 'This segment requires an authorized account to access active telemetry streams.'
	} = $props();

	// Auth mode switcher: 'login' | 'signup' | 'forgot'
	let authMode = $state('login');
	let resetSent = $state(false);
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
			{#if authMode === 'signup'}
				Please create an account to unlock premium modules and personal trackers.
			{:else if authMode === 'forgot'}
				Recover access to your account with a secure password reset link.
			{:else}
				Please sign in to unlock premium modules and personal trackers.
			{/if}
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

		<!-- Auth Mode Tabs -->
		<div class="flex items-center gap-1 p-1 bg-zinc-100 dark:bg-zinc-800/70 border border-zinc-200/60 dark:border-zinc-700/60 rounded-xl">
			<button
				type="button"
				onclick={() => { authMode = 'login'; resetSent = false; }}
				class="px-3 py-1.5 text-xs font-bold rounded-lg transition-all {authMode === 'login' ? 'bg-white dark:bg-zinc-900 text-zinc-900 dark:text-white shadow-sm' : 'text-zinc-500 dark:text-zinc-400 hover:text-zinc-900 dark:hover:text-zinc-200'}"
			>
				Sign In
			</button>
			<button
				type="button"
				onclick={() => { authMode = 'signup'; resetSent = false; }}
				class="px-3 py-1.5 text-xs font-bold rounded-lg transition-all {authMode === 'signup' ? 'bg-white dark:bg-zinc-900 text-zinc-900 dark:text-white shadow-sm' : 'text-zinc-500 dark:text-zinc-400 hover:text-zinc-900 dark:hover:text-zinc-200'}"
			>
				Sign Up
			</button>
			<button
				type="button"
				onclick={() => { authMode = 'forgot'; resetSent = false; }}
				class="px-3 py-1.5 text-xs font-bold rounded-lg transition-all {authMode === 'forgot' ? 'bg-white dark:bg-zinc-900 text-zinc-900 dark:text-white shadow-sm' : 'text-zinc-500 dark:text-zinc-400 hover:text-zinc-900 dark:hover:text-zinc-200'}"
			>
				Forgot Password
			</button>
		</div>

		<!-- Mode Content -->
		{#if authMode === 'login'}
			<div class="max-w-md space-y-2">
				<h2 class="text-xl font-black text-zinc-900 dark:text-white">Sign In to Continue</h2>
				<p class="text-xs sm:text-sm font-medium text-zinc-500 dark:text-zinc-400 leading-relaxed">
					{description}
				</p>
			</div>

			<!-- Action triggers -->
			<div class="flex flex-col items-center gap-3 mt-2">
				<button
					type="button"
					onclick={login}
					class="px-5 py-2.5 bg-emerald-500 hover:bg-emerald-600 active:scale-95 text-white text-xs font-bold rounded-xl shadow-md shadow-emerald-500/10 focus:outline-none transition-all flex items-center gap-1.5"
				>
					<svg class="h-4 w-4" fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24">
						<path stroke-linecap="round" stroke-linejoin="round" d="M11 16l-4-4m0 0l4-4m-4 4h14m-5 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013 3v1" />
					</svg>
					Sign In Now
				</button>
				<div class="flex items-center gap-3 text-xs">
					<button
						type="button"
						onclick={() => { authMode = 'signup'; resetSent = false; }}
						class="font-semibold text-emerald-600 dark:text-emerald-400 hover:underline"
					>
						Don't have an account? Sign Up
					</button>
					<span class="text-zinc-300 dark:text-zinc-700">•</span>
					<button
						type="button"
						onclick={() => { authMode = 'forgot'; resetSent = false; }}
						class="text-zinc-500 dark:text-zinc-400 hover:text-zinc-900 dark:hover:text-white transition-colors"
					>
						Forgot Password?
					</button>
				</div>
			</div>
		{:else if authMode === 'signup'}
			<div class="max-w-md space-y-2">
				<h2 class="text-xl font-black text-zinc-900 dark:text-white">Create an Account</h2>
				<p class="text-xs sm:text-sm font-medium text-zinc-500 dark:text-zinc-400 leading-relaxed">
					Register with AeriQ to unlock customized air pollution warnings, multi-city tracking, and personalized telemetry.
				</p>
			</div>

			<!-- Action triggers -->
			<div class="flex flex-col items-center gap-3 mt-2">
				<button
					type="button"
					onclick={login}
					class="px-5 py-2.5 bg-emerald-500 hover:bg-emerald-600 active:scale-95 text-white text-xs font-bold rounded-xl shadow-md shadow-emerald-500/10 focus:outline-none transition-all flex items-center gap-1.5"
				>
					<svg class="h-4 w-4" fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24">
						<path stroke-linecap="round" stroke-linejoin="round" d="M18 9v3m0 0v3m0-3h3m-3 0h-3m-2-5a4 4 0 11-8 0 4 4 0 018 0zM3 20a6 6 0 0112 0v1H3v-1z" />
					</svg>
					Sign Up Now
				</button>
				<button
					type="button"
					onclick={() => { authMode = 'login'; resetSent = false; }}
					class="text-xs font-semibold text-emerald-600 dark:text-emerald-400 hover:underline"
				>
					Already have an account? Sign In
				</button>
			</div>
		{:else if authMode === 'forgot'}
			<div class="max-w-md space-y-2">
				<h2 class="text-xl font-black text-zinc-900 dark:text-white">Reset Password</h2>
				<p class="text-xs sm:text-sm font-medium text-zinc-500 dark:text-zinc-400 leading-relaxed">
					{#if resetSent}
						We have sent password reset instructions to your registered email address.
					{:else}
						Enter your email to receive secure recovery instructions and reset your account password.
					{/if}
				</p>
			</div>

			<!-- Action triggers -->
			<div class="flex flex-col items-center gap-3 mt-2">
				{#if resetSent}
					<div class="flex items-center gap-2 px-4 py-2 bg-emerald-50 dark:bg-emerald-950/40 text-emerald-700 dark:text-emerald-300 rounded-xl text-xs font-semibold border border-emerald-200 dark:border-emerald-800">
						<svg class="h-4 w-4" fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24">
							<path stroke-linecap="round" stroke-linejoin="round" d="M5 13l4 4L19 7" />
						</svg>
						Reset link dispatched successfully
					</div>
				{:else}
					<button
						type="button"
						onclick={() => (resetSent = true)}
						class="px-5 py-2.5 bg-emerald-500 hover:bg-emerald-600 active:scale-95 text-white text-xs font-bold rounded-xl shadow-md shadow-emerald-500/10 focus:outline-none transition-all flex items-center gap-1.5"
					>
						<svg class="h-4 w-4" fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24">
							<path stroke-linecap="round" stroke-linejoin="round" d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
						</svg>
						Send Reset Link
					</button>
				{/if}
				<button
					type="button"
					onclick={() => { authMode = 'login'; resetSent = false; }}
					class="text-xs font-semibold text-emerald-600 dark:text-emerald-400 hover:underline"
				>
					Back to Sign In
				</button>
			</div>
		{/if}
	</div>
</div>
