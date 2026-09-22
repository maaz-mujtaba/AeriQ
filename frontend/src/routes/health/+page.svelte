<script>
	import { onMount } from 'svelte';
	import { loggedIn } from '$lib/stores/authStore.js';
	import { currentAQI } from '$lib/stores/aqiStore.js';
	import { loadCurrentAQI } from '$lib/api.js';
	import LoginRequired from '$lib/components/LoginRequired.svelte';

	// Available health conditions
	const ALL_CONDITIONS = [
		'Asthma',
		'COPD',
		'Allergies',
		'Heart condition',
		'Diabetes',
		'Pregnancy',
		'None',
		'Other'
	];

	// Persistence key for health profile
	const STORAGE_KEY = 'aeriq_health_profile';

	// State for health conditions
	let savedConditions = $state(['Asthma', 'Allergies']);
	let isEditModalOpen = $state(false);
	let tempConditions = $state(['Asthma', 'Allergies']);
	let customConditionInput = $state('');

	// Ticking/formatted time state
	let formattedDateTime = $state('');

	// Load stored profile and subscribe to AQI data
	onMount(() => {
		// Update live date/time display
		const updateDateTime = () => {
			const now = new Date();
			formattedDateTime = now.toLocaleDateString('en-US', {
				day: 'numeric',
				month: 'short',
				year: 'numeric'
			}) + ', ' + now.toLocaleTimeString('en-US', {
				hour: '2-digit',
				minute: '2-digit',
				hour12: true
			});
		};
		updateDateTime();
		const timeInterval = setInterval(updateDateTime, 30000);

		// Load persisted health conditions
		try {
			const stored = localStorage.getItem(STORAGE_KEY);
			if (stored !== null) {
				const parsed = JSON.parse(stored);
				if (Array.isArray(parsed) && parsed.length > 0) {
					savedConditions = parsed;
				} else {
					savedConditions = [];
				}
			} else {
				// Initial state: default to reference conditions and persist
				savedConditions = ['Asthma', 'Allergies'];
				localStorage.setItem(STORAGE_KEY, JSON.stringify(savedConditions));
			}
		} catch (e) {
			console.error('Error reading health profile from storage:', e);
		}

		// Try loading live AQI if not already available
		if (!$currentAQI) {
			loadCurrentAQI(28.6139, 77.209).catch(() => {
				// Graceful fallback to rich local state
			});
		}

		return () => clearInterval(timeInterval);
	});

	/**
	 * Save conditions to localStorage
	 * @param {string[]} newConditions
	 */
	function persistConditions(newConditions) {
		savedConditions = newConditions;
		try {
			localStorage.setItem(STORAGE_KEY, JSON.stringify(newConditions));
		} catch (e) {
			console.error('Error saving health profile:', e);
		}
	}

	/**
	 * Open the edit modal and populate temporary selection state
	 */
	function openEditModal() {
		tempConditions = [...savedConditions];
		customConditionInput = '';
		isEditModalOpen = true;
	}

	/**
	 * Close the edit modal and discard any unsaved changes
	 */
	function closeEditModal() {
		isEditModalOpen = false;
		customConditionInput = '';
	}

	/**
	 * Toggle condition selection inside the modal
	 * @param {string} condition
	 */
	function toggleTempCondition(condition) {
		if (condition === 'None') {
			if (tempConditions.includes('None')) {
				tempConditions = [];
			} else {
				tempConditions = ['None'];
			}
			return;
		}

		let updated = tempConditions.filter((c) => c !== 'None');
		if (updated.includes(condition)) {
			updated = updated.filter((c) => c !== condition);
		} else {
			updated = [...updated, condition];
		}
		tempConditions = updated;
	}

	/**
	 * Add a custom condition within the modal
	 */
	function addCustomCondition() {
		const trimmed = customConditionInput.trim();
		if (trimmed && !tempConditions.includes(trimmed)) {
			let updated = tempConditions.filter((c) => c !== 'None');
			updated = [...updated, trimmed];
			tempConditions = updated;
			customConditionInput = '';
		}
	}

	/**
	 * Save updated conditions from modal and close
	 */
	function saveEditModal() {
		persistConditions(tempConditions);
		closeEditModal();
	}

	/**
	 * Remove a single chip from the profile card
	 * @param {string} condition
	 * @param {MouseEvent} [event]
	 */
	function removeCondition(condition, event) {
		if (event) event.stopPropagation();
		const updated = savedConditions.filter((c) => c !== condition);
		persistConditions(updated);
	}

	// Derived current AQI details
	let activeAQI = $derived($currentAQI?.aqi ?? 156);
	let activeCity = $derived(
		$currentAQI?.city
			? `${$currentAQI.city}${$currentAQI.state ? ', ' + $currentAQI.state : ''}`
			: 'New Delhi, India'
	);
	let activeDate = $derived(
		$currentAQI?.lastUpdated || formattedDateTime || '22 Sep 2026, 09:30 PM'
	);

	// Derived AQI category and styling
	let aqiCategory = $derived.by(() => {
		const val = activeAQI;
		if (val <= 50) return { label: 'Good', color: '#22c55e', textClass: 'text-emerald-500 dark:text-emerald-400', badgeClass: 'bg-emerald-500/10 text-emerald-600 dark:text-emerald-400 border-emerald-500/20' };
		if (val <= 100) return { label: 'Moderate', color: '#eab308', textClass: 'text-amber-500 dark:text-amber-400', badgeClass: 'bg-amber-500/10 text-amber-600 dark:text-amber-400 border-amber-500/20' };
		if (val <= 200) return { label: 'Unhealthy', color: '#ef4444', textClass: 'text-red-500 dark:text-red-400', badgeClass: 'bg-red-500/10 text-red-600 dark:text-red-400 border-red-500/20' };
		if (val <= 300) return { label: 'Very Unhealthy', color: '#a855f7', textClass: 'text-purple-500 dark:text-purple-400', badgeClass: 'bg-purple-500/10 text-purple-600 dark:text-purple-400 border-purple-500/20' };
		return { label: 'Hazardous', color: '#881337', textClass: 'text-rose-600 dark:text-rose-400', badgeClass: 'bg-rose-500/15 text-rose-700 dark:text-rose-300 border-rose-500/30' };
	});

	// Check condition presence
	let hasRespiratoryCondition = $derived(
		savedConditions.some((c) =>
			['Asthma', 'COPD', 'Allergies'].includes(c)
		)
	);
	let hasAsthma = $derived(savedConditions.includes('Asthma'));
	let hasCopd = $derived(savedConditions.includes('COPD'));
	let hasHeart = $derived(savedConditions.includes('Heart condition'));
	let hasPregnancy = $derived(savedConditions.includes('Pregnancy'));

	// Derived Health Risk based on conditions and AQI
	let healthRisk = $derived.by(() => {
		const val = activeAQI;
		const isSensitive = hasRespiratoryCondition || hasHeart || hasPregnancy;

		if (val <= 50) {
			return {
				level: 'Low Risk',
				badgeClass: 'bg-emerald-500/10 text-emerald-600 dark:text-emerald-400 border-emerald-500/20',
				dotClass: 'bg-emerald-500',
				text: 'Air quality is satisfactory. Minimal health impact expected for your profile.'
			};
		} else if (val <= 100) {
			if (isSensitive) {
				return {
					level: 'Moderate Risk',
					badgeClass: 'bg-amber-500/10 text-amber-600 dark:text-amber-400 border-amber-500/20',
					dotClass: 'bg-amber-500',
					text: 'Sensitive individuals may experience minor irritation or respiratory symptoms.'
				};
			}
			return {
				level: 'Low Risk',
				badgeClass: 'bg-emerald-500/10 text-emerald-600 dark:text-emerald-400 border-emerald-500/20',
				dotClass: 'bg-emerald-500',
				text: 'Air quality is acceptable for the general population.'
			};
		} else if (val <= 200) {
			if (isSensitive) {
				return {
					level: 'Elevated Risk',
					badgeClass: 'bg-red-500/10 text-red-600 dark:text-red-400 border-red-500/20',
					dotClass: 'bg-red-500',
					text: 'Due to your health condition(s), current air quality may increase the likelihood of respiratory irritation and breathing discomfort.'
				};
			}
			return {
				level: 'Moderate Risk',
				badgeClass: 'bg-amber-500/10 text-amber-600 dark:text-amber-400 border-amber-500/20',
				dotClass: 'bg-amber-500',
				text: 'Members of sensitive groups may experience health effects. General public is less likely to be affected.'
			};
		} else if (val <= 300) {
			return {
				level: isSensitive ? 'Severe Risk' : 'High Risk',
				badgeClass: 'bg-purple-500/10 text-purple-600 dark:text-purple-400 border-purple-500/20',
				dotClass: 'bg-purple-500',
				text: 'Health alert: High risk of aggravated symptoms for your condition. Limit outdoor exposure.'
			};
		} else {
			return {
				level: 'Critical Risk',
				badgeClass: 'bg-rose-500/15 text-rose-700 dark:text-rose-300 border-rose-500/30',
				dotClass: 'bg-rose-600',
				text: 'Emergency conditions. Significant health danger for your profile. Remain indoors.'
			};
		}
	});

	// Dynamic fourth recommendation card tailored to condition
	let tailoredCard4 = $derived.by(() => {
		if (hasAsthma || hasCopd) {
			return {
				icon: 'inhaler',
				title: 'Carry Your Inhaler',
				text: "If you're going out, make sure to keep your prescribed inhaler with you."
			};
		} else if (hasRespiratoryCondition) {
			return {
				icon: 'medical',
				title: 'Manage Allergens',
				text: 'Keep anti-allergy medication accessible and rinse nasal passages if exposed outdoors.'
			};
		} else if (hasHeart) {
			return {
				icon: 'heart',
				title: 'Monitor Heart Rate',
				text: 'Watch for chest tightness or unusual fatigue. Rest indoors and avoid physical strain.'
			};
		} else if (hasPregnancy) {
			return {
				icon: 'shield',
				title: 'Protect & Rest',
				text: 'Limit exposure to traffic pollutants. Relax in well-filtered, temperature-controlled spaces.'
			};
		} else {
			return {
				icon: 'air',
				title: 'Air Purification',
				text: 'Run an indoor air purifier or maintain clean filters to minimize ambient particulate buildup.'
			};
		}
	});
