<script>
	import { onMount } from 'svelte';
	import { goto } from '$app/navigation';
	import { login, loggedIn, updateSessionUser } from '$lib/stores/authStore.js';
	import { getCurrentUser, serverWaking, signIn, signUp, updateCurrentUser } from '$lib/api.js';

	let mode = $state('login');
	let name = $state('');
	let email = $state('');
	let password = $state('');
	let age = $state('');
	let gender = $state('');
	let city = $state('');
	/** @type {string[]} */
	let vulnerabilities = $state([]);
	let errorMessage = $state('');
	let successMessage = $state('');
	let busy = $state(false);
	let loading = $state(false);

	const vulnerabilityOptions = [
		{ value: 'asthma', label: 'Asthma' },
		{ value: 'respiratory', label: 'Other respiratory condition' },
		{ value: 'heart_disease', label: 'Heart disease' },
		{ value: 'elderly', label: 'Older adult (65+)' },
		{ value: 'child', label: 'Child (under 18)' },
		{ value: 'general', label: 'General health considerations' }
	];

	onMount(async () => {
		if (new URLSearchParams(window.location.search).get('mode') === 'signup') mode = 'signup';
		if (!$loggedIn) return;
		loading = true;
		try {
			const user = await getCurrentUser();
			name = user.name ?? '';
			email = user.email ?? '';
			age = user.age == null ? '' : String(user.age);
			gender = user.gender ?? '';
			city = user.city ?? '';
			vulnerabilities = Array.isArray(user.vulnerabilities) ? user.vulnerabilities.filter((/** @type {string} */ item) => item !== 'none') : [];
		} catch (error) {
			errorMessage = error instanceof Error ? error.message : 'Unable to load your settings.';
		} finally {
			loading = false;
		}
	});

	/** @param {string} value */
	function toggleVulnerability(value) {
		vulnerabilities = vulnerabilities.includes(value)
			? vulnerabilities.filter((item) => item !== value)
			: [...vulnerabilities, value];
	}

	/** @param {SubmitEvent} event */
	async function submitAuth(event) {
		event.preventDefault(); errorMessage = ''; busy = true;
		try {
			const session = mode === 'login'
				? await signIn({ email: email.trim(), password })
				: await signUp({ name: name.trim(), email: email.trim(), password, age: Number(age), gender, city: city.trim(), vulnerabilities: vulnerabilities.length ? vulnerabilities : ['none'] });
			login(session);
			await goto('/settings');
		} catch (error) {
			errorMessage = error instanceof Error ? error.message : 'Unable to complete your request.';
		} finally { busy = false; }
	}

	/** @param {SubmitEvent} event */
	async function saveSettings(event) {
		event.preventDefault(); errorMessage = ''; successMessage = ''; busy = true;
		try {
			const user = await updateCurrentUser({ name: name.trim(), age: Number(age), gender, city: city.trim(), vulnerabilities: vulnerabilities.length ? vulnerabilities : ['none'] });
			updateSessionUser(user);
			name = user.name; age = String(user.age); gender = user.gender; city = user.city;
			vulnerabilities = (user.vulnerabilities ?? []).filter((/** @type {string} */ item) => item !== 'none');
			successMessage = 'Your profile and health settings have been saved.';
		} catch (error) {
			errorMessage = error instanceof Error ? error.message : 'Unable to save your settings.';
		} finally { busy = false; }
	}
</script>

<svelte:head>
	<title>Settings | AeriQ</title>
	<meta name="description" content="Manage your AeriQ account and health profile." />
</svelte:head>

