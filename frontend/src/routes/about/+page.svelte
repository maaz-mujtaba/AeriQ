<script>
	let activeSection = 'overview';

	const features = [
		{
			icon: '◉',
			title: 'Real-Time Air Quality',
			description:
				'Monitor AQI and key environmental indicators for your selected location through a clean and focused dashboard.'
		},
		{
			icon: '↗',
			title: 'Air Quality Forecasts',
			description:
				'View forecast trends to understand how environmental conditions may change over the coming hours and days.'
		},
		{
			icon: '♡',
			title: 'Health Insights',
			description:
				'Understand how different air-quality conditions may affect sensitive groups and everyday activities.'
		},
		{
			icon: '⌁',
			title: 'AQI Map',
			description:
				'Explore air-quality conditions across locations using a visual map-based experience.'
		},
		{
			icon: '▣',
			title: 'Reports',
			description:
				'Generate structured environmental reports containing monitored conditions, trends, and relevant insights.'
		},
		{
			icon: '☆',
			title: 'Saved Cities',
			description:
				'Keep frequently monitored locations easily accessible for faster environmental monitoring.'
		}
	];

	const workflow = [
		{
			number: '01',
			title: 'Select Location',
			description: 'Choose a city or location you want to monitor.'
		},
		{
			number: '02',
			title: 'Collect Data',
			description: 'AeriQ processes available environmental and air-quality information.'
		},
		{
			number: '03',
			title: 'Analyze',
			description: 'The platform organizes measurements and identifies meaningful trends.'
		},
		{
			number: '04',
			title: 'Understand',
			description: 'View forecasts, health context, maps, alerts, and reports in one place.'
		}
	];

	const technologies = [
		'SvelteKit',
		'Tailwind CSS',
		'JavaScript',
		'REST APIs',
		'Environmental Data',
		'Data Visualization'
	];

	function setSection(section) {
		activeSection = section;

		setTimeout(() => {
			document
				.getElementById(section)
				?.scrollIntoView({ behavior: 'smooth', block: 'start' });
		}, 0);
	}
</script>

<svelte:head>
	<title>About | AeriQ</title>
	<meta
		name="description"
		content="Learn about AeriQ, an environmental intelligence platform designed to make air-quality information easier to understand and act upon."
	/>
</svelte:head>