</script>

<svelte:head>
	<title>Health Recommendations | AeriQ</title>
	<meta name="description" content="Personalized air-quality guidance based on your health profile." />
</svelte:head>

{#if !$loggedIn}
	<LoginRequired
		title="Health Recommendations"
		description="Access medical-backed health recommendations, air quality alerts, and activity schedules tailored for your active locations."
	/>
{:else}
	<div class="space-y-6 select-none max-w-7xl mx-auto">
		<!-- 1. PAGE HEADER -->
		<div class="space-y-1">
			<div class="flex items-center gap-2 text-xs font-semibold text-zinc-400 dark:text-zinc-500 uppercase tracking-wider">
				<span>App</span>
				<span>/</span>
				<span class="text-emerald-500 dark:text-emerald-400 font-bold">Health</span>
			</div>
			<h1 class="text-2xl sm:text-3xl font-extrabold tracking-tight text-zinc-900 dark:text-white">
				Health Recommendations
			</h1>
			<p class="text-sm text-zinc-500 dark:text-zinc-400 font-medium">
				Personalized air-quality guidance based on your health profile.
			</p>
		</div>

		<!-- 2, 3, 4. TOP ROW (3 CARDS ON DESKTOP) -->
		<div class="grid grid-cols-1 lg:grid-cols-3 gap-5">
			<!-- CARD 1: HEALTH PROFILE CARD -->
			<div class="bg-white dark:bg-zinc-900/70 border border-zinc-200/80 dark:border-zinc-800/80 rounded-2xl p-6 shadow-sm flex flex-col justify-between transition-all duration-300 relative overflow-hidden backdrop-blur-sm">
				<div class="space-y-4">
					<!-- Card Header -->
					<div class="flex items-center justify-between gap-3">
						<div class="flex items-center gap-2.5">
							<div class="h-9 w-9 rounded-xl bg-emerald-500/10 text-emerald-500 flex items-center justify-center shrink-0">
								<!-- Health / User Icon -->
								<svg class="h-5 w-5" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
									<path stroke-linecap="round" stroke-linejoin="round" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
								</svg>
							</div>
							<h2 class="text-base font-bold text-zinc-900 dark:text-white">
								Your Health Profile
							</h2>
						</div>

						<!-- Edit Button -->
						<button
							type="button"
							onclick={openEditModal}
							class="text-xs font-semibold px-3 py-1.5 rounded-lg border bg-zinc-100 hover:bg-zinc-200/80 dark:bg-zinc-800/80 dark:hover:bg-zinc-800 text-zinc-700 dark:text-zinc-300 border-zinc-200 dark:border-zinc-700/80 transition-all duration-200 focus:outline-none"
						>
							Edit
						</button>
					</div>

					<!-- Card Description -->
					<p class="text-xs text-zinc-500 dark:text-zinc-400 leading-relaxed">
						Your selected health conditions are saved and used to give you personalized recommendations.
					</p>

					<!-- Chips Area (No + Add button) -->
					<div class="pt-1">
						<div class="flex flex-wrap items-center gap-2">
							{#if savedConditions.length === 0}
								<span class="text-xs text-zinc-400 italic">No condition selected.</span>
							{:else}
								{#each savedConditions as condition}
									<span class="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-semibold bg-emerald-500/10 text-emerald-700 dark:text-emerald-300 border border-emerald-500/20 transition-all">
										<span>{condition}</span>
										<button
											type="button"
											onclick={(e) => removeCondition(condition, e)}
											aria-label="Remove {condition}"
											class="h-3.5 w-3.5 rounded-full hover:bg-emerald-500/20 text-emerald-600 dark:text-emerald-400 flex items-center justify-center transition-colors text-xs font-bold leading-none"
										>
											&times;
										</button>
									</span>
								{/each}
							{/if}
						</div>
					</div>
				</div>
			</div>

			<!-- CARD 2: CURRENT AIR QUALITY CARD -->
			<div class="bg-white dark:bg-zinc-900/70 border border-zinc-200/80 dark:border-zinc-800/80 rounded-2xl p-6 shadow-sm flex flex-col justify-between transition-all duration-300 relative overflow-hidden backdrop-blur-sm">
				<div class="space-y-4">
					<!-- Card Header -->
					<div class="flex items-center justify-between gap-3">
						<div class="flex items-center gap-2.5">
							<div class="h-9 w-9 rounded-xl bg-emerald-500/10 text-emerald-500 flex items-center justify-center shrink-0">
								<!-- Wind / AQI Icon -->
								<svg class="h-5 w-5" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
									<path stroke-linecap="round" stroke-linejoin="round" d="M14 5l7 7m0 0l-7 7m7-7H3" />
								</svg>
							</div>
							<h2 class="text-base font-bold text-zinc-900 dark:text-white">
								Current Air Quality
							</h2>
						</div>

						<!-- Status Badge -->
						<span class="inline-flex items-center px-2.5 py-1 rounded-full text-xs font-extrabold border {aqiCategory.badgeClass}">
							{aqiCategory.label}
						</span>
					</div>

					<!-- AQI Large Number Display -->
					<div class="flex items-baseline gap-3 pt-1">
						<span class="text-4xl sm:text-5xl font-black tracking-tight text-zinc-900 dark:text-white">
							{activeAQI}
						</span>
						<span class="text-sm font-semibold text-zinc-400 dark:text-zinc-500">
							AQI
						</span>
					</div>

					<!-- Location & Timestamp -->
					<div class="space-y-1.5 pt-1 text-xs text-zinc-500 dark:text-zinc-400">
						<div class="flex items-center gap-1.5">
							<svg class="h-4 w-4 text-zinc-400 shrink-0" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
								<path stroke-linecap="round" stroke-linejoin="round" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
								<path stroke-linecap="round" stroke-linejoin="round" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
							</svg>
							<span class="font-medium text-zinc-700 dark:text-zinc-300">{activeCity}</span>
						</div>

						<div class="flex items-center gap-1.5 text-[11px] text-zinc-400 dark:text-zinc-500">
							<svg class="h-3.5 w-3.5 shrink-0" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
								<path stroke-linecap="round" stroke-linejoin="round" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
							</svg>
							<span>{activeDate}</span>
						</div>
					</div>
				</div>

				<!-- Subtle AQI Spectrum Bar at bottom -->
				<div class="mt-4 pt-3 border-t border-zinc-100 dark:border-zinc-800/80">
					<div class="h-1.5 w-full bg-zinc-200 dark:bg-zinc-800 rounded-full overflow-hidden flex">
						<div class="h-full bg-emerald-500" style="width: 15%;"></div>
						<div class="h-full bg-amber-500" style="width: 15%;"></div>
						<div class="h-full bg-orange-500" style="width: 30%;"></div>
						<div class="h-full bg-purple-500" style="width: 25%;"></div>
						<div class="h-full bg-rose-900" style="width: 15%;"></div>
					</div>
				</div>
			</div>

			<!-- CARD 3: HEALTH RISK CARD -->
			<div class="bg-white dark:bg-zinc-900/70 border border-zinc-200/80 dark:border-zinc-800/80 rounded-2xl p-6 shadow-sm flex flex-col justify-between transition-all duration-300 relative overflow-hidden backdrop-blur-sm">
				<div class="space-y-4">
					<!-- Card Header -->
					<div class="flex items-center justify-between gap-3">
						<div class="flex items-center gap-2.5">
							<div class="h-9 w-9 rounded-xl bg-emerald-500/10 text-emerald-500 flex items-center justify-center shrink-0">
								<!-- Heart pulse / Risk Icon -->
								<svg class="h-5 w-5" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
									<path stroke-linecap="round" stroke-linejoin="round" d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z" />
								</svg>
							</div>
							<h2 class="text-base font-bold text-zinc-900 dark:text-white">
								Your Health Risk
							</h2>
						</div>

						<!-- Status Badge -->
						<span class="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-extrabold border {healthRisk.badgeClass}">
							<span class="h-1.5 w-1.5 rounded-full {healthRisk.dotClass}"></span>
							{healthRisk.level}
						</span>
					</div>

					<!-- Risk Explanation -->
					<div class="pt-1">
						<p class="text-xs sm:text-sm text-zinc-600 dark:text-zinc-300 leading-relaxed font-normal">
							{healthRisk.text}
						</p>
					</div>

					<!-- Note on general guidance -->
					<div class="pt-2 text-[11px] text-zinc-400 dark:text-zinc-500 flex items-center gap-1.5">
						<svg class="h-3.5 w-3.5 shrink-0 text-zinc-400" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
							<path stroke-linecap="round" stroke-linejoin="round" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
						</svg>
						<span>Based on your saved profile and active AQI ({activeAQI}).</span>
					</div>
				</div>
			</div>
		</div>

		<!-- 5. "WHAT SHOULD YOU DO NOW?" SECTION -->
		<div class="bg-white dark:bg-zinc-900/70 border border-zinc-200/80 dark:border-zinc-800/80 rounded-2xl p-6 sm:p-7 shadow-sm transition-all duration-300 backdrop-blur-sm space-y-5">
			<div>
				<h2 class="text-lg font-extrabold text-zinc-900 dark:text-white tracking-tight">
					What should you do now?
				</h2>
				<p class="text-xs sm:text-sm text-zinc-500 dark:text-zinc-400 font-medium mt-0.5">
					Simple steps to stay safe based on your health profile and current AQI.
				</p>
			</div>

			<!-- 4 Horizontal Recommendation Cards -->
			<div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
				<!-- CARD 1: Indoor Activities -->
				<div class="p-5 rounded-xl bg-zinc-50/70 dark:bg-zinc-800/40 border border-zinc-200/60 dark:border-zinc-800/60 flex flex-col justify-between space-y-4 hover:border-emerald-500/30 transition-all duration-200">
					<div class="space-y-3">
						<div class="h-10 w-10 rounded-xl bg-emerald-500/10 text-emerald-500 flex items-center justify-center shrink-0">
							<!-- Home Icon -->
							<svg class="h-5 w-5" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
								<path stroke-linecap="round" stroke-linejoin="round" d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6" />
							</svg>
						</div>
						<h3 class="text-sm font-bold text-zinc-900 dark:text-white">
							Indoor Activities
						</h3>
						<p class="text-xs text-zinc-500 dark:text-zinc-400 leading-relaxed">
							Prefer indoor activities and keep windows closed when AQI is high.
						</p>
					</div>
				</div>

				<!-- CARD 2: Outdoor Activity -->
				<div class="p-5 rounded-xl bg-zinc-50/70 dark:bg-zinc-800/40 border border-zinc-200/60 dark:border-zinc-800/60 flex flex-col justify-between space-y-4 hover:border-emerald-500/30 transition-all duration-200">
					<div class="space-y-3">
						<div class="h-10 w-10 rounded-xl bg-emerald-500/10 text-emerald-500 flex items-center justify-center shrink-0">
							<!-- Running / Activity Icon -->
							<svg class="h-5 w-5" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
								<path stroke-linecap="round" stroke-linejoin="round" d="M13 10V3L4 14h7v7l9-11h-7z" />
							</svg>
						</div>
						<h3 class="text-sm font-bold text-zinc-900 dark:text-white">
							Outdoor Activity
						</h3>
						<p class="text-xs text-zinc-500 dark:text-zinc-400 leading-relaxed">
							Avoid prolonged or strenuous outdoor exercise.
						</p>
					</div>
				</div>

				<!-- CARD 3: Wear a Mask -->
				<div class="p-5 rounded-xl bg-zinc-50/70 dark:bg-zinc-800/40 border border-zinc-200/60 dark:border-zinc-800/60 flex flex-col justify-between space-y-4 hover:border-emerald-500/30 transition-all duration-200">
					<div class="space-y-3">
						<div class="h-10 w-10 rounded-xl bg-emerald-500/10 text-emerald-500 flex items-center justify-center shrink-0">
							<!-- Mask / Shield Icon -->
							<svg class="h-5 w-5" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
								<path stroke-linecap="round" stroke-linejoin="round" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" />
							</svg>
						</div>
						<h3 class="text-sm font-bold text-zinc-900 dark:text-white">
							Wear a Mask
						</h3>
						<p class="text-xs text-zinc-500 dark:text-zinc-400 leading-relaxed">
							Use a well-fitting mask (N95 or equivalent) when outdoors.
						</p>
					</div>
				</div>

				<!-- CARD 4: Tailored to Condition (Carry Your Inhaler / Medical) -->
				<div class="p-5 rounded-xl bg-zinc-50/70 dark:bg-zinc-800/40 border border-zinc-200/60 dark:border-zinc-800/60 flex flex-col justify-between space-y-4 hover:border-emerald-500/30 transition-all duration-200">
					<div class="space-y-3">
						<div class="h-10 w-10 rounded-xl bg-emerald-500/10 text-emerald-500 flex items-center justify-center shrink-0">
							{#if tailoredCard4.icon === 'inhaler' || tailoredCard4.icon === 'medical'}
								<!-- Inhaler / Medical Dispenser Icon -->
								<svg class="h-5 w-5" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
									<path stroke-linecap="round" stroke-linejoin="round" d="M19.428 15.428a2 2 0 00-1.022-.547l-2.387-.477a6 6 0 00-3.86.517l-.318.158a6 6 0 01-3.86.517L6.05 15.21a2 2 0 00-1.806.547M8 4h8l-1 1v5.172a2 2 0 00.586 1.414l5 5c1.26 1.26.367 3.414-1.415 3.414H4.828c-1.782 0-2.674-2.154-1.414-3.414l5-5A2 2 0 009 10.172V5L8 4z" />
								</svg>
							{:else if tailoredCard4.icon === 'heart'}
								<!-- Heart Icon -->
								<svg class="h-5 w-5" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
									<path stroke-linecap="round" stroke-linejoin="round" d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z" />
								</svg>
							{:else}
								<!-- Air / Shield Icon -->
								<svg class="h-5 w-5" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
									<path stroke-linecap="round" stroke-linejoin="round" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" />
								</svg>
							{/if}
						</div>
						<h3 class="text-sm font-bold text-zinc-900 dark:text-white">
							{tailoredCard4.title}
						</h3>
						<p class="text-xs text-zinc-500 dark:text-zinc-400 leading-relaxed">
							{tailoredCard4.text}
						</p>
					</div>
				</div>
			</div>
		</div>

		<!-- 7. AQI LEVELS & HEALTH IMPACT (FOR YOUR CONDITION) -->
		<div class="bg-white dark:bg-zinc-900/70 border border-zinc-200/80 dark:border-zinc-800/80 rounded-2xl p-6 sm:p-7 shadow-sm transition-all duration-300 backdrop-blur-sm space-y-4">
			<div>
				<h2 class="text-lg font-extrabold text-zinc-900 dark:text-white tracking-tight">
					AQI Levels & Health Impact (For Your Condition)
				</h2>
			</div>

			<!-- 5 Compact Columns -->
			<div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-5 gap-3.5">
				<!-- LEVEL 1: Good (0 - 50) -->
				<div class="p-4 rounded-xl border transition-all duration-200 flex flex-col justify-between {activeAQI <= 50 ? 'bg-emerald-500/10 border-emerald-500/40 ring-1 ring-emerald-500/30' : 'bg-zinc-50/60 dark:bg-zinc-800/30 border-zinc-200/70 dark:border-zinc-800/60'}">
					<div class="space-y-2">
						<div class="flex items-center justify-between">
							<span class="text-xs font-black text-emerald-600 dark:text-emerald-400">
								0 – 50
							</span>
							{#if activeAQI <= 50}
								<span class="text-[10px] font-extrabold uppercase px-1.5 py-0.5 rounded bg-emerald-500 text-white">Current</span>
							{/if}
						</div>
						<h4 class="text-sm font-bold text-zinc-900 dark:text-white">
							Good
						</h4>
						<p class="text-xs text-zinc-500 dark:text-zinc-400 leading-relaxed">
							Generally safe for outdoor activities.
						</p>
					</div>
				</div>

				<!-- LEVEL 2: Moderate (51 - 100) -->
				<div class="p-4 rounded-xl border transition-all duration-200 flex flex-col justify-between {activeAQI > 50 && activeAQI <= 100 ? 'bg-amber-500/10 border-amber-500/40 ring-1 ring-amber-500/30' : 'bg-zinc-50/60 dark:bg-zinc-800/30 border-zinc-200/70 dark:border-zinc-800/60'}">
					<div class="space-y-2">
						<div class="flex items-center justify-between">
							<span class="text-xs font-black text-amber-600 dark:text-amber-400">
								51 – 100
							</span>
							{#if activeAQI > 50 && activeAQI <= 100}
								<span class="text-[10px] font-extrabold uppercase px-1.5 py-0.5 rounded bg-amber-500 text-white">Current</span>
							{/if}
						</div>
						<h4 class="text-sm font-bold text-zinc-900 dark:text-white">
							Moderate
						</h4>
						<p class="text-xs text-zinc-500 dark:text-zinc-400 leading-relaxed">
							May cause mild symptoms in sensitive individuals.
						</p>
					</div>
				</div>

				<!-- LEVEL 3: Unhealthy (101 - 200) -->
				<div class="p-4 rounded-xl border transition-all duration-200 flex flex-col justify-between {activeAQI > 100 && activeAQI <= 200 ? 'bg-orange-500/10 border-orange-500/40 ring-1 ring-orange-500/30' : 'bg-zinc-50/60 dark:bg-zinc-800/30 border-zinc-200/70 dark:border-zinc-800/60'}">
					<div class="space-y-2">
						<div class="flex items-center justify-between">
							<span class="text-xs font-black text-orange-600 dark:text-orange-400">
								101 – 200
							</span>
							{#if activeAQI > 100 && activeAQI <= 200}
								<span class="text-[10px] font-extrabold uppercase px-1.5 py-0.5 rounded bg-orange-500 text-white">Current</span>
							{/if}
						</div>
						<h4 class="text-sm font-bold text-zinc-900 dark:text-white">
							Unhealthy
						</h4>
						<p class="text-xs text-zinc-500 dark:text-zinc-400 leading-relaxed">
							Higher risk of breathing difficulty and allergy symptoms.
						</p>
					</div>
				</div>

				<!-- LEVEL 4: Very Unhealthy (201 - 300) -->
				<div class="p-4 rounded-xl border transition-all duration-200 flex flex-col justify-between {activeAQI > 200 && activeAQI <= 300 ? 'bg-purple-500/10 border-purple-500/40 ring-1 ring-purple-500/30' : 'bg-zinc-50/60 dark:bg-zinc-800/30 border-zinc-200/70 dark:border-zinc-800/60'}">
					<div class="space-y-2">
						<div class="flex items-center justify-between">
							<span class="text-xs font-black text-purple-600 dark:text-purple-400">
								201 – 300
							</span>
							{#if activeAQI > 200 && activeAQI <= 300}
								<span class="text-[10px] font-extrabold uppercase px-1.5 py-0.5 rounded bg-purple-500 text-white">Current</span>
							{/if}
						</div>
						<h4 class="text-sm font-bold text-zinc-900 dark:text-white">
							Very Unhealthy
						</h4>
						<p class="text-xs text-zinc-500 dark:text-zinc-400 leading-relaxed">
							Avoid outdoor exposure. Follow medical advice.
						</p>
					</div>
				</div>

				<!-- LEVEL 5: Hazardous (301+) -->
				<div class="p-4 rounded-xl border transition-all duration-200 flex flex-col justify-between {activeAQI > 300 ? 'bg-rose-500/15 border-rose-500/50 ring-1 ring-rose-500/30' : 'bg-zinc-50/60 dark:bg-zinc-800/30 border-zinc-200/70 dark:border-zinc-800/60'}">
					<div class="space-y-2">
						<div class="flex items-center justify-between">
							<span class="text-xs font-black text-rose-600 dark:text-rose-400">
								301+
							</span>
							{#if activeAQI > 300}
								<span class="text-[10px] font-extrabold uppercase px-1.5 py-0.5 rounded bg-rose-600 text-white">Current</span>
							{/if}
						</div>
						<h4 class="text-sm font-bold text-zinc-900 dark:text-white">
							Hazardous
						</h4>
						<p class="text-xs text-zinc-500 dark:text-zinc-400 leading-relaxed">
							Stay indoors. Minimize exposure as much as possible.
						</p>
					</div>
				</div>
			</div>
		</div>

		<!-- 11. MEDICAL SAFETY DISCLAIMER -->
		<div class="pt-2 pb-6 text-center">
			<p class="text-xs text-zinc-400 dark:text-zinc-500 max-w-2xl mx-auto leading-relaxed">
				AeriQ provides general air-quality guidance and does not diagnose or treat medical conditions. Always follow the advice of your healthcare professional.
			</p>
		</div>
	</div>

	<!-- EDIT HEALTH PROFILE MODAL OVERLAY -->
	{#if isEditModalOpen}
		<div
			class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/60 backdrop-blur-xs transition-opacity animate-fade-in"
			role="dialog"
			aria-modal="true"
			aria-labelledby="modal-title"
			tabindex="-1"
			onclick={(e) => { if (e.target === e.currentTarget) closeEditModal(); }}
			onkeydown={(e) => { if (e.key === 'Escape') closeEditModal(); }}
		>
			<div
				class="bg-white dark:bg-zinc-900 border border-zinc-200/80 dark:border-zinc-800 rounded-2xl p-6 sm:p-7 shadow-2xl max-w-md w-full space-y-5 relative transition-all"
				onclick={(e) => e.stopPropagation()}
			>
				<!-- Modal Header -->
				<div class="flex items-start justify-between gap-3">
					<div class="space-y-1">
						<h3 id="modal-title" class="text-lg font-bold text-zinc-900 dark:text-white">
							Edit Health Profile
						</h3>
						<p class="text-xs text-zinc-500 dark:text-zinc-400 leading-relaxed">
							Select the conditions you'd like AeriQ to consider for your air-quality recommendations.
						</p>
					</div>

					<!-- Close X Button -->
					<button
						type="button"
						onclick={closeEditModal}
						aria-label="Close modal"
						class="text-zinc-400 hover:text-zinc-600 dark:text-zinc-500 dark:hover:text-zinc-300 p-1 rounded-lg hover:bg-zinc-100 dark:hover:bg-zinc-800 transition-colors focus:outline-none shrink-0"
					>
						<svg class="h-5 w-5" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
							<path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12" />
						</svg>
					</button>
				</div>

				<!-- Conditions Options -->
				<div class="space-y-2">
					<span class="text-[11px] font-bold uppercase tracking-wider text-zinc-400 dark:text-zinc-500">
						Available Conditions
					</span>
					<div class="flex flex-wrap gap-2 pt-1">
						{#each ALL_CONDITIONS as item}
							{@const isSelected = tempConditions.includes(item)}
							<button
								type="button"
								onclick={() => toggleTempCondition(item)}
								class="text-xs px-3 py-1.5 rounded-xl border transition-all flex items-center gap-1.5 focus:outline-none {isSelected ? 'bg-emerald-500 text-white border-emerald-500 font-semibold shadow-xs' : 'bg-zinc-100 hover:bg-zinc-200/70 dark:bg-zinc-800/80 dark:hover:bg-zinc-800 text-zinc-700 dark:text-zinc-300 border-zinc-200 dark:border-zinc-700 hover:border-emerald-500/40'}"
							>
								{#if isSelected}
									<svg class="h-3.5 w-3.5" fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24">
										<path stroke-linecap="round" stroke-linejoin="round" d="M5 13l4 4L19 7" />
									</svg>
								{/if}
								<span>{item}</span>
							</button>
						{/each}
					</div>
				</div>

				<!-- Custom Condition input (when Other is selected) -->
				{#if tempConditions.includes('Other')}
					<div class="pt-1 space-y-1.5">
						<label for="custom-condition" class="text-[11px] font-bold uppercase tracking-wider text-zinc-400 dark:text-zinc-500">
							Specify Other Condition
						</label>
						<div class="flex items-center gap-2">
							<input
								id="custom-condition"
								type="text"
								bind:value={customConditionInput}
								placeholder="e.g. Bronchitis..."
								class="flex-1 text-xs px-3 py-2 rounded-xl bg-zinc-50 dark:bg-zinc-800/60 border border-zinc-200 dark:border-zinc-700 text-zinc-900 dark:text-zinc-100 focus:outline-none focus:border-emerald-500"
								onkeydown={(e) => { if (e.key === 'Enter') { e.preventDefault(); addCustomCondition(); } }}
							/>
							<button
								type="button"
								onclick={addCustomCondition}
								class="text-xs font-semibold px-3 py-2 bg-emerald-500 hover:bg-emerald-600 text-white rounded-xl transition-colors shrink-0"
							>
								Add
							</button>
						</div>
					</div>
				{/if}

				<!-- Modal Actions: Cancel & Save Changes -->
				<div class="flex items-center justify-end gap-2.5 pt-3 border-t border-zinc-100 dark:border-zinc-800/80">
					<button
						type="button"
						onclick={closeEditModal}
						class="px-4 py-2 text-xs font-semibold rounded-xl border border-zinc-200 dark:border-zinc-700 text-zinc-700 dark:text-zinc-300 hover:bg-zinc-100 dark:hover:bg-zinc-800 transition-colors focus:outline-none"
					>
						Cancel
					</button>
					<button
						type="button"
						onclick={saveEditModal}
						class="px-4.5 py-2 text-xs font-semibold rounded-xl bg-emerald-500 hover:bg-emerald-600 active:scale-95 text-white shadow-sm shadow-emerald-500/20 transition-all focus:outline-none"
					>
						Save Changes
					</button>
				</div>
			</div>
		</div>
	{/if}
{/if}
