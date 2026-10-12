<script lang="ts">
	import { PaymentProcessor } from '$lib/enums/paymentProcessor';
	import { useToast } from '$lib/state/toast';
	import type { ActionData, PageData } from './$types';

	let { data, form }: { data: PageData; form: ActionData } = $props();
	let processor = $state(form?.processor ?? (data.processor === PaymentProcessor.PAYPAL ? PaymentProcessor.PAYPAL : 'None'));
	const showToast = useToast();

	$effect(() => {
		if (form?.message) {
			showToast({ type: 'error', title: 'Payment settings update failed', message: form.message });
		} else if (form?.success) {
			showToast({
				type: 'success',
				title: 'Payment settings saved',
				message: 'Your payment settings have been updated.'
			});
		}
	});
</script>

<form method="POST">
	<label for="processor">Payment processor</label>
	<select id="processor" name="processor" bind:value={processor}>
		<option value="None">None</option>
		<option value={PaymentProcessor.PAYPAL}>PayPal</option>
	</select>
	{#if processor === PaymentProcessor.PAYPAL}
		{#if data.paypalConfigured}
			<p>PayPal credentials are configured. Leave both fields blank to keep them, or enter both to replace them.</p>
		{/if}
		<label for="client_id">PayPal client ID</label>
		<input id="client_id" name="client_id" autocomplete="off" value={form?.clientId ?? ''} required={!data.paypalConfigured} />
		<label for="client_secret">PayPal client secret</label>
		<input id="client_secret" name="client_secret" type="password" autocomplete="new-password" required={!data.paypalConfigured} />
	{/if}
	<button type="submit">Save payment settings</button>
</form>

<style>
	form {
		display: flex;
		flex-direction: column;
		align-items: flex-start;
		gap: 0.75rem;
	}

	input,
	select {
		max-width: 100%;
	}

	button {
		margin-top: 0.5rem;
	}
</style>