<div class="space-y-8 pb-12">
	<!-- Breadcrumb + Header -->
	<div class="space-y-3">
		<div
			class="flex items-center gap-2 text-xs font-semibold uppercase tracking-[0.18em] text-zinc-400 dark:text-zinc-500"
		>
			<span>App</span>
			<span class="text-zinc-500">/</span>
			<span class="text-emerald-500 dark:text-emerald-400">About</span>
		</div>

		<div class="flex flex-col gap-4 lg:flex-row lg:items-end lg:justify-between">
			<div>
				<h1
					class="text-3xl font-extrabold tracking-tight text-zinc-950 dark:text-white sm:text-4xl"
				>
					About AeriQ
				</h1>

				<p class="mt-2 max-w-2xl text-sm leading-6 text-zinc-600 dark:text-zinc-400 sm:text-base">
					An environmental intelligence platform designed to make air-quality information
					easier to monitor, understand, and use.
				</p>
			</div>

			<div
				class="flex w-fit items-center gap-2 rounded-full border border-emerald-200 bg-emerald-50 px-3 py-2 text-xs font-semibold text-emerald-700 dark:border-emerald-500/20 dark:bg-emerald-500/10 dark:text-emerald-400"
			>
				<span class="h-2 w-2 rounded-full bg-emerald-500"></span>
				Environmental Intelligence
			</div>
		</div>
	</div>

	<!-- Navigation -->
	<div
		class="sticky top-4 z-10 flex flex-wrap gap-2 rounded-2xl border border-zinc-200 bg-white/90 p-2 shadow-sm backdrop-blur dark:border-zinc-800 dark:bg-zinc-950/90"
	>
		<button
			class:active-tab={activeSection === 'overview'}
			on:click={() => setSection('overview')}
			class="rounded-xl px-4 py-2 text-sm font-semibold transition-all hover:bg-zinc-100 dark:hover:bg-zinc-900"
		>
			Overview
		</button>

		<button
			class:active-tab={activeSection === 'features'}
			on:click={() => setSection('features')}
			class="rounded-xl px-4 py-2 text-sm font-semibold transition-all hover:bg-zinc-100 dark:hover:bg-zinc-900"
		>
			Features
		</button>

		<button
			class:active-tab={activeSection === 'workflow'}
			on:click={() => setSection('workflow')}
			class="rounded-xl px-4 py-2 text-sm font-semibold transition-all hover:bg-zinc-100 dark:hover:bg-zinc-900"
		>
			How It Works
		</button>

		<button
			class:active-tab={activeSection === 'technology'}
			on:click={() => setSection('technology')}
			class="rounded-xl px-4 py-2 text-sm font-semibold transition-all hover:bg-zinc-100 dark:hover:bg-zinc-900"
		>
			Technology
		</button>
	</div>

	<!-- Hero / Overview -->
	<section
		id="overview"
		class="scroll-mt-24 overflow-hidden rounded-3xl border border-zinc-200 bg-white shadow-sm dark:border-zinc-800 dark:bg-zinc-950"
	>
		<div class="relative overflow-hidden p-6 sm:p-8 lg:p-10">
			<!-- Decorative background -->
			<div
				class="pointer-events-none absolute -right-24 -top-24 h-72 w-72 rounded-full bg-emerald-500/10 blur-3xl"
			></div>

			<div
				class="pointer-events-none absolute -bottom-32 -left-20 h-64 w-64 rounded-full bg-cyan-500/5 blur-3xl"
			></div>

			<div class="relative grid gap-10 lg:grid-cols-[1.25fr_0.75fr] lg:items-center">
				<div>
					<div
						class="mb-5 inline-flex h-14 w-14 items-center justify-center rounded-2xl bg-emerald-500/10 text-2xl text-emerald-500 ring-1 ring-emerald-500/20"
					>
						⌁
					</div>

					<h2
						class="max-w-3xl text-3xl font-extrabold tracking-tight text-zinc-950 dark:text-white sm:text-4xl lg:text-5xl"
					>
						Breathe Better.
						<span class="text-emerald-500">Live Better.</span>
					</h2>

					<p
						class="mt-5 max-w-2xl text-base leading-7 text-zinc-600 dark:text-zinc-400"
					>
						AeriQ brings air-quality monitoring, forecasts, health context, location
						intelligence, alerts, and reports together in one unified experience.
					</p>

					<div class="mt-7 flex flex-wrap gap-3">
						<button
							on:click={() => setSection('features')}
							class="rounded-xl bg-emerald-500 px-5 py-3 text-sm font-bold text-white shadow-lg shadow-emerald-500/20 transition-all hover:-translate-y-0.5 hover:bg-emerald-600"
						>
							Explore Features
						</button>

						<button
							on:click={() => setSection('workflow')}
							class="rounded-xl border border-zinc-300 bg-white px-5 py-3 text-sm font-bold text-zinc-800 transition-all hover:bg-zinc-50 dark:border-zinc-700 dark:bg-zinc-900 dark:text-zinc-200 dark:hover:bg-zinc-800"
						>
							How AeriQ Works
						</button>
					</div>
				</div>

				<!-- Product Summary Card -->
				<div
					class="rounded-3xl border border-zinc-200 bg-zinc-50 p-5 dark:border-zinc-800 dark:bg-zinc-900/70"
				>
					<div class="mb-5 flex items-center justify-between">
						<div>
							<p class="text-xs font-semibold uppercase tracking-wider text-zinc-400">
								AeriQ Intelligence
							</p>
							<h3 class="mt-1 text-lg font-bold text-zinc-900 dark:text-white">
								Environmental Snapshot
							</h3>
						</div>

						<div
							class="flex h-10 w-10 items-center justify-center rounded-xl bg-emerald-500/10 text-emerald-500"
						>
							✓
						</div>
					</div>

					<div class="grid grid-cols-2 gap-3">
						<div
							class="rounded-2xl border border-zinc-200 bg-white p-4 dark:border-zinc-800 dark:bg-zinc-950"
						>
							<p class="text-xs text-zinc-500">Monitoring</p>
							<p class="mt-2 text-lg font-bold text-zinc-900 dark:text-white">
								Real-Time
							</p>
							<p class="mt-1 text-xs text-emerald-500">Environmental data</p>
						</div>

						<div
							class="rounded-2xl border border-zinc-200 bg-white p-4 dark:border-zinc-800 dark:bg-zinc-950"
						>
							<p class="text-xs text-zinc-500">Forecast</p>
							<p class="mt-2 text-lg font-bold text-zinc-900 dark:text-white">
								Trend
							</p>
							<p class="mt-1 text-xs text-emerald-500">Future conditions</p>
						</div>

						<div
							class="rounded-2xl border border-zinc-200 bg-white p-4 dark:border-zinc-800 dark:bg-zinc-950"
						>
							<p class="text-xs text-zinc-500">Health</p>
							<p class="mt-2 text-lg font-bold text-zinc-900 dark:text-white">
								Context
							</p>
							<p class="mt-1 text-xs text-emerald-500">Personal awareness</p>
						</div>

						<div
							class="rounded-2xl border border-zinc-200 bg-white p-4 dark:border-zinc-800 dark:bg-zinc-950"
						>
							<p class="text-xs text-zinc-500">Reports</p>
							<p class="mt-2 text-lg font-bold text-zinc-900 dark:text-white">
								Insights
							</p>
							<p class="mt-1 text-xs text-emerald-500">Structured output</p>
						</div>
					</div>
				</div>
			</div>
		</div>

		<!-- Mission -->
		<div
			class="grid border-t border-zinc-200 dark:border-zinc-800 lg:grid-cols-3"
		>
			<div class="p-6 sm:p-8 lg:col-span-2">
				<p class="text-xs font-bold uppercase tracking-[0.18em] text-emerald-500">
					Our Mission
				</p>

				<h3 class="mt-3 text-2xl font-bold text-zinc-950 dark:text-white">
					Turn environmental data into understandable information.
				</h3>

				<p class="mt-4 max-w-3xl text-sm leading-7 text-zinc-600 dark:text-zinc-400">
					Air-quality data can contain multiple measurements, changing conditions, forecasts,
					and health considerations. AeriQ is designed to bring those pieces together so users
					can understand their surroundings without having to interpret fragmented information
					from multiple places.
				</p>
			</div>

			<div
				class="border-t border-zinc-200 bg-zinc-50 p-6 dark:border-zinc-800 dark:bg-zinc-900/40 sm:p-8 lg:border-l lg:border-t-0"
			>
				<p class="text-xs font-bold uppercase tracking-[0.18em] text-zinc-500">
					Core Principle
				</p>

				<p class="mt-4 text-lg font-semibold leading-7 text-zinc-900 dark:text-white">
					Make complex environmental information simple, visual, and accessible.
				</p>
			</div>
		</div>
	</section>

	<!-- Features -->
	<section id="features" class="scroll-mt-24 space-y-5">
		<div>
			<p class="text-xs font-bold uppercase tracking-[0.18em] text-emerald-500">
				Platform Capabilities
			</p>

			<h2 class="mt-2 text-2xl font-bold text-zinc-950 dark:text-white sm:text-3xl">
				Everything you need in one place
			</h2>

			<p class="mt-2 max-w-2xl text-sm leading-6 text-zinc-600 dark:text-zinc-400">
				AeriQ connects monitoring, prediction, location intelligence, health information,
				and reporting into a single dashboard experience.
			</p>
		</div>

		<div class="grid gap-4 sm:grid-cols-2 xl:grid-cols-3">
			{#each features as feature, index}
				<div
					class="group rounded-2xl border border-zinc-200 bg-white p-6 shadow-sm transition-all duration-300 hover:-translate-y-1 hover:border-emerald-300 hover:shadow-lg hover:shadow-emerald-500/5 dark:border-zinc-800 dark:bg-zinc-950 dark:hover:border-emerald-500/30"
				>
					<div class="flex items-start justify-between">
						<div
							class="flex h-11 w-11 items-center justify-center rounded-xl bg-emerald-500/10 text-lg font-bold text-emerald-500 transition-transform duration-300 group-hover:scale-110"
						>
							{feature.icon}
						</div>

						<span class="text-xs font-bold text-zinc-300 dark:text-zinc-700">
							0{index + 1}
						</span>
					</div>

					<h3 class="mt-5 text-base font-bold text-zinc-900 dark:text-white">
						{feature.title}
					</h3>

					<p class="mt-2 text-sm leading-6 text-zinc-600 dark:text-zinc-400">
						{feature.description}
					</p>
				</div>
			{/each}
		</div>
	</section>

	<!-- How it works -->
	<section id="workflow" class="scroll-mt-24">
		<div
			class="overflow-hidden rounded-3xl border border-zinc-200 bg-white dark:border-zinc-800 dark:bg-zinc-950"
		>
			<div class="p-6 sm:p-8">
				<p class="text-xs font-bold uppercase tracking-[0.18em] text-emerald-500">
					How It Works
				</p>

				<h2 class="mt-2 text-2xl font-bold text-zinc-950 dark:text-white sm:text-3xl">
					From location to insight
				</h2>

				<p class="mt-2 max-w-2xl text-sm leading-6 text-zinc-600 dark:text-zinc-400">
					AeriQ organizes environmental information into a simple monitoring workflow.
				</p>
			</div>

			<div class="grid border-t border-zinc-200 dark:border-zinc-800 md:grid-cols-4">
				{#each workflow as step, index}
					<div
						class="relative border-b border-zinc-200 p-6 last:border-b-0 dark:border-zinc-800 md:border-b-0 md:border-r md:last:border-r-0"
					>
						<div class="flex items-center justify-between">
							<span
								class="text-xs font-extrabold tracking-wider text-emerald-500"
							>
								{step.number}
							</span>

							{#if index < workflow.length - 1}
								<span class="hidden text-zinc-300 dark:text-zinc-700 md:block">→</span>
							{/if}
						</div>

						<h3 class="mt-5 text-base font-bold text-zinc-900 dark:text-white">
							{step.title}
						</h3>

						<p class="mt-2 text-sm leading-6 text-zinc-600 dark:text-zinc-400">
							{step.description}
						</p>
					</div>
				{/each}
			</div>
		</div>
	</section>

	<!-- Technology -->
	<section id="technology" class="scroll-mt-24">
		<div class="grid gap-5 lg:grid-cols-[0.9fr_1.1fr]">
			<div
				class="rounded-3xl border border-zinc-200 bg-zinc-950 p-7 text-white dark:border-zinc-800 sm:p-8"
			>
				<div
					class="flex h-12 w-12 items-center justify-center rounded-2xl bg-emerald-500/10 text-xl text-emerald-400"
				>
					&lt;/&gt;
				</div>

				<h2 class="mt-6 text-2xl font-bold">
					Technology behind AeriQ
				</h2>

				<p class="mt-3 text-sm leading-7 text-zinc-400">
					The platform combines a modern web interface with environmental data,
					API integrations, visualizations, and structured information processing.
				</p>

				<div class="mt-6 flex flex-wrap gap-2">
					{#each technologies as technology}
						<span
							class="rounded-full border border-zinc-700 bg-zinc-900 px-3 py-1.5 text-xs font-semibold text-zinc-300"
						>
							{technology}
						</span>
					{/each}
				</div>
			</div>

			<div
				class="rounded-3xl border border-zinc-200 bg-zinc-50 p-7 dark:border-zinc-800 dark:bg-zinc-900/50 sm:p-8"
			>
				<p class="text-xs font-bold uppercase tracking-[0.18em] text-emerald-500">
					Designed For
				</p>

				<div class="mt-5 grid gap-4 sm:grid-cols-2">
					<div
						class="rounded-2xl border border-zinc-200 bg-white p-5 dark:border-zinc-800 dark:bg-zinc-950"
					>
						<div class="text-lg">◉</div>
						<h3 class="mt-3 font-bold text-zinc-900 dark:text-white">
							Everyday Users
						</h3>
						<p class="mt-2 text-sm leading-6 text-zinc-600 dark:text-zinc-400">
							Understand current and upcoming environmental conditions around you.
						</p>
					</div>

					<div
						class="rounded-2xl border border-zinc-200 bg-white p-5 dark:border-zinc-800 dark:bg-zinc-950"
					>
						<div class="text-lg">♡</div>
						<h3 class="mt-3 font-bold text-zinc-900 dark:text-white">
							Health-Conscious Users
						</h3>
						<p class="mt-2 text-sm leading-6 text-zinc-600 dark:text-zinc-400">
							Use air-quality context to make more informed daily decisions.
						</p>
					</div>

					<div
						class="rounded-2xl border border-zinc-200 bg-white p-5 dark:border-zinc-800 dark:bg-zinc-950"
					>
						<div class="text-lg">⌁</div>
						<h3 class="mt-3 font-bold text-zinc-900 dark:text-white">
							Researchers & Analysts
						</h3>
						<p class="mt-2 text-sm leading-6 text-zinc-600 dark:text-zinc-400">
							Review environmental trends through structured information and reports.
						</p>
					</div>

					<div
						class="rounded-2xl border border-zinc-200 bg-white p-5 dark:border-zinc-800 dark:bg-zinc-950"
					>
						<div class="text-lg">⌖</div>
						<h3 class="mt-3 font-bold text-zinc-900 dark:text-white">
							Location Monitoring
						</h3>
						<p class="mt-2 text-sm leading-6 text-zinc-600 dark:text-zinc-400">
							Keep track of locations that matter to you through saved cities and maps.
						</p>
					</div>
				</div>
			</div>
		</div>
	</section>

	<!-- Data & Reliability -->
	<section
		class="rounded-3xl border border-amber-200 bg-amber-50 p-6 dark:border-amber-500/20 dark:bg-amber-500/5 sm:p-8"
	>
		<div class="flex gap-4">
			<div
				class="flex h-11 w-11 shrink-0 items-center justify-center rounded-xl bg-amber-100 text-lg text-amber-700 dark:bg-amber-500/10 dark:text-amber-400"
			>
				!
			</div>

			<div>
				<h2 class="font-bold text-zinc-900 dark:text-white">
					About AeriQ's information
				</h2>

				<p class="mt-2 text-sm leading-6 text-zinc-700 dark:text-zinc-400">
					AeriQ presents environmental information based on the data available to the
					application. Air-quality measurements and forecasts can change over time and may
					vary by location and data source.
				</p>

				<p class="mt-3 text-sm leading-6 text-zinc-700 dark:text-zinc-400">
					Health-related information provided by AeriQ is intended for awareness and
					informational purposes and should not be treated as a substitute for professional
					medical advice.
				</p>
			</div>
		</div>
	</section>

	<!-- Footer CTA -->
	<section
		class="relative overflow-hidden rounded-3xl bg-emerald-500 p-7 text-white shadow-xl shadow-emerald-500/10 sm:p-10"
	>
		<div
			class="pointer-events-none absolute -right-16 -top-20 h-56 w-56 rounded-full bg-white/10 blur-2xl"
		></div>

		<div class="relative flex flex-col gap-6 lg:flex-row lg:items-center lg:justify-between">
			<div>
				<p class="text-xs font-bold uppercase tracking-[0.18em] text-emerald-100">
					AeriQ
				</p>

				<h2 class="mt-2 text-2xl font-extrabold sm:text-3xl">
					Understand the air around you.
				</h2>

				<p class="mt-2 max-w-xl text-sm leading-6 text-emerald-50">
					Monitor. Understand. Prepare. Make environmental information part of your everyday
					awareness.
				</p>
			</div>

			<a
				href="/dashboard"
				class="inline-flex w-fit items-center rounded-xl bg-white px-5 py-3 text-sm font-bold text-emerald-700 shadow-lg transition-all hover:-translate-y-0.5 hover:bg-emerald-50"
			>
				Go to Dashboard
				<span class="ml-2">→</span>
			</a>
		</div>
	</section>

	<!-- Bottom -->
	<div class="pb-2 text-center">
		<p class="text-xs text-zinc-500 dark:text-zinc-600">
			AeriQ • Breathe Better. Live Better.
		</p>
	</div>
</div>

<style>
	:global(html) {
		scroll-behavior: smooth;
	}

	.active-tab {
		background: rgb(16 185 129 / 0.1);
		color: rgb(16 185 129);
	}

	:global(.dark) .active-tab {
		background: rgb(16 185 129 / 0.12);
		color: rgb(52 211 153);
	}

	@media (prefers-reduced-motion: reduce) {
		:global(html) {
			scroll-behavior: auto;
		}
	}
</style>