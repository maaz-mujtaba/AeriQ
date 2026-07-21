<script>
	import { loggedIn, login, logout } from '$lib/stores/authStore.js';
	import { goto } from '$app/navigation';

	// Props using Svelte 5 bindable runes
	let {
		isCollapsed = $bindable(false),
		isMobileOpen = $bindable(false)
	} = $props();

	// Dropdown states
	let isCityDropdownOpen = $state(false);
	let isNotificationOpen = $state(false);
	let isUserDropdownOpen = $state(false);
	let currentCity = $state('New Delhi, India');

	const mockCities = [
		'New Delhi, India',
		'New York, USA',
		'London, UK',
		'Tokyo, Japan',
		'Sydney, Australia'
	];

	const mockNotifications = [
		{ id: 1, text: 'AQI in New Delhi has reached 185 (Unhealthy)', time: '10m ago', type: 'warning' },
		{ id: 2, text: 'Weekly air quality report is ready to download', time: '1h ago', type: 'info' },
		{ id: 3, text: 'Alert: High ozone levels forecast for tomorrow', time: '5h ago', type: 'alert' }
	];

	/**
	 * @param {MouseEvent} e
	 */
	function toggleCityDropdown(e) {
		e.stopPropagation();
		isCityDropdownOpen = !isCityDropdownOpen;
		isNotificationOpen = false;
		isUserDropdownOpen = false;
	}

	/**
	 * @param {MouseEvent} e
	 */
	function toggleNotificationDropdown(e) {
		e.stopPropagation();
		isNotificationOpen = !isNotificationOpen;
		isCityDropdownOpen = false;
		isUserDropdownOpen = false;
	}

	/**
	 * @param {MouseEvent} e
	 */
	function toggleUserDropdown(e) {
		e.stopPropagation();
		isUserDropdownOpen = !isUserDropdownOpen;
		isCityDropdownOpen = false;
		isNotificationOpen = false;
	}

	/**
	 * @param {string} city
	 */
	function selectCity(city) {
		currentCity = city;
		isCityDropdownOpen = false;
	}

	function closeAllDropdowns() {
		isCityDropdownOpen = false;
		isNotificationOpen = false;
		isUserDropdownOpen = false;
	}

	function handleSignIn() {
		login();
	}

	function handleLogout() {
		logout();
		isUserDropdownOpen = false;
		goto('/dashboard');
	}
</script>

<svelte:window onclick={closeAllDropdowns} />

