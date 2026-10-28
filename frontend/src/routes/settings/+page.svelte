<script>
	import { onMount } from 'svelte';
	import { goto } from '$app/navigation';
	import { login } from '$lib/stores/authStore.js';
	import { serverWaking, signIn, signUp } from '$lib/api.js';

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
	let busy = $state(false);

	const vulnerabilityOptions = [
		{ value: 'asthma', label: 'Asthma' },
		{ value: 'respiratory', label: 'Other respiratory condition' },
		{ value: 'heart_disease', label: 'Heart disease' },
		{ value: 'elderly', label: 'Elderly' },
		{ value: 'child', label: 'Child' }
	];

	onMount(() => {
		if (new URLSearchParams(window.location.search).get('mode') === 'signup') mode = 'signup';
	});

	/** @param {string} value */
	function toggleVulnerability(value) {
		vulnerabilities = vulnerabilities.includes(value)
			? vulnerabilities.filter((item) => item !== value)
			: [...vulnerabilities, value];
	}

	/** @param {SubmitEvent} event */
	async function submit(event) {
		event.preventDefault();
		errorMessage = '';
		busy = true;
		try {
			const session = mode === 'login'
				? await signIn({ email: email.trim(), password })
				: await signUp({
					name: name.trim(), email: email.trim(), password,
					age: Number(age), gender, city: city.trim(),
					vulnerabilities: vulnerabilities.length ? vulnerabilities : ['none']
				});
			login(session);
			await goto('/dashboard');
		} catch (error) {
			errorMessage = error instanceof Error ? error.message : 'Unable to complete your request.';
		} finally {
			busy = false;
		}
	}
</script>

<svelte:head>
	<title>{mode === 'login' ? 'Sign In' : 'Create Account'} | AeriQ</title>
	<meta name="description" content="Sign in or create an AeriQ account to access air quality insights." />
</svelte:head>

<main class="mx-auto max-w-xl py-8">
	<div class="mb-6 space-y-2">
		<p class="text-xs font-bold uppercase tracking-widest text-emerald-500">AeriQ Account</p>
		<h1 class="text-3xl font-extrabold text-zinc-900 dark:text-white">{mode === 'login' ? 'Welcome back' : 'Create your account'}</h1>
		<p class="text-sm text-zinc-500 dark:text-zinc-400">{mode === 'login' ? 'Sign in to access your air quality dashboard.' : 'Create an account for personalized air quality and health insights.'}</p>
	</div>

	<div class="mb-5 flex gap-2 rounded-xl border border-zinc-200 p-1 dark:border-zinc-800">
		<button type="button" aria-pressed={mode === 'login'} onclick={() => { mode = 'login'; errorMessage = ''; }} class="flex-1 rounded-lg px-4 py-2 text-sm font-semibold {mode === 'login' ? 'bg-emerald-500 text-white' : 'text-zinc-500'}">Sign In</button>
		<button type="button" aria-pressed={mode === 'signup'} onclick={() => { mode = 'signup'; errorMessage = ''; }} class="flex-1 rounded-lg px-4 py-2 text-sm font-semibold {mode === 'signup' ? 'bg-emerald-500 text-white' : 'text-zinc-500'}">Create Account</button>
	</div>

	<form onsubmit={submit} class="space-y-4 rounded-2xl border border-zinc-200 bg-white p-6 shadow-sm dark:border-zinc-800 dark:bg-zinc-900">
		{#if mode === 'signup'}
			<label class="block space-y-1.5 text-sm font-medium text-zinc-700 dark:text-zinc-300">
				<span>Full name</span>
				<input bind:value={name} required minlength="2" maxlength="100" autocomplete="name" class="w-full rounded-xl border border-zinc-300 bg-transparent px-3 py-2.5 dark:border-zinc-700" />
			</label>
		{/if}

		<label class="block space-y-1.5 text-sm font-medium text-zinc-700 dark:text-zinc-300">
			<span>Email</span>
			<input bind:value={email} type="email" required autocomplete="email" class="w-full rounded-xl border border-zinc-300 bg-transparent px-3 py-2.5 dark:border-zinc-700" />
		</label>

		<label class="block space-y-1.5 text-sm font-medium text-zinc-700 dark:text-zinc-300">
			<span>Password</span>
			<input bind:value={password} type="password" required minlength="8" autocomplete={mode === 'login' ? 'current-password' : 'new-password'} class="w-full rounded-xl border border-zinc-300 bg-transparent px-3 py-2.5 dark:border-zinc-700" />
			{#if mode === 'signup'}<span class="text-xs text-zinc-500">Use at least 8 characters, including uppercase, lowercase, and a number.</span>{/if}
		</label>

		{#if mode === 'signup'}
			<div class="grid grid-cols-1 gap-4 sm:grid-cols-3">
				<label class="block space-y-1.5 text-sm font-medium text-zinc-700 dark:text-zinc-300">
					<span>Age</span><input bind:value={age} type="number" min="1" max="120" required class="w-full rounded-xl border border-zinc-300 bg-transparent px-3 py-2.5 dark:border-zinc-700" />
				</label>
				<label class="block space-y-1.5 text-sm font-medium text-zinc-700 dark:text-zinc-300 sm:col-span-2">
					<span>Gender</span><select bind:value={gender} required class="w-full rounded-xl border border-zinc-300 bg-white px-3 py-2.5 dark:border-zinc-700 dark:bg-zinc-900"><option value="">Select</option><option value="female">Female</option><option value="male">Male</option><option value="other">Other</option><option value="prefer_not_to_say">Prefer not to say</option></select>
				</label>
			</div>
			<label class="block space-y-1.5 text-sm font-medium text-zinc-700 dark:text-zinc-300">
				<span>Home city in India</span><input bind:value={city} required minlength="2" autocomplete="address-level2" placeholder="e.g. Delhi" class="w-full rounded-xl border border-zinc-300 bg-transparent px-3 py-2.5 dark:border-zinc-700" />
			</label>
			<fieldset class="space-y-2">
				<legend class="text-sm font-medium text-zinc-700 dark:text-zinc-300">Health considerations (optional)</legend>
				<div class="grid gap-2 sm:grid-cols-2">
					{#each vulnerabilityOptions as option}
						<label class="flex items-center gap-2 text-sm text-zinc-600 dark:text-zinc-400"><input type="checkbox" checked={vulnerabilities.includes(option.value)} onchange={() => toggleVulnerability(option.value)} />{option.label}</label>
					{/each}
				</div>
			</fieldset>
		{/if}

		{#if errorMessage}<p role="alert" class="rounded-lg bg-red-50 px-3 py-2 text-sm text-red-700 dark:bg-red-950/30 dark:text-red-300">{errorMessage}</p>{/if}
		{#if $serverWaking}<p role="status" class="text-sm text-amber-600 dark:text-amber-400">Waking up server… your request may take up to a minute.</p>{/if}
		<button type="submit" disabled={busy} class="w-full rounded-xl bg-emerald-500 px-4 py-3 font-semibold text-white transition hover:bg-emerald-600 disabled:cursor-wait disabled:opacity-60">{busy ? 'Please wait…' : mode === 'login' ? 'Sign In' : 'Create Account'}</button>
	</form>
</main>
