<script>
    import { loggedIn } from '$lib/stores/authStore.js';
    import LoginRequired from '$lib/components/LoginRequired.svelte';

    let reportType = 'Air Quality Summary';
    let selectedCity = 'New Delhi, India';
    let dateRange = 'Last 30 Days';
    let format = 'PDF';

    let generating = false;
    let showSuccess = false;

    let reports = [
        {
            id: 1,
            name: 'New Delhi Air Quality Summary',
            type: 'Air Quality Summary',
            date: '29 Sep 2026',
            range: 'Last 30 Days',
            format: 'PDF',
            size: '2.4 MB'
        },
        {
            id: 2,
            name: 'Weekly AQI Analysis',
            type: 'AQI Analysis',
            date: '27 Sep 2026',
            range: 'Last 7 Days',
            format: 'CSV',
            size: '486 KB'
        },
        {
            id: 3,
            name: 'Health Impact Report',
            type: 'Health Impact',
            date: '24 Sep 2026',
            range: 'Last 30 Days',
            format: 'PDF',
            size: '1.8 MB'
        },
        {
            id: 4,
            name: 'Pollution Trend Report',
            type: 'Pollution Trends',
            date: '20 Sep 2026',
            range: 'Last 90 Days',
            format: 'JSON',
            size: '732 KB'
        }
    ];

    const reportTypes = [
        'Air Quality Summary',
        'AQI Analysis',
        'Pollution Trends',
        'Health Impact',
        'Forecast Summary'
    ];

    const cities = [
        'New Delhi, India',
        'Mumbai, India',
        'Bengaluru, India',
        'Chennai, India',
        'Kolkata, India',
        'Hyderabad, India'
    ];

    const ranges = [
        'Last 7 Days',
        'Last 30 Days',
        'Last 90 Days',
        'Last 6 Months',
        'This Year'
    ];

    function generateReport() {
        generating = true;
        showSuccess = false;

        setTimeout(() => {
            const newReport = {
                id: Date.now(),
                name: `${selectedCity.split(',')[0]} ${reportType}`,
                type: reportType,
                date: new Date().toLocaleDateString('en-GB', {
                    day: '2-digit',
                    month: 'short',
                    year: 'numeric'
                }),
                range: dateRange,
                format: format,
                size: format === 'PDF' ? '1.9 MB' : format === 'CSV' ? '512 KB' : '680 KB'
            };

            reports = [newReport, ...reports];
            generating = false;
            showSuccess = true;

            setTimeout(() => {
                showSuccess = false;
            }, 4000);
        }, 1200);
    }

    function deleteReport(id) {
        reports = reports.filter((report) => report.id !== id);
    }

    function downloadReport(report) {
        let content = '';

        if (report.format === 'JSON') {
            content = JSON.stringify(
                {
                    report: report.name,
                    city: selectedCity,
                    type: report.type,
                    dateRange: report.range,
                    generated: report.date,
                    aqi: 142,
                    pm25: 68,
                    pm10: 121,
                    ozone: 74,
                    no2: 39
                },
                null,
                2
            );
        } else {
            content =
                `AeriQ Report\n\n` +
                `Report: ${report.name}\n` +
                `Type: ${report.type}\n` +
                `Date: ${report.date}\n` +
                `Range: ${report.range}\n\n` +
                `AQI: 142\n` +
                `PM2.5: 68 µg/m³\n` +
                `PM10: 121 µg/m³\n` +
                `O₃: 74 µg/m³\n` +
                `NO₂: 39 µg/m³\n`;
        }

        const blob = new Blob([content], {
            type: report.format === 'JSON'
                ? 'application/json'
                : 'text/plain'
        });

        const url = URL.createObjectURL(blob);
        const link = document.createElement('a');

        link.href = url;
        link.download = `${report.name.replace(/\s+/g, '_')}.${report.format.toLowerCase()}`;
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);

        URL.revokeObjectURL(url);
    }
</script>

<svelte:head>
    <title>Reports | AeriQ</title>
    <meta
        name="description"
        content="Generate, manage and download air-quality reports with AeriQ."
    />
</svelte:head>