<header class="sticky top-0 right-0 z-30 h-16 flex items-center justify-between px-4 lg:px-6 bg-white/80 dark:bg-zinc-950/80 backdrop-blur-md border-b border-zinc-200/80 dark:border-zinc-800/80 transition-colors duration-300">
	<!-- Left: Hamburger & Search -->
	<div class="flex items-center gap-3 md:gap-4 flex-1">
		<!-- Sidebar Toggle Button -->
		<button
			onclick={(e) => {
				e.stopPropagation();
				// Mobile toggles drawer, Tablet/Desktop collapses
				if (window.innerWidth < 1024) {
					isMobileOpen = !isMobileOpen;
				} else {
					isCollapsed = !isCollapsed;
				}
			}}
			class="p-2 rounded-xl text-zinc-500 dark:text-zinc-400 hover:text-zinc-950 dark:hover:text-zinc-50 hover:bg-zinc-100 dark:hover:bg-zinc-900 transition-all duration-150 focus:outline-none"
			aria-label="Toggle sidebar"
		>
			<svg class="h-5 w-5" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
				<path stroke-linecap="round" stroke-linejoin="round" d="M4 6h16M4 12h16M4 18h16" />
			</svg>
		</button>

		<!-- Search Input (Desktop/Tablet) -->
		<div class="relative max-w-md w-full hidden sm:block">
			<div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
				<svg class="h-4.5 w-4.5 text-zinc-400 dark:text-zinc-500" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
					<path stroke-linecap="round" stroke-linejoin="round" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
				</svg>
			</div>
			<input
				type="text"
				placeholder="Search cities, AQI, forecasts..."
				class="w-full pl-9 pr-12 py-2 rounded-xl text-sm bg-zinc-50 dark:bg-zinc-900/60 border border-zinc-200 dark:border-zinc-800 text-zinc-900 dark:text-zinc-100 placeholder-zinc-400 dark:placeholder-zinc-500 focus:outline-none focus:ring-2 focus:ring-emerald-500/20 focus:border-emerald-500 dark:focus:border-emerald-500/80 transition-all duration-200"
			/>
			<div class="absolute inset-y-0 right-0 pr-3 flex items-center pointer-events-none">
				<kbd class="text-[10px] font-semibold text-zinc-400 dark:text-zinc-500 bg-white dark:bg-zinc-800 border border-zinc-200 dark:border-zinc-700 px-1.5 py-0.5 rounded shadow-sm">
					Ctrl K
				</kbd>
			</div>
		</div>
	</div>

	<!-- Right: Actions -->
	<div class="flex items-center gap-2 sm:gap-3.5">
		<!-- Current City Dropdown -->
		<div class="relative">
			<button
				onclick={toggleCityDropdown}
				class="flex items-center gap-1.5 px-3 py-2 rounded-xl text-xs sm:text-sm font-semibold text-zinc-700 dark:text-zinc-300 hover:text-zinc-950 dark:hover:text-zinc-50 hover:bg-zinc-50 dark:hover:bg-zinc-900/60 border border-zinc-200 dark:border-zinc-800 shadow-sm focus:outline-none transition-all duration-150"
			>
				<svg class="h-4 w-4 text-emerald-500" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
					<path stroke-linecap="round" stroke-linejoin="round" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
					<path stroke-linecap="round" stroke-linejoin="round" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
				</svg>
				<span class="max-w-[100px] sm:max-w-none truncate">{currentCity}</span>
				<svg class="h-3.5 w-3.5 text-zinc-400" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
					<path stroke-linecap="round" stroke-linejoin="round" d="M19 9l-7 7-7-7" />
				</svg>
			</button>

			<!-- Dropdown Menu -->
			{#if isCityDropdownOpen}
				<div class="absolute right-0 mt-2 w-52 bg-white dark:bg-zinc-900 border border-zinc-100 dark:border-zinc-800 rounded-xl shadow-lg shadow-zinc-200/50 dark:shadow-black/40 overflow-hidden py-1 z-40 transform origin-top-right transition-all">
					<div class="px-3 py-2 border-b border-zinc-100 dark:border-zinc-800/80">
						<p class="text-[10px] font-bold text-zinc-400 dark:text-zinc-500 uppercase tracking-wider">Select Location</p>
					</div>
					{#each mockCities as city}
						<button
							onclick={() => selectCity(city)}
							class="w-full text-left px-3.5 py-2.5 text-sm text-zinc-700 dark:text-zinc-300 hover:bg-zinc-50 dark:hover:bg-zinc-800/60 hover:text-zinc-900 dark:hover:text-zinc-100 flex items-center justify-between transition-colors"
						>
							<span>{city}</span>
							{#if currentCity === city}
								<svg class="h-4 w-4 text-emerald-500" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5">
									<path stroke-linecap="round" stroke-linejoin="round" d="M5 13l4 4L19 7" />
								</svg>
							{/if}
						</button>
					{/each}
				</div>
			{/if}
		</div>

		<!-- Notifications Menu -->
		<div class="relative">
			<button
				onclick={toggleNotificationDropdown}
				class="p-2 rounded-xl border border-zinc-200 dark:border-zinc-800 text-zinc-600 dark:text-zinc-400 hover:text-zinc-950 dark:hover:text-zinc-50 hover:bg-zinc-50 dark:hover:bg-zinc-900/60 shadow-sm relative focus:outline-none transition-all duration-150"
				aria-label="View notifications"
			>
				<svg class="h-5 w-5" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
					<path stroke-linecap="round" stroke-linejoin="round" d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9" />
				</svg>
				<!-- Active notification badge -->
				<span class="absolute top-1.5 right-1.5 h-2 w-2 rounded-full bg-amber-500 animate-ping"></span>
				<span class="absolute top-1.5 right-1.5 h-2 w-2 rounded-full bg-amber-500"></span>
			</button>

			<!-- Dropdown Menu -->
			{#if isNotificationOpen}
				<div class="absolute right-0 mt-2 w-72 sm:w-80 bg-white dark:bg-zinc-900 border border-zinc-100 dark:border-zinc-800 rounded-xl shadow-lg shadow-zinc-200/50 dark:shadow-black/40 overflow-hidden py-1 z-40">
					<div class="px-4 py-2.5 border-b border-zinc-100 dark:border-zinc-800/80 flex items-center justify-between">
						<span class="text-xs font-bold text-zinc-800 dark:text-zinc-200">Notifications</span>
						<button class="text-[10px] font-semibold text-emerald-500 hover:text-emerald-600">Mark all read</button>
					</div>
					<div class="divide-y divide-zinc-100 dark:divide-zinc-800/50 max-h-64 overflow-y-auto">
						{#each mockNotifications as alert}
							<div class="p-3.5 hover:bg-zinc-50 dark:hover:bg-zinc-800/40 transition-colors">
								<div class="flex items-start gap-2.5">
									<!-- Warning/Alert Indicator -->
									<div class="mt-0.5 shrink-0">
										{#if alert.type === 'warning'}
											<span class="flex h-2 w-2 rounded-full bg-amber-500"></span>
										{:else if alert.type === 'alert'}
											<span class="flex h-2 w-2 rounded-full bg-rose-500"></span>
										{:else}
											<span class="flex h-2 w-2 rounded-full bg-blue-500"></span>
										{/if}
									</div>
									<div class="flex-1 space-y-0.5">
										<p class="text-xs text-zinc-700 dark:text-zinc-300 leading-normal">{alert.text}</p>
										<p class="text-[10px] text-zinc-400 dark:text-zinc-500 font-medium">{alert.time}</p>
									</div>
								</div>
							</div>
						{/each}
					</div>
				</div>
			{/if}
		</div>

		<!-- User Menu / Auth Buttons -->
		{#if $loggedIn}
			<div class="relative">
				<button
					onclick={toggleUserDropdown}
					class="flex items-center justify-center h-9 w-9 rounded-xl border border-zinc-200 dark:border-zinc-800 bg-zinc-100 dark:bg-zinc-800 text-zinc-800 dark:text-zinc-200 hover:border-zinc-300 dark:hover:border-zinc-700 focus:outline-none overflow-hidden shadow-sm transition-all"
					aria-label="User account"
				>
					<span class="text-sm font-bold tracking-wide">AQ</span>
				</button>

				<!-- Dropdown Menu -->
				{#if isUserDropdownOpen}
					<div class="absolute right-0 mt-2 w-52 bg-white dark:bg-zinc-900 border border-zinc-100 dark:border-zinc-800 rounded-xl shadow-lg shadow-zinc-200/50 dark:shadow-black/40 overflow-hidden py-1.5 z-40">
						<div class="px-3.5 py-2 border-b border-zinc-100 dark:border-zinc-800/80">
							<p class="text-xs font-bold text-zinc-900 dark:text-zinc-100">AeriQ User</p>
							<p class="text-[10px] text-zinc-400 dark:text-zinc-500 truncate">user@aeriq.com</p>
						</div>
						<div class="py-1">
							<a href="/settings" onclick={closeAllDropdowns} class="flex items-center gap-2 px-3.5 py-2 text-sm text-zinc-600 dark:text-zinc-400 hover:bg-zinc-50 dark:hover:bg-zinc-800/60 hover:text-zinc-900 dark:hover:text-zinc-100 transition-colors">
								<svg class="h-4 w-4" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
									<path stroke-linecap="round" stroke-linejoin="round" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
								</svg>
								Profile
							</a>
							<a href="/settings" onclick={closeAllDropdowns} class="flex items-center gap-2 px-3.5 py-2 text-sm text-zinc-600 dark:text-zinc-400 hover:bg-zinc-50 dark:hover:bg-zinc-800/60 hover:text-zinc-900 dark:hover:text-zinc-100 transition-colors">
								<svg class="h-4 w-4" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
									<path stroke-linecap="round" stroke-linejoin="round" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" />
									<path stroke-linecap="round" stroke-linejoin="round" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
								</svg>
								Settings
							</a>
						</div>
						<div class="border-t border-zinc-100 dark:border-zinc-800/80 py-1">
							<button onclick={handleLogout} class="w-full text-left flex items-center gap-2 px-3.5 py-2 text-sm text-rose-500 hover:bg-rose-50 dark:hover:bg-rose-950/20 transition-colors">
								<svg class="h-4 w-4" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
									<path stroke-linecap="round" stroke-linejoin="round" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
								</svg>
								Logout
							</button>
						</div>
					</div>
				{/if}
			</div>
		{:else}
			<div class="flex items-center gap-2">
				<button
					onclick={handleSignIn}
					class="px-3.5 py-2 bg-white/40 dark:bg-zinc-900/40 border border-zinc-200 dark:border-zinc-800 rounded-xl text-xs font-bold text-zinc-700 dark:text-zinc-350 hover:text-zinc-950 dark:hover:text-zinc-150 hover:bg-white dark:hover:bg-zinc-850 shadow-sm focus:outline-none transition-all active:scale-95"
				>
					Sign In
				</button>
				<button
					onclick={handleSignIn}
					class="px-3.5 py-2 bg-emerald-500 hover:bg-emerald-600 active:scale-95 text-white text-xs font-bold rounded-xl shadow-md shadow-emerald-500/10 focus:outline-none transition-all"
				>
					Register
				</button>
			</div>
		{/if}
	</div>
</header>
