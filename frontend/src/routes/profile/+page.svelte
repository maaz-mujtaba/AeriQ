<script>
	import { onMount } from 'svelte';
	import { getCurrentUser, serverWaking } from '$lib/api.js';

	/** @type {{ id: number, name: string, email: string, age: number | null, gender: string | null, city: string | null, vulnerabilities: string[], created_at: string, updated_at?: string | null } | null} */
	let profile = $state(null);
	let loading = $state(true);
	let errorMessage = $state('');

	onMount(async () => {
		try {
			profile = await getCurrentUser();
		} catch (error) {
			errorMessage = error instanceof Error ? error.message : 'Unable to load your profile.';
		} finally {
			loading = false;
		}
	});

	/** @param {string} value */
	const titleCase = (value) => value.replaceAll('_', ' ').replace(/\b\w/g, (letter) => letter.toUpperCase());
	/** @param {string | number | null | undefined} value */
	const displayValue = (value) => value === null || value === undefined || value === '' ? 'Not provided' : value;
	/** @param {string | null | undefined} value */
	const formatDate = (value) => value ? new Intl.DateTimeFormat(undefined, { dateStyle: 'long' }).format(new Date(value)) : 'Not available';
</script>

<svelte:head>
	<title>Profile | AeriQ</title>
	<meta name="description" content="View your AeriQ account and health profile." />
</svelte:head>

<main class="mx-auto max-w-4xl space-y-6">
	<header class="space-y-2">
		<p class="text-xs font-bold uppercase tracking-widest text-emerald-500">Account</p>
		<h1 class="text-3xl font-extrabold text-zinc-900 dark:text-white">Your Profile</h1>
		<p class="text-sm text-zinc-500 dark:text-zinc-400">Account information loaded from your AeriQ profile.</p>
	</header>

	{#if loading}
		<section class="rounded-2xl border border-zinc-200 bg-white p-8 text-sm text-zinc-500 shadow-sm dark:border-zinc-800 dark:bg-zinc-900" role="status">
			{$serverWaking ? 'Waking up server and loading your profile…' : 'Loading your profile…'}
		</section>
	{:else if errorMessage}
		<section class="rounded-2xl border border-red-200 bg-red-50 p-6 text-sm text-red-700 dark:border-red-900 dark:bg-red-950/30 dark:text-red-300" role="alert">
			<p class="font-semibold">We could not load your profile.</p>
			<p class="mt-1">{errorMessage}</p>
			<button onclick={() => location.reload()} class="mt-4 rounded-lg bg-red-700 px-4 py-2 font-semibold text-white hover:bg-red-800">Try again</button>
		</section>
	{:else if profile}
		<section class="rounded-2xl border border-zinc-200 bg-white p-6 shadow-sm dark:border-zinc-800 dark:bg-zinc-900 sm:p-8">
			<div class="flex items-center gap-4 border-b border-zinc-100 pb-6 dark:border-zinc-800">
				<div class="flex h-14 w-14 items-center justify-center rounded-2xl bg-emerald-100 text-xl font-bold text-emerald-700 dark:bg-emerald-950/50 dark:text-emerald-400">
					{profile.name.slice(0, 1).toUpperCase()}
				</div>
				<div class="min-w-0">
					<h2 class="truncate text-xl font-bold text-zinc-900 dark:text-white">{profile.name}</h2>
					<p class="truncate text-sm text-zinc-500 dark:text-zinc-400">{profile.email}</p>
				</div>
			</div>

			<div class="grid gap-x-8 sm:grid-cols-2">
				{#each [
					{ label: 'Full name', value: profile.name },
					{ label: 'Email address', value: profile.email },
					{ label: 'Age', value: profile.age },
					{ label: 'Gender', value: profile.gender ? titleCase(profile.gender) : null },
					{ label: 'Home city', value: profile.city },
					{ label: 'Member since', value: formatDate(profile.created_at) }
				] as item}
					<div class="border-b border-zinc-100 py-4 dark:border-zinc-800">
						<p class="text-xs font-semibold uppercase tracking-wide text-zinc-400">{item.label}</p>
						<p class="mt-1 text-sm font-semibold text-zinc-800 dark:text-zinc-200">{displayValue(item.value)}</p>
					</div>
				{/each}
			</div>

			<div class="pt-6">
				<h3 class="text-sm font-bold text-zinc-900 dark:text-white">Health considerations</h3>
				{#if profile.vulnerabilities?.length}
					<div class="mt-3 flex flex-wrap gap-2">
						{#each profile.vulnerabilities as vulnerability (vulnerability)}
							<span class="rounded-full bg-emerald-50 px-3 py-1 text-xs font-semibold text-emerald-700 dark:bg-emerald-950/40 dark:text-emerald-300">{titleCase(vulnerability)}</span>
						{/each}
					</div>
				{:else}
					<p class="mt-2 text-sm text-zinc-500 dark:text-zinc-400">No health considerations saved.</p>
				{/if}
			</div>

			<div class="mt-6 rounded-xl bg-zinc-50 p-4 dark:bg-zinc-950/60">
				<h3 class="text-sm font-bold text-zinc-900 dark:text-white">Cities</h3>
				<p class="mt-1 text-sm text-zinc-600 dark:text-zinc-400">Home city saved to your account: <span class="font-semibold text-zinc-800 dark:text-zinc-200">{displayValue(profile.city)}</span></p>
				<p class="mt-1 text-xs text-zinc-500 dark:text-zinc-500">Your account currently stores one home city. Additional saved cities are not available in the backend yet.</p>
			</div>
		</section>
	{/if}
</main>
