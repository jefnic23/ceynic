<script lang="ts">
	import { loadScript } from '@paypal/paypal-js';
	import { createEventDispatcher, onMount } from 'svelte';
	import { PUBLIC_PAYPAL_CLIENT_ID, PUBLIC_API_URL } from '$env/static/public';

	export let productIds: number[];

	const dispatch = createEventDispatcher<{
		confirm_order: string
	}>();

	onMount(async () => {
		let paypal;

		try {
			paypal = await loadScript({
				clientId: PUBLIC_PAYPAL_CLIENT_ID,
				currency: 'USD',
				disableFunding: 'venmo',
				dataPageType: 'checkout',
				intent: 'authorize'
				// debug: true
			});
		} catch (error) {
			// todo: log error and show something in the UI
		}

		if (!paypal || !paypal.Buttons) {
			// todo: add logic for skeleton buttons
			return;
		}

		try {
			await paypal
				.Buttons({
					onShippingChange: function (_, actions) {
						return actions.resolve();
					},
					createOrder: async function () {
						const response = await fetch(`${PUBLIC_API_URL}/orders`, {
							method: 'POST',
							headers: {
								'Content-Type': 'application/json'
							},
							body: JSON.stringify({ product_ids: productIds })
						});

						if (!response.ok) {
							console.log('Error creating order.');
						}

						const json = await response.json();

						return json.orderId;
					},
					onApprove: async function (data, _) {
						const response = await fetch(`${PUBLIC_API_URL}/orders/${data.orderID}/authorize`, {
							method: 'POST',
							headers: {
								'Content-Type': 'application/json'
							},
							body: JSON.stringify({ product_ids: productIds })
						});

						if (!response.ok) {
							console.log('Error creating order.');
							// todo: raise exception
						}

						const json = await response.json();

						console.log(json);

						dispatch("confirm_order", data.orderID);
					}
					// onApprove: function(data, actions) {
					// 	const CAPTURE_ORDER_URL = '{{ url_for("main.capture_order", order_id="order_id") }}'.replace('order_id', data.orderID);
					// 	return fetch(CAPTURE_ORDER_URL, {
					// 		method: "POST",
					// 		headers: {
					// 			'Content-Type': 'application/json'
					// 		},
					// 		body: JSON.stringify({
					// 			'id': {{data.id}}
					// 		})
					// 	}).then((res) => {
					// 		return res.json();
					// 	}).then((orderData) => {
					// 		var errorDetail = Array.isArray(orderData.details) && orderData.details[0];

					// 		if (errorDetail && errorDetail.issue === 'INSTRUMENT_DECLINED') {
					// 			return actions.restart();
					// 		}

					// 		if (errorDetail) {
					// 			var msg = 'Sorry, your transaction could not be processed.';
					// 			if (errorDetail.description) msg += '\n\n' + errorDetail.description;
					// 			if (orderData.debug_id) msg += ' (' + orderData.debug_id + ')';
					// 			return alert(msg);
					// 		}

					// 		actions.redirect('{{ url_for("main.order_confirmation", purchase_id="purchase_id", _external=True) }}'.replace('purchase_id', orderData.purchase_id));
					// 	});
					// }
				})
				.render('#paypal-container-element');
		} catch (error) {
			// log error and show something in the UI
		}
	});
</script>

<div id="paypal-container-element"></div>
