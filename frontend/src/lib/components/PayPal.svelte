<script lang="ts">
	import { type PayPalNamespace } from '@paypal/paypal-js';
	import { PUBLIC_API_URL } from '$env/static/public';

	interface Props {
		paypal: PayPalNamespace | null;
		productIds: number[];
		confirmOrder: CallableFunction;
		onConflict: () => Promise<void>;
	}

	let { paypal, productIds, confirmOrder, onConflict }: Props = $props();
	let checkoutError: string | null = $state(null);

	$effect(() => {
		if (paypal) renderButtons();
	})

	async function renderButtons () {
		if (!paypal?.Buttons) return;

		try {
			await paypal?.Buttons({
					onError: () => {
						checkoutError ??= 'Unable to complete checkout. Please try again.';
					},
					onShippingChange: (_, actions) => {
						return actions.resolve();
					},
					createOrder: async () => {
						checkoutError = null;
						const response = await fetch(`${PUBLIC_API_URL}/orders`, {
							method: 'POST',
							headers: {
								'Content-Type': 'application/json'
							},
							body: JSON.stringify({ product_ids: productIds })
						});

						if (!response.ok) {
							if (response.status === 409) {
								checkoutError = 'An item has sold. Remove it from your cart before checking out.';
								await onConflict();
							}
							throw new Error('Error creating order.');
						}

						const json = await response.json();

						return json.orderId;
					},
					onApprove: async (data) => {
						const response = await fetch(`${PUBLIC_API_URL}/orders/${data.orderID}/authorize`, {
							method: 'POST'
						});

						if (!response.ok) {
							if (response.status === 409) {
								checkoutError = 'An item has sold. Remove it from your cart before checking out.';
								await onConflict();
							}
							throw new Error('Error authorizing order.');
						}

						confirmOrder(data.orderID);
					}
				})
				.render('#paypal-container-element');
		} catch (error) {
			checkoutError = 'Unable to load checkout. Please try again.';
		}
	};
</script>

<div id="paypal-container-element"></div>
{#if checkoutError}<p role="alert">{checkoutError}</p>{/if}
