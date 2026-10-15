<script lang="ts">
	import Card from '$lib/components/shared/Card.svelte';
	import type { Address, UnitAmount } from '$lib/interfaces/OrderDetails';
	import type { PageData } from './$types';

	let { data }: { data: PageData } = $props();

	function formatAmount(amount: UnitAmount | undefined): string {
		if (!amount) return '';
		return new Intl.NumberFormat('en-US', {
			style: 'currency',
			currency: amount.currencyCode ?? 'USD'
		}).format(Number(amount.value));
	}

	function formatAddress(address: Address): string {
		return [
			address.addressLine1,
			address.addressLine2,
			address.adminArea2,
			address.adminArea1,
			address.postalCode,
			address.countryCode
		].filter(Boolean).join(', ');
	}
</script>

<svelte:head>
	<title>Order confirmation</title>
</svelte:head>

<div class="confirmation">
	<h1>Order confirmed!</h1>
	<p>Thank you for your order. Your order ID is <strong>{data.order.id}</strong>.</p>

	<Card width="100%">
		<h2>Order summary</h2>
		{#each data.order.purchaseUnits as unit}
			{#each unit.items ?? [] as item}
				<div class="item">
					<span>{item.name} × {item.quantity}</span>
					{#if item.unitAmount}
						<span>{formatAmount(item.unitAmount)} each</span>
					{/if}
				</div>
			{/each}
			{#if unit.amount}
				<div class="total">
					<strong>Total</strong>
					<strong>{formatAmount(unit.amount)}</strong>
				</div>
			{/if}
		{/each}
	</Card>

	{#if data.order.purchaseUnits.some((unit) => unit.shipping?.address)}
		<Card width="100%">
			<h2>Shipping address</h2>
			{#each data.order.purchaseUnits as unit}
				{#if unit.shipping?.address}
					<p>{formatAddress(unit.shipping.address)}</p>
				{/if}
			{/each}
		</Card>
	{/if}

	<a href="/products">Continue shopping</a>
</div>

<style>
	.confirmation {
		display: flex;
		flex-direction: column;
		gap: 1.5rem;
		width: 100%;
		max-width: 750px;
	}

	h1, h2, p {
		margin: 0;
	}

	.item, .total {
		display: flex;
		justify-content: space-between;
		gap: 1rem;
		padding: 0.75rem 0;
	}

	.total {
		border-top: 1px solid #e7e7e7;
	}
</style>
