<script lang="ts">
	import Button from '$lib/components/shared/Button.svelte';
	import Dropdown from '$lib/components/shared/Dropdown.svelte';
	import Input from '$lib/components/shared/Input.svelte';
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
	<Dropdown id="processor" label="Payment processor" bind:value={processor}>
		<option value="None">None</option>
		<option value={PaymentProcessor.PAYPAL}>PayPal</option>
	</Dropdown>
	{#if processor === PaymentProcessor.PAYPAL}
		{#if data.paypalConfigured}
			<p>PayPal credentials are configured. Leave both fields blank to keep them, or enter both to replace them.</p>
		{/if}
		<Input id="client_id" label="PayPal client ID" autocomplete="off" value={form?.clientId ?? ''} required={!data.paypalConfigured} />
		<Input id="client_secret" label="PayPal client secret" type="password" autocomplete="new-password" value="" required={!data.paypalConfigured} />
	{/if}
	<Button type="submit">Save payment settings</Button>
</form>

<style>
	form {
		display: flex;
		flex-direction: column;
		align-items: flex-start;
		gap: 0.75rem;
		width: 100%;
		max-width: 30rem;
	}
</style>
