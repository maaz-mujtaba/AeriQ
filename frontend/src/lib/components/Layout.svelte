<script>
	import Sidebar from './Sidebar.svelte';
	import Navbar from './Navbar.svelte';
	import { onMount } from 'svelte';

	let { children } = $props();

	// Sidebar & Theme States
	let isCollapsed = $state(false);
	let isMobileOpen = $state(false);
	let isDark = $state(false);

	onMount(() => {
		// Dark mode setup
		const savedTheme = localStorage.getItem('theme');
		const systemPrefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;

		if (savedTheme === 'dark' || (!savedTheme && systemPrefersDark)) {
			isDark = true;
			document.documentElement.classList.add('dark');
		} else {
			isDark = false;
			document.documentElement.classList.remove('dark');
		}

		// Responsive layout hook
		let lastCollapsed = isCollapsed;
		const handleResize = () => {
			const width = window.innerWidth;
			const nextCollapsed = width >= 768 && width < 1024;
			if (nextCollapsed !== lastCollapsed) {
				isCollapsed = nextCollapsed;
				lastCollapsed = nextCollapsed;
			}
		};

		// Run initially
		handleResize();

		window.addEventListener('resize', handleResize);
		return () => {
			window.removeEventListener('resize', handleResize);
		};
	});
</script>

<div class="min-h-screen bg-gradient-to-br from-sky-50/40 via-zinc-50 to-emerald-50/20 dark:from-zinc-950 dark:via-zinc-900/60 dark:to-emerald-950/20 text-zinc-900 dark:text-zinc-50 transition-colors duration-300 relative overflow-hidden">
	<!-- Blurred ambient background shapes -->
	<div class="absolute inset-0 pointer-events-none overflow-hidden z-0 opacity-40 dark:opacity-20">
		<div class="absolute -top-[15%] -left-[10%] w-[45%] h-[45%] rounded-full bg-sky-200/40 blur-[130px]"></div>
		<div class="absolute -bottom-[20%] -right-[10%] w-[50%] h-[50%] rounded-full bg-emerald-200/30 blur-[130px]"></div>
	</div>

	<!-- Reusable Sidebar -->
	<Sidebar bind:isCollapsed bind:isMobileOpen bind:isDark />

	<!-- Layout Content Area -->
	<div
		class="min-h-screen flex flex-col transition-all duration-300 ease-in-out relative z-10
			{isCollapsed ? 'lg:pl-16' : 'lg:pl-64'}"
	>
		<!-- Reusable Navbar -->
		<Navbar bind:isCollapsed bind:isMobileOpen />

		<!-- Main Page Slot -->
		<main class="flex-1 p-4 md:p-6 lg:p-8 max-w-7xl w-full mx-auto space-y-6 focus:outline-none">
			{@render children()}
		</main>
	</div>
</div>
