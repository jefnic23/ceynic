<script lang="ts">
	import { PUBLIC_API_URL, PUBLIC_MEASUREMENT_ID } from '$env/static/public';
	import { loadScript } from '@paypal/paypal-js';
	import { PaymentProcessor } from '$lib/enums/paymentProcessor';
	import { providePayPal, type PayPalState } from '$lib/state/paypal';
	import { page } from '$app/state';
	import type { PageData } from './$types';
	import Footer from '$lib/components/Footer.svelte';
	import { afterNavigate, onNavigate } from '$app/navigation';
	import { onMount } from 'svelte';
	import EcommHeader from '$lib/components/ecomm/EcommHeader.svelte';
	import GoogleAnalytics from '$lib/components/GoogleAnalytics.svelte';
	import type { Snippet } from 'svelte';

	onMount(() => {
		data.pinterestEnabled.then((enabled) => {
			if (!enabled) return;

			// Pinterest injects scripts into the document; wait until Svelte has hydrated the head.
			if (document.querySelector('script[src="https://assets.pinterest.com/js/pinit.js"]')) return;

			const script = document.createElement('script');
			script.src = 'https://assets.pinterest.com/js/pinit.js';
			script.async = true;
			script.dataset.pinHover = 'true';
			script.dataset.pinSticky = 'false';
			script.onload = () => window.PinUtils?.build();
			document.body.appendChild(script);
		});
	});

	afterNavigate(async () => {
		if (await data.pinterestEnabled) window.PinUtils?.build();
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
	const paypal = $state<PayPalState>({ sdk: null, error: false });
	providePayPal(paypal);

	onMount(() => {
		let cancelled = false;
		async function initializePayPal() {
			try {
				if (data.paymentProcessor !== PaymentProcessor.PAYPAL) return;

				const response = await fetch(`${PUBLIC_API_URL}/settings/paypalClientId`);
				if (!response.ok) throw new Error('Unable to load PayPal client ID.');
				const { clientId }: { clientId: string } = await response.json();
				if (!clientId) throw new Error('PayPal client ID is missing.');

				const sdk = await loadScript({
					clientId,
					currency: 'USD',
					dataPageType: 'checkout',
					intent: 'authorize'
				});
				if (!sdk) throw new Error('Unable to load PayPal.');
				if (!cancelled) paypal.sdk = sdk;
			} catch {
				if (!cancelled) paypal.error = true;
			}
		}

		void initializePayPal();
		return () => {
			cancelled = true;
		};
	});

	let name: string = $state('');

	$effect(() => {
		data?.name?.then((value) => {
			name = value;
		});
	});
</script>

<GoogleAnalytics measurementId={PUBLIC_MEASUREMENT_ID} />

<div class="wrapper">
	<EcommHeader url={page.url} {name} paymentProcessor={data.paymentProcessor} />

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
