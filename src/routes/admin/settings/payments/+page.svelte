<script lang="ts">
	import { PaymentProcessor } from '$lib/enums/paymentProcessor';
	import type { ActionData, PageData } from './$types';

	let { data, form }: { data: PageData; form: ActionData } = $props();
	let processor = $state(form?.processor ?? (data.processor === PaymentProcessor.PAYPAL ? PaymentProcessor.PAYPAL : 'None'));
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
	{#if form?.message}
		<p role="alert">{form.message}</p>
	{:else if form?.success}
		<p role="status">Payment settings saved.</p>
	{/if}
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
