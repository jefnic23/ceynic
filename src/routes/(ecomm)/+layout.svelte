<script lang="ts">
	import { PUBLIC_MEASUREMENT_ID } from '$env/static/public';
	import { page } from '$app/state';
	import type { PageData } from './$types';
	import Footer from '$lib/components/Footer.svelte';
	import { onNavigate } from '$app/navigation';
	import EcommHeader from '$lib/components/ecomm/EcommHeader.svelte';
	import GoogleAnalytics from '$lib/components/GoogleAnalytics.svelte';
	import type { Snippet } from 'svelte';

	onNavigate((navigation) => {
		if (!document?.startViewTransition) return;

		return new Promise((resolve) => {
			document?.startViewTransition(async () => {
				resolve();
				await navigation.complete;
			});
		});
	});

	interface Props {
		data: PageData;
		children?: Snippet;
	}

	let { data, children }: Props = $props();

	let name: string = $state('');

	$effect(() => {
		data?.name?.then((value) => {
			name = value;
		});
	});
</script>

<GoogleAnalytics measurementId={PUBLIC_MEASUREMENT_ID} />

<div class="wrapper">
	<EcommHeader url={page.url} {name} />

	{#key data.url}
		<main>
			{@render children?.()}
		</main>
	{/key}

	{#await data.socialMediaLinks}
		<Footer copyright={name} />
	{:then socialMediaLinks}
		<Footer copyright={name} {socialMediaLinks} />
	{/await}
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
