<script lang="ts">
	import { PUBLIC_MEASUREMENT_ID, PUBLIC_PAYPAL_CLIENT_ID } from '$env/static/public';
	import { loadScript } from '@paypal/paypal-js';
	import { page } from '$app/state';
	import type { PageData } from './$types';
	import Footer from '$lib/components/Footer.svelte';
	import { afterNavigate, onNavigate } from '$app/navigation';
	import { onMount, setContext } from 'svelte';
	import EcommHeader from '$lib/components/ecomm/EcommHeader.svelte';
	import GoogleAnalytics from '$lib/components/GoogleAnalytics.svelte';
	import type { Snippet } from 'svelte';
	import { paypalContextKey, type PayPalContext } from '$lib/state/paypalContext';

	const paypalContext: PayPalContext = $state({ paypal: null });
	setContext(paypalContextKey, paypalContext);

	onMount(async () => {
		try {
			paypalContext.paypal = await loadScript({
				clientId: PUBLIC_PAYPAL_CLIENT_ID,
				currency: 'USD',
				dataPageType: 'checkout',
				intent: 'authorize'
				// debug: true
				// todo: add merchantId
			});
		} catch (error) {
			// todo: log error and show something in the UI
		}
	});

	onMount(() => {
		// Pinterest injects scripts into the document; wait until Svelte has hydrated the head.
		if (document.querySelector('script[src="https://assets.pinterest.com/js/pinit.js"]')) return;

		const script = document.createElement('script');
		script.src = 'https://assets.pinterest.com/js/pinit.js';
		script.async = true;
		script.dataset.pinHover = 'true';
		script.dataset.pinSticky = 'false';
		document.body.appendChild(script);
	});

	afterNavigate(() => {
		window.PinUtils?.build();
	});

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