{#if $loggedIn}
	<main class="mx-auto max-w-4xl space-y-6">
		<header class="space-y-2">
			<p class="text-xs font-bold uppercase tracking-widest text-emerald-500">Account</p>
			<h1 class="text-3xl font-extrabold text-zinc-900 dark:text-white">Settings</h1>
			<p class="text-sm text-zinc-500 dark:text-zinc-400">Edit the profile and health information used for your personalized air quality guidance.</p>
		</header>
		{#if loading}
			<section class="rounded-2xl border border-zinc-200 bg-white p-8 text-sm text-zinc-500 dark:border-zinc-800 dark:bg-zinc-900" role="status">{$serverWaking ? 'Waking up server and loading your settings…' : 'Loading your saved profile…'}</section>
		{:else}
			<form onsubmit={saveSettings} class="space-y-6">
				<section class="space-y-4 rounded-2xl border border-zinc-200 bg-white p-6 dark:border-zinc-800 dark:bg-zinc-900">
					<div><h2 class="text-lg font-bold text-zinc-900 dark:text-white">Overall profile</h2><p class="mt-1 text-sm text-zinc-500 dark:text-zinc-400">These details are saved to your AeriQ account.</p></div>
					<div class="grid gap-4 sm:grid-cols-2">
						<label class="space-y-1.5 text-sm font-medium"><span>Full name</span><input bind:value={name} required minlength="2" maxlength="100" autocomplete="name" class="w-full rounded-xl border border-zinc-300 bg-transparent px-3 py-2.5 dark:border-zinc-700" /></label>
						<label class="space-y-1.5 text-sm font-medium"><span>Email address</span><input value={email} readonly class="w-full cursor-not-allowed rounded-xl border border-zinc-300 bg-zinc-100 px-3 py-2.5 text-zinc-500 dark:border-zinc-700 dark:bg-zinc-950" /><span class="block text-xs text-zinc-500">Email changes are not supported.</span></label>
						<label class="space-y-1.5 text-sm font-medium"><span>Age</span><input bind:value={age} type="number" min="1" max="120" required class="w-full rounded-xl border border-zinc-300 bg-transparent px-3 py-2.5 dark:border-zinc-700" /></label>
						<label class="space-y-1.5 text-sm font-medium"><span>Gender</span><select bind:value={gender} required class="w-full rounded-xl border border-zinc-300 bg-white px-3 py-2.5 dark:border-zinc-700 dark:bg-zinc-900"><option value="">Select</option><option value="female">Female</option><option value="male">Male</option><option value="other">Other</option><option value="prefer_not_to_say">Prefer not to say</option></select></label>
						<label class="space-y-1.5 text-sm font-medium sm:col-span-2"><span>Home city</span><input bind:value={city} required minlength="2" autocomplete="address-level2" class="w-full rounded-xl border border-zinc-300 bg-transparent px-3 py-2.5 dark:border-zinc-700" /></label>
					</div>
				</section>
				<section class="space-y-4 rounded-2xl border border-zinc-200 bg-white p-6 dark:border-zinc-800 dark:bg-zinc-900">
					<div><h2 class="text-lg font-bold text-zinc-900 dark:text-white">Health profile</h2><p class="mt-1 text-sm text-zinc-500 dark:text-zinc-400">Select relevant groups to personalize health risk assessments.</p></div>
					<div class="grid gap-3 sm:grid-cols-2">
						{#each vulnerabilityOptions as option (option.value)}
							<label class="flex cursor-pointer items-center gap-3 rounded-xl border border-zinc-200 p-3 text-sm dark:border-zinc-800"><input type="checkbox" checked={vulnerabilities.includes(option.value)} onchange={() => toggleVulnerability(option.value)} />{option.label}</label>
						{/each}
					</div>
				</section>
				{#if errorMessage}<p role="alert" class="rounded-lg bg-red-50 px-3 py-2 text-sm text-red-700 dark:bg-red-950/30 dark:text-red-300">{errorMessage}</p>{/if}
				{#if successMessage}<p role="status" class="rounded-lg bg-emerald-50 px-3 py-2 text-sm text-emerald-700 dark:bg-emerald-950/30 dark:text-emerald-300">{successMessage}</p>{/if}
				<div class="flex flex-wrap gap-3"><button type="submit" disabled={busy} class="rounded-xl bg-emerald-500 px-5 py-3 font-semibold text-white hover:bg-emerald-600 disabled:opacity-60">{busy ? 'Saving…' : 'Save settings'}</button><button type="button" onclick={() => goto('/profile')} class="rounded-xl border border-zinc-300 px-5 py-3 font-semibold dark:border-zinc-700">View profile</button><button type="button" onclick={() => goto('/health')} class="rounded-xl border border-zinc-300 px-5 py-3 font-semibold dark:border-zinc-700">Health insights</button></div>
			</form>
		{/if}
	</main>
{:else}
	<main class="mx-auto max-w-xl py-8">
		<div class="mb-6 space-y-2"><p class="text-xs font-bold uppercase tracking-widest text-emerald-500">AeriQ Account</p><h1 class="text-3xl font-extrabold text-zinc-900 dark:text-white">{mode === 'login' ? 'Welcome back' : 'Create your account'}</h1><p class="text-sm text-zinc-500 dark:text-zinc-400">{mode === 'login' ? 'Sign in to access your air quality dashboard.' : 'Create an account for personalized air quality and health insights.'}</p></div>
		<div class="mb-5 flex gap-2 rounded-xl border border-zinc-200 p-1 dark:border-zinc-800"><button type="button" aria-pressed={mode === 'login'} onclick={() => { mode = 'login'; errorMessage = ''; }} class="flex-1 rounded-lg px-4 py-2 text-sm font-semibold {mode === 'login' ? 'bg-emerald-500 text-white' : 'text-zinc-500'}">Sign In</button><button type="button" aria-pressed={mode === 'signup'} onclick={() => { mode = 'signup'; errorMessage = ''; }} class="flex-1 rounded-lg px-4 py-2 text-sm font-semibold {mode === 'signup' ? 'bg-emerald-500 text-white' : 'text-zinc-500'}">Create Account</button></div>
		<form onsubmit={submitAuth} class="space-y-4 rounded-2xl border border-zinc-200 bg-white p-6 shadow-sm dark:border-zinc-800 dark:bg-zinc-900">
			{#if mode === 'signup'}<label class="block space-y-1.5 text-sm font-medium"><span>Full name</span><input bind:value={name} required minlength="2" maxlength="100" autocomplete="name" class="w-full rounded-xl border border-zinc-300 bg-transparent px-3 py-2.5 dark:border-zinc-700" /></label>{/if}
			<label class="block space-y-1.5 text-sm font-medium"><span>Email</span><input bind:value={email} type="email" required autocomplete="email" class="w-full rounded-xl border border-zinc-300 bg-transparent px-3 py-2.5 dark:border-zinc-700" /></label>
			<label class="block space-y-1.5 text-sm font-medium"><span>Password</span><input bind:value={password} type="password" required minlength="8" autocomplete={mode === 'login' ? 'current-password' : 'new-password'} class="w-full rounded-xl border border-zinc-300 bg-transparent px-3 py-2.5 dark:border-zinc-700" /></label>
			{#if mode === 'signup'}<div class="grid gap-4 sm:grid-cols-2"><label class="space-y-1.5 text-sm font-medium"><span>Age</span><input bind:value={age} type="number" min="1" max="120" required class="w-full rounded-xl border border-zinc-300 bg-transparent px-3 py-2.5 dark:border-zinc-700" /></label><label class="space-y-1.5 text-sm font-medium"><span>Gender</span><select bind:value={gender} required class="w-full rounded-xl border border-zinc-300 bg-white px-3 py-2.5 dark:border-zinc-700 dark:bg-zinc-900"><option value="">Select</option><option value="female">Female</option><option value="male">Male</option><option value="other">Other</option><option value="prefer_not_to_say">Prefer not to say</option></select></label></div><label class="block space-y-1.5 text-sm font-medium"><span>Home city in India</span><input bind:value={city} required minlength="2" autocomplete="address-level2" class="w-full rounded-xl border border-zinc-300 bg-transparent px-3 py-2.5 dark:border-zinc-700" /></label>{/if}
			{#if errorMessage}<p role="alert" class="rounded-lg bg-red-50 px-3 py-2 text-sm text-red-700 dark:bg-red-950/30 dark:text-red-300">{errorMessage}</p>{/if}{#if $serverWaking}<p role="status" class="text-sm text-amber-600">Waking up server… your request may take up to a minute.</p>{/if}
			<button type="submit" disabled={busy} class="w-full rounded-xl bg-emerald-500 px-4 py-3 font-semibold text-white disabled:opacity-60">{busy ? 'Please wait…' : mode === 'login' ? 'Sign In' : 'Create Account'}</button>
		</form>
	</main>
{/if}
