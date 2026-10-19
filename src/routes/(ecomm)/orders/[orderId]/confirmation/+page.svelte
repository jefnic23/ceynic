<script lang="ts">
	import Card from '$lib/components/shared/Card.svelte';
	import PageContainer from '$lib/components/shared/PageContainer.svelte';
	import OrderLine from '$lib/components/shared/OrderLine.svelte';
	import OrderSummary from '$lib/components/shared/OrderSummary.svelte';
	import { formatAddress } from '$lib/utils/formatters';
	import type { UnitAmount } from '$lib/interfaces/OrderDetails';
	import type { PageData } from './$types';

	let { data }: { data: PageData } = $props();

	function formatAmount(amount: UnitAmount | undefined): string {
		if (!amount) return '';
		return new Intl.NumberFormat('en-US', {
			style: 'currency',
			currency: amount.currencyCode ?? 'USD'
		}).format(Number(amount.value));
	}

</script>

<svelte:head>
	<title>Order confirmation</title>
</svelte:head>

<PageContainer>
	<div class="confirmation">
	<h1>Order confirmed!</h1>
	<p>Thank you for your order. Your order ID is <strong>{data.order.id}</strong>.</p>

	<OrderSummary>
		{#each data.order.purchaseUnits as unit}
			{#each unit.items ?? [] as item}
				<OrderLine>
					<span>{item.name} × {item.quantity}</span>
					{#if item.unitAmount}
						<span>{formatAmount(item.unitAmount)} each</span>
					{/if}
				</OrderLine>
			{/each}
			{#if unit.amount}
				<OrderLine total>
					<strong>Total</strong>
					<strong>{formatAmount(unit.amount)}</strong>
				</OrderLine>
			{/if}
		{/each}
	</OrderSummary>

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
</PageContainer>

<style>
	.confirmation {
		display: flex;
		flex-direction: column;
		gap: 1.5rem;
	}

	h1, h2, p {
		margin-block: 0;
	}
</style>