{#if !$loggedIn}
    <LoginRequired
        title="Reports Manager"
        description="Generate, manage and download customized air-quality reports."
    />
{:else}

    <div class="space-y-6 pb-10">

        <!-- PAGE HEADER -->
        <div class="space-y-2">
            <div
                class="flex items-center gap-2 text-xs font-semibold uppercase tracking-[0.18em]
                text-zinc-400 dark:text-zinc-500"
            >
                <span>APP</span>
                <span>/</span>
                <span class="text-emerald-500 dark:text-emerald-400">
                    REPORTS
                </span>
            </div>

            <div class="flex flex-col gap-4 lg:flex-row lg:items-end lg:justify-between">
                <div>
                    <h1
                        class="text-3xl font-extrabold tracking-tight
                        text-zinc-950 dark:text-white"
                    >
                        Reports
                    </h1>

                    <p
                        class="mt-1 max-w-2xl text-sm
                        text-zinc-600 dark:text-zinc-400"
                    >
                        Generate, analyze and download structured air-quality
                        reports for your monitored cities.
                    </p>
                </div>

                <div
                    class="flex items-center gap-2 rounded-xl border
                    border-zinc-200 bg-white px-3 py-2 text-xs
                    shadow-sm dark:border-zinc-800 dark:bg-zinc-900"
                >
                    <span
                        class="h-2 w-2 rounded-full bg-emerald-500
                        shadow-[0_0_10px_rgba(16,185,129,0.7)]"
                    ></span>

                    <span class="text-zinc-600 dark:text-zinc-400">
                        Monitoring Active
                    </span>
                </div>
            </div>
        </div>


        <!-- SUCCESS MESSAGE -->
        {#if showSuccess}
            <div
                class="flex items-center gap-3 rounded-xl border
                border-emerald-200 bg-emerald-50 px-4 py-3
                text-sm text-emerald-700
                dark:border-emerald-900/60 dark:bg-emerald-950/30
                dark:text-emerald-400"
            >
                <div
                    class="flex h-7 w-7 items-center justify-center
                    rounded-full bg-emerald-500 text-white"
                >
                    ✓
                </div>

                <div>
                    <p class="font-semibold">
                        Report generated successfully
                    </p>

                    <p class="text-xs opacity-80">
                        Your report has been added to Recent Reports.
                    </p>
                </div>
            </div>
        {/if}


        <!-- REPORT GENERATOR -->
        <section
            class="overflow-hidden rounded-2xl border
            border-zinc-200 bg-white shadow-sm
            dark:border-zinc-800 dark:bg-zinc-900/70"
        >

            <!-- CARD HEADER -->
            <div
                class="border-b border-zinc-200 px-6 py-5
                dark:border-zinc-800"
            >
                <div class="flex items-center gap-3">

                    <div
                        class="flex h-11 w-11 items-center justify-center
                        rounded-xl bg-emerald-500/10
                        text-emerald-500 dark:text-emerald-400"
                    >
                        <svg
                            viewBox="0 0 24 24"
                            fill="none"
                            stroke="currentColor"
                            stroke-width="1.8"
                            class="h-6 w-6"
                        >
                            <path
                                d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"
                            />
                            <path d="M14 2v6h6" />
                            <path d="M8 13h8M8 17h5" />
                        </svg>
                    </div>

                    <div>
                        <h2
                            class="font-bold text-zinc-900 dark:text-white"
                        >
                            Generate New Report
                        </h2>

                        <p
                            class="text-xs text-zinc-500
                            dark:text-zinc-400"
                        >
                            Configure your report parameters and export
                            the latest air-quality data.
                        </p>
                    </div>
                </div>
            </div>


            <!-- FORM -->
            <div class="grid gap-5 p-6 md:grid-cols-2 xl:grid-cols-4">

                <!-- REPORT TYPE -->
                <div>
                    <label
                        for="reportType"
                        class="mb-2 block text-xs font-semibold
                        text-zinc-600 dark:text-zinc-400"
                    >
                        Report Type
                    </label>

                    <select
                        id="reportType"
                        bind:value={reportType}
                        class="w-full rounded-xl border
                        border-zinc-200 bg-zinc-50 px-4 py-3
                        text-sm text-zinc-900 outline-none
                        transition focus:border-emerald-500
                        focus:ring-2 focus:ring-emerald-500/10
                        dark:border-zinc-700 dark:bg-zinc-950
                        dark:text-white"
                    >
                        {#each reportTypes as type}
                            <option value={type}>{type}</option>
                        {/each}
                    </select>
                </div>


                <!-- CITY -->
                <div>
                    <label
                        for="city"
                        class="mb-2 block text-xs font-semibold
                        text-zinc-600 dark:text-zinc-400"
                    >
                        Location
                    </label>

                    <select
                        id="city"
                        bind:value={selectedCity}
                        class="w-full rounded-xl border
                        border-zinc-200 bg-zinc-50 px-4 py-3
                        text-sm text-zinc-900 outline-none
                        transition focus:border-emerald-500
                        focus:ring-2 focus:ring-emerald-500/10
                        dark:border-zinc-700 dark:bg-zinc-950
                        dark:text-white"
                    >
                        {#each cities as city}
                            <option value={city}>{city}</option>
                        {/each}
                    </select>
                </div>


                <!-- DATE RANGE -->
                <div>
                    <label
                        for="dateRange"
                        class="mb-2 block text-xs font-semibold
                        text-zinc-600 dark:text-zinc-400"
                    >
                        Date Range
                    </label>

                    <select
                        id="dateRange"
                        bind:value={dateRange}
                        class="w-full rounded-xl border
                        border-zinc-200 bg-zinc-50 px-4 py-3
                        text-sm text-zinc-900 outline-none
                        transition focus:border-emerald-500
                        focus:ring-2 focus:ring-emerald-500/10
                        dark:border-zinc-700 dark:bg-zinc-950
                        dark:text-white"
                    >
                        {#each ranges as range}
                            <option value={range}>{range}</option>
                        {/each}
                    </select>
                </div>


                <!-- FORMAT -->
                <div>
                    <label
                        class="mb-2 block text-xs font-semibold
                        text-zinc-600 dark:text-zinc-400"
                    >
                        Export Format
                    </label>

                    <div class="grid grid-cols-3 gap-2">
                        {#each ['PDF', 'CSV', 'JSON'] as item}
                            <button
                                type="button"
                                onclick={() => (format = item)}
                                class={`rounded-xl border px-3 py-3 text-xs font-bold
                                transition ${
                                    format === item
                                        ? 'border-emerald-500 bg-emerald-500 text-white shadow-sm'
                                        : 'border-zinc-200 bg-zinc-50 text-zinc-600 hover:border-emerald-300 dark:border-zinc-700 dark:bg-zinc-950 dark:text-zinc-400'
                                }`}
                            >
                                {item}
                            </button>
                        {/each}
                    </div>
                </div>

            </div>


            <!-- GENERATE BUTTON -->
            <div
                class="flex flex-col gap-3 border-t
                border-zinc-200 bg-zinc-50 px-6 py-4
                sm:flex-row sm:items-center sm:justify-between
                dark:border-zinc-800 dark:bg-zinc-950/40"
            >
                <div>
                    <p
                        class="text-xs font-semibold text-zinc-700
                        dark:text-zinc-300"
                    >
                        Ready to generate
                    </p>

                    <p
                        class="text-xs text-zinc-500
                        dark:text-zinc-500"
                    >
                        {reportType} · {selectedCity} · {dateRange}
                    </p>
                </div>

                <button
                    type="button"
                    onclick={generateReport}
                    disabled={generating}
                    class="inline-flex items-center justify-center
                    gap-2 rounded-xl bg-emerald-500 px-5 py-3
                    text-sm font-bold text-white shadow-sm
                    transition hover:bg-emerald-600
                    hover:shadow-md disabled:cursor-not-allowed
                    disabled:opacity-60"
                >
                    {#if generating}
                        <svg
                            class="h-4 w-4 animate-spin"
                            viewBox="0 0 24 24"
                            fill="none"
                        >
                            <circle
                                cx="12"
                                cy="12"
                                r="9"
                                stroke="currentColor"
                                stroke-width="3"
                                opacity=".25"
                            />
                            <path
                                d="M21 12a9 9 0 0 1-9 9"
                                stroke="currentColor"
                                stroke-width="3"
                            />
                        </svg>

                        Generating...
                    {:else}
                        <svg
                            viewBox="0 0 24 24"
                            fill="none"
                            stroke="currentColor"
                            stroke-width="2"
                            class="h-4 w-4"
                        >
                            <path d="M12 3v12" />
                            <path d="m7 10 5 5 5-5" />
                            <path d="M5 21h14" />
                        </svg>

                        Generate Report
                    {/if}
                </button>
            </div>

        </section>


        <!-- OVERVIEW STATISTICS -->
        <div class="grid gap-4 sm:grid-cols-2 xl:grid-cols-4">

            <!-- GENERATED -->
            <div
                class="rounded-2xl border border-zinc-200
                bg-white p-5 shadow-sm
                dark:border-zinc-800 dark:bg-zinc-900/70"
            >
                <div class="flex items-start justify-between">
                    <div>
                        <p
                            class="text-xs font-medium text-zinc-500
                            dark:text-zinc-400"
                        >
                            Reports Generated
                        </p>

                        <p
                            class="mt-2 text-3xl font-extrabold
                            text-zinc-950 dark:text-white"
                        >
                            24
                        </p>
                    </div>

                    <div
                        class="rounded-xl bg-emerald-500/10 p-3
                        text-emerald-500"
                    >
                        <svg
                            class="h-5 w-5"
                            viewBox="0 0 24 24"
                            fill="none"
                            stroke="currentColor"
                            stroke-width="1.8"
                        >
                            <path d="M4 19V5" />
                            <path d="M4 19h16" />
                            <path d="m7 15 3-4 3 2 5-7" />
                        </svg>
                    </div>
                </div>

                <p
                    class="mt-3 text-xs text-emerald-600
                    dark:text-emerald-400"
                >
                    +18% from last month
                </p>
            </div>


            <!-- AQI -->
            <div
                class="rounded-2xl border border-zinc-200
                bg-white p-5 shadow-sm
                dark:border-zinc-800 dark:bg-zinc-900/70"
            >
                <div class="flex items-start justify-between">
                    <div>
                        <p
                            class="text-xs font-medium text-zinc-500
                            dark:text-zinc-400"
                        >
                            Average AQI
                        </p>

                        <p
                            class="mt-2 text-3xl font-extrabold
                            text-zinc-950 dark:text-white"
                        >
                            142
                        </p>
                    </div>

                    <div
                        class="rounded-xl bg-orange-500/10 p-3
                        text-orange-500"
                    >
                        <svg
                            class="h-5 w-5"
                            viewBox="0 0 24 24"
                            fill="none"
                            stroke="currentColor"
                            stroke-width="1.8"
                        >
                            <path d="M12 3v18" />
                            <path d="M5 8h14" />
                            <path d="M7 4h10" />
                            <path d="M7 20h10" />
                        </svg>
                    </div>
                </div>

                <p
                    class="mt-3 text-xs text-orange-500
                    dark:text-orange-400"
                >
                    Moderate pollution level
                </p>
            </div>


            <!-- PM2.5 -->
            <div
                class="rounded-2xl border border-zinc-200
                bg-white p-5 shadow-sm
                dark:border-zinc-800 dark:bg-zinc-900/70"
            >
                <div class="flex items-start justify-between">
                    <div>
                        <p
                            class="text-xs font-medium text-zinc-500
                            dark:text-zinc-400"
                        >
                            Avg. PM2.5
                        </p>

                        <p
                            class="mt-2 text-3xl font-extrabold
                            text-zinc-950 dark:text-white"
                        >
                            68
                        </p>
                    </div>

                    <div
                        class="rounded-xl bg-blue-500/10 p-3
                        text-blue-500"
                    >
                        <span class="text-sm font-bold">µg</span>
                    </div>
                </div>

                <p
                    class="mt-3 text-xs text-zinc-500
                    dark:text-zinc-400"
                >
                    Based on selected location
                </p>
            </div>


            <!-- DATA POINTS -->
            <div
                class="rounded-2xl border border-zinc-200
                bg-white p-5 shadow-sm
                dark:border-zinc-800 dark:bg-zinc-900/70"
            >
                <div class="flex items-start justify-between">
                    <div>
                        <p
                            class="text-xs font-medium text-zinc-500
                            dark:text-zinc-400"
                        >
                            Data Points
                        </p>

                        <p
                            class="mt-2 text-3xl font-extrabold
                            text-zinc-950 dark:text-white"
                        >
                            8.4K
                        </p>
                    </div>

                    <div
                        class="rounded-xl bg-purple-500/10 p-3
                        text-purple-500"
                    >
                        <svg
                            class="h-5 w-5"
                            viewBox="0 0 24 24"
                            fill="none"
                            stroke="currentColor"
                            stroke-width="1.8"
                        >
                            <circle cx="6" cy="12" r="2" />
                            <circle cx="12" cy="6" r="2" />
                            <circle cx="18" cy="12" r="2" />
                            <path d="m7.5 10.5 3-3" />
                            <path d="m13.5 7.5 3 3" />
                        </svg>
                    </div>
                </div>

                <p
                    class="mt-3 text-xs text-zinc-500
                    dark:text-zinc-400"
                >
                    Processed successfully
                </p>
            </div>

        </div>


        <!-- REPORT CONTENT GRID -->
        <div class="grid gap-6 xl:grid-cols-[1.4fr_0.8fr]">

            <!-- AIR QUALITY SUMMARY -->
            <section
                class="rounded-2xl border border-zinc-200
                bg-white p-6 shadow-sm
                dark:border-zinc-800 dark:bg-zinc-900/70"
            >
                <div
                    class="mb-6 flex flex-col gap-3 sm:flex-row
                    sm:items-center sm:justify-between"
                >
                    <div>
                        <h2
                            class="font-bold text-zinc-900
                            dark:text-white"
                        >
                            Air Quality Summary
                        </h2>

                        <p
                            class="mt-1 text-xs text-zinc-500
                            dark:text-zinc-400"
                        >
                            Current environmental indicators for
                            {selectedCity}.
                        </p>
                    </div>

                    <span
                        class="w-fit rounded-full bg-orange-500/10
                        px-3 py-1 text-xs font-bold text-orange-500"
                    >
                        AQI 142 · Moderate
                    </span>
                </div>


                <!-- POLLUTANTS -->
                <div class="grid gap-3 sm:grid-cols-2">

                    <div
                        class="rounded-xl border border-zinc-200
                        bg-zinc-50 p-4
                        dark:border-zinc-800 dark:bg-zinc-950/50"
                    >
                        <div class="flex items-center justify-between">
                            <span
                                class="text-xs font-semibold
                                text-zinc-500 dark:text-zinc-400"
                            >
                                PM2.5
                            </span>

                            <span
                                class="text-xs font-bold
                                text-orange-500"
                            >
                                Elevated
                            </span>
                        </div>

                        <div class="mt-3 flex items-end gap-1">
                            <span
                                class="text-2xl font-extrabold
                                text-zinc-900 dark:text-white"
                            >
                                68
                            </span>

                            <span
                                class="pb-1 text-xs text-zinc-500"
                            >
                                µg/m³
                            </span>
                        </div>

                        <div
                            class="mt-3 h-1.5 overflow-hidden rounded-full
                            bg-zinc-200 dark:bg-zinc-800"
                        >
                            <div
                                class="h-full w-[68%] rounded-full
                                bg-orange-500"
                            ></div>
                        </div>
                    </div>


                    <div
                        class="rounded-xl border border-zinc-200
                        bg-zinc-50 p-4
                        dark:border-zinc-800 dark:bg-zinc-950/50"
                    >
                        <div class="flex items-center justify-between">
                            <span
                                class="text-xs font-semibold
                                text-zinc-500 dark:text-zinc-400"
                            >
                                PM10
                            </span>

                            <span
                                class="text-xs font-bold
                                text-orange-500"
                            >
                                Elevated
                            </span>
                        </div>

                        <div class="mt-3 flex items-end gap-1">
                            <span
                                class="text-2xl font-extrabold
                                text-zinc-900 dark:text-white"
                            >
                                121
                            </span>

                            <span
                                class="pb-1 text-xs text-zinc-500"
                            >
                                µg/m³
                            </span>
                        </div>

                        <div
                            class="mt-3 h-1.5 overflow-hidden rounded-full
                            bg-zinc-200 dark:bg-zinc-800"
                        >
                            <div
                                class="h-full w-[74%] rounded-full
                                bg-orange-500"
                            ></div>
                        </div>
                    </div>


                    <div
                        class="rounded-xl border border-zinc-200
                        bg-zinc-50 p-4
                        dark:border-zinc-800 dark:bg-zinc-950/50"
                    >
                        <div class="flex items-center justify-between">
                            <span
                                class="text-xs font-semibold
                                text-zinc-500 dark:text-zinc-400"
                            >
                                O₃
                            </span>

                            <span
                                class="text-xs font-bold
                                text-emerald-500"
                            >
                                Good
                            </span>
                        </div>

                        <div class="mt-3 flex items-end gap-1">
                            <span
                                class="text-2xl font-extrabold
                                text-zinc-900 dark:text-white"
                            >
                                74
                            </span>

                            <span
                                class="pb-1 text-xs text-zinc-500"
                            >
                                µg/m³
                            </span>
                        </div>

                        <div
                            class="mt-3 h-1.5 overflow-hidden rounded-full
                            bg-zinc-200 dark:bg-zinc-800"
                        >
                            <div
                                class="h-full w-[42%] rounded-full
                                bg-emerald-500"
                            ></div>
                        </div>
                    </div>


                    <div
                        class="rounded-xl border border-zinc-200
                        bg-zinc-50 p-4
                        dark:border-zinc-800 dark:bg-zinc-950/50"
                    >
                        <div class="flex items-center justify-between">
                            <span
                                class="text-xs font-semibold
                                text-zinc-500 dark:text-zinc-400"
                            >
                                NO₂
                            </span>

                            <span
                                class="text-xs font-bold
                                text-emerald-500"
                            >
                                Normal
                            </span>
                        </div>

                        <div class="mt-3 flex items-end gap-1">
                            <span
                                class="text-2xl font-extrabold
                                text-zinc-900 dark:text-white"
                            >
                                39
                            </span>

                            <span
                                class="pb-1 text-xs text-zinc-500"
                            >
                                µg/m³
                            </span>
                        </div>

                        <div
                            class="mt-3 h-1.5 overflow-hidden rounded-full
                            bg-zinc-200 dark:bg-zinc-800"
                        >
                            <div
                                class="h-full w-[28%] rounded-full
                                bg-emerald-500"
                            ></div>
                        </div>
                    </div>

                </div>
            </section>


            <!-- REPORT INSIGHTS -->
            <section
                class="rounded-2xl border border-zinc-200
                bg-white p-6 shadow-sm
                dark:border-zinc-800 dark:bg-zinc-900/70"
            >
                <div class="flex items-center gap-3">

                    <div
                        class="flex h-10 w-10 items-center justify-center
                        rounded-xl bg-emerald-500/10
                        text-emerald-500"
                    >
                        <svg
                            class="h-5 w-5"
                            viewBox="0 0 24 24"
                            fill="none"
                            stroke="currentColor"
                            stroke-width="1.8"
                        >
                            <path
                                d="M12 3a7 7 0 0 0-4 12.74V19h8v-3.26A7 7 0 0 0 12 3Z"
                            />
                            <path d="M9 22h6" />
                            <path d="M9 19h6" />
                        </svg>
                    </div>

                    <div>
                        <h2
                            class="font-bold text-zinc-900
                            dark:text-white"
                        >
                            Report Insights
                        </h2>

                        <p
                            class="text-xs text-zinc-500
                            dark:text-zinc-400"
                        >
                            Automated summary
                        </p>
                    </div>
                </div>


                <div class="mt-5 space-y-4">

                    <div class="flex gap-3">
                        <span
                            class="mt-1 h-2 w-2 shrink-0 rounded-full
                            bg-orange-500"
                        ></span>

                        <p
                            class="text-sm leading-6 text-zinc-600
                            dark:text-zinc-400"
                        >
                            PM2.5 is currently the primary contributor
                            to the overall AQI level.
                        </p>
                    </div>

                    <div class="flex gap-3">
                        <span
                            class="mt-1 h-2 w-2 shrink-0 rounded-full
                            bg-emerald-500"
                        ></span>

                        <p
                            class="text-sm leading-6 text-zinc-600
                            dark:text-zinc-400"
                        >
                            O₃ and NO₂ concentrations remain within
                            the monitored normal range.
                        </p>
                    </div>

                    <div class="flex gap-3">
                        <span
                            class="mt-1 h-2 w-2 shrink-0 rounded-full
                            bg-blue-500"
                        ></span>

                        <p
                            class="text-sm leading-6 text-zinc-600
                            dark:text-zinc-400"
                        >
                            The selected reporting period contains
                            sufficient data for trend analysis.
                        </p>
                    </div>

                </div>


                <div
                    class="mt-6 rounded-xl border
                    border-emerald-200 bg-emerald-50 p-4
                    dark:border-emerald-900/50
                    dark:bg-emerald-950/20"
                >
                    <p
                        class="text-xs font-bold text-emerald-700
                        dark:text-emerald-400"
                    >
                        AeriQ Recommendation
                    </p>

                    <p
                        class="mt-1 text-xs leading-5
                        text-emerald-700/80
                        dark:text-emerald-400/70"
                    >
                        Continue monitoring PM2.5 levels and review
                        short-term pollution trends before making
                        exposure-related decisions.
                    </p>
                </div>

            </section>

        </div>


        <!-- RECENT REPORTS -->
        <section
            class="overflow-hidden rounded-2xl border
            border-zinc-200 bg-white shadow-sm
            dark:border-zinc-800 dark:bg-zinc-900/70"
        >

            <div
                class="flex flex-col gap-3 border-b
                border-zinc-200 px-6 py-5
                sm:flex-row sm:items-center
                sm:justify-between
                dark:border-zinc-800"
            >
                <div>
                    <h2
                        class="font-bold text-zinc-900
                        dark:text-white"
                    >
                        Recent Reports
                    </h2>

                    <p
                        class="mt-1 text-xs text-zinc-500
                        dark:text-zinc-400"
                    >
                        Previously generated reports and exports.
                    </p>
                </div>

                <span
                    class="w-fit rounded-lg bg-zinc-100 px-3 py-1.5
                    text-xs font-semibold text-zinc-600
                    dark:bg-zinc-800 dark:text-zinc-400"
                >
                    {reports.length} reports
                </span>
            </div>


            <!-- DESKTOP TABLE -->
            <div class="hidden overflow-x-auto md:block">

                <table class="w-full text-left">
                    <thead
                        class="border-b border-zinc-200
                        bg-zinc-50 dark:border-zinc-800
                        dark:bg-zinc-950/40"
                    >
                        <tr>
                            <th
                                class="px-6 py-4 text-xs font-bold
                                text-zinc-500 dark:text-zinc-400"
                            >
                                REPORT
                            </th>

                            <th
                                class="px-6 py-4 text-xs font-bold
                                text-zinc-500 dark:text-zinc-400"
                            >
                                TYPE
                            </th>

                            <th
                                class="px-6 py-4 text-xs font-bold
                                text-zinc-500 dark:text-zinc-400"
                            >
                                DATE
                            </th>

                            <th
                                class="px-6 py-4 text-xs font-bold
                                text-zinc-500 dark:text-zinc-400"
                            >
                                FORMAT
                            </th>

                            <th
                                class="px-6 py-4 text-right text-xs
                                font-bold text-zinc-500
                                dark:text-zinc-400"
                            >
                                ACTIONS
                            </th>
                        </tr>
                    </thead>

                    <tbody
                        class="divide-y divide-zinc-200
                        dark:divide-zinc-800"
                    >
                        {#each reports as report}
                            <tr
                                class="transition hover:bg-zinc-50
                                dark:hover:bg-zinc-800/30"
                            >
                                <td class="px-6 py-4">
                                    <div class="flex items-center gap-3">

                                        <div
                                            class="flex h-9 w-9
                                            items-center justify-center
                                            rounded-lg bg-emerald-500/10
                                            text-emerald-500"
                                        >
                                            <svg
                                                class="h-4 w-4"
                                                viewBox="0 0 24 24"
                                                fill="none"
                                                stroke="currentColor"
                                                stroke-width="1.8"
                                            >
                                                <path
                                                    d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"
                                                />
                                                <path d="M14 2v6h6" />
                                                <path d="M8 13h8M8 17h5" />
                                            </svg>
                                        </div>

                                        <div>
                                            <p
                                                class="text-sm font-semibold
                                                text-zinc-900
                                                dark:text-white"
                                            >
                                                {report.name}
                                            </p>

                                            <p
                                                class="mt-0.5 text-xs
                                                text-zinc-500"
                                            >
                                                {report.range}
                                            </p>
                                        </div>

                                    </div>
                                </td>

                                <td
                                    class="px-6 py-4 text-sm
                                    text-zinc-600 dark:text-zinc-400"
                                >
                                    {report.type}
                                </td>

                                <td
                                    class="px-6 py-4 text-sm
                                    text-zinc-600 dark:text-zinc-400"
                                >
                                    {report.date}
                                </td>

                                <td class="px-6 py-4">
                                    <span
                                        class="rounded-lg bg-zinc-100
                                        px-2.5 py-1 text-xs font-bold
                                        text-zinc-600
                                        dark:bg-zinc-800
                                        dark:text-zinc-300"
                                    >
                                        {report.format}
                                    </span>
                                </td>

                                <td class="px-6 py-4">
                                    <div
                                        class="flex justify-end gap-2"
                                    >
                                        <button
                                            type="button"
                                            onclick={() =>
                                                downloadReport(report)
                                            }
                                            class="rounded-lg border
                                            border-zinc-200 px-3 py-2
                                            text-xs font-semibold
                                            text-zinc-700 transition
                                            hover:border-emerald-400
                                            hover:text-emerald-600
                                            dark:border-zinc-700
                                            dark:text-zinc-300
                                            dark:hover:text-emerald-400"
                                        >
                                            Download
                                        </button>

                                        <button
                                            type="button"
                                            onclick={() =>
                                                deleteReport(report.id)
                                            }
                                            class="rounded-lg px-3 py-2
                                            text-xs font-semibold
                                            text-zinc-400 transition
                                            hover:bg-red-500/10
                                            hover:text-red-500"
                                        >
                                            Delete
                                        </button>
                                    </div>
                                </td>

                            </tr>
                        {/each}
                    </tbody>
                </table>

            </div>


            <!-- MOBILE REPORT LIST -->
            <div class="divide-y divide-zinc-200 md:hidden dark:divide-zinc-800">

                {#each reports as report}
                    <div class="p-5">

                        <div class="flex items-start justify-between gap-4">

                            <div class="flex gap-3">

                                <div
                                    class="flex h-10 w-10 shrink-0
                                    items-center justify-center
                                    rounded-lg bg-emerald-500/10
                                    text-emerald-500"
                                >
                                    <svg
                                        class="h-5 w-5"
                                        viewBox="0 0 24 24"
                                        fill="none"
                                        stroke="currentColor"
                                        stroke-width="1.8"
                                    >
                                        <path
                                            d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"
                                        />
                                        <path d="M14 2v6h6" />
                                        <path d="M8 13h8M8 17h5" />
                                    </svg>
                                </div>

                                <div>
                                    <p
                                        class="text-sm font-semibold
                                        text-zinc-900
                                        dark:text-white"
                                    >
                                        {report.name}
                                    </p>

                                    <p
                                        class="mt-1 text-xs
                                        text-zinc-500"
                                    >
                                        {report.type}
                                    </p>

                                    <p
                                        class="mt-1 text-xs
                                        text-zinc-500"
                                    >
                                        {report.date} · {report.range}
                                    </p>
                                </div>

                            </div>

                            <span
                                class="rounded-lg bg-zinc-100 px-2 py-1
                                text-[10px] font-bold
                                text-zinc-600 dark:bg-zinc-800
                                dark:text-zinc-300"
                            >
                                {report.format}
                            </span>

                        </div>


                        <div class="mt-4 flex gap-2">

                            <button
                                type="button"
                                onclick={() => downloadReport(report)}
                                class="flex-1 rounded-lg border
                                border-zinc-200 px-3 py-2 text-xs
                                font-semibold text-zinc-700
                                transition hover:border-emerald-400
                                hover:text-emerald-600
                                dark:border-zinc-700
                                dark:text-zinc-300"
                            >
                                Download
                            </button>

                            <button
                                type="button"
                                onclick={() => deleteReport(report.id)}
                                class="rounded-lg border
                                border-zinc-200 px-4 py-2 text-xs
                                font-semibold text-red-500
                                transition hover:bg-red-500/10
                                dark:border-zinc-700"
                            >
                                Delete
                            </button>

                        </div>

                    </div>
                {/each}

            </div>

        </section>


        <!-- FOOTER NOTE -->
        <div
            class="flex items-start gap-3 rounded-xl border
            border-zinc-200 bg-zinc-50 p-4
            dark:border-zinc-800 dark:bg-zinc-900/40"
        >
            <svg
                class="mt-0.5 h-4 w-4 shrink-0 text-zinc-400"
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                stroke-width="1.8"
            >
                <circle cx="12" cy="12" r="9" />
                <path d="M12 10v6" />
                <path d="M12 7h.01" />
            </svg>

            <p
                class="text-xs leading-5 text-zinc-500
                dark:text-zinc-400"
            >
                Reports generated by AeriQ summarize monitored
                environmental data for the selected location and
                period. Always consider local monitoring conditions
                and official advisories when interpreting air-quality
                information.
            </p>
        </div>

    </div>

{/if}