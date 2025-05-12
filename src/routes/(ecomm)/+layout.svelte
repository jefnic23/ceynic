<script lang="ts">
	import { PUBLIC_MEASUREMENT_ID } from "$env/static/public";
	import { page } from '$app/stores';
	import type { PageData } from './$types';
	import Footer from '$lib/components/Footer.svelte';
	import { onNavigate } from '$app/navigation';
	import EcommHeader from '$lib/components/ecomm/EcommHeader.svelte';
	import GoogleAnalytics from '$lib/components/GoogleAnalytics.svelte';

	onNavigate((navigation) => {
		if (!document.startViewTransition) return;

		return new Promise((resolve) => {
			document.startViewTransition(async () => {
				resolve();
				await navigation.complete;
			});
		});
	});

	export let data: PageData;

	let namePromise: Promise<string> = data.name;
	let name: string = "";

	$: if (namePromise) {
		namePromise.then((value) => {
			name = value;
		});
	}
</script>

<GoogleAnalytics measurementId={PUBLIC_MEASUREMENT_ID} />

<div class="wrapper">
	<EcommHeader url={$page.url} name={name} />

	{#key data.url}
		<main>
			<slot />
		</main>
	{/key}

	<Footer copyright={name} />
</div>

<style>
	main {
		position: relative;
		display: flex;
		justify-content: center;
		flex: 1;
		padding: 2rem;
	}

	.wrapper {
		min-height: 100svh;
		display: flex;
		flex-direction: column;
		justify-content: space-between;
	}
</style>
