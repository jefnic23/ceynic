<script lang="ts">
	import PageContainer from '$lib/components/shared/PageContainer.svelte';
	import OrderLine from '$lib/components/shared/OrderLine.svelte';
	import OrderSummary from '$lib/components/shared/OrderSummary.svelte';
	import type { Money } from '$lib/interfaces/OrderConfirmation';
	import type { PageData } from './$types';

	let { data }: { data: PageData } = $props();
	let isConfirmed = $derived(['PENDING', 'CAPTURE_PENDING', 'COMPLETED'].includes(data.order.status));

	function formatAmount(amount: Money | null | undefined): string {
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
	<h1>{isConfirmed ? 'Order confirmed!' : 'Order details'}</h1>
	<p>{isConfirmed ? 'Thank you for your order. ' : ''}Your order ID is <strong>{data.order.id}</strong>.</p>

	<OrderSummary>
		{#each data.order.items as item}
			<OrderLine>
				<span>{item.name} × {item.quantity}</span>
				{#if item.unitAmount}
					<span>{formatAmount(item.unitAmount)} each</span>
				{/if}
			</OrderLine>
		{/each}
		{#if data.order.total}
			<OrderLine total>
				<strong>Total</strong>
				<strong>{formatAmount(data.order.total)}</strong>
			</OrderLine>
		{/if}
	</OrderSummary>

	<a href="/products">Continue shopping</a>
	</div>
</PageContainer>

<style>
	.confirmation {
		display: flex;
		flex-direction: column;
		gap: 1.5rem;
	}

	h1, p {
		margin-block: 0;
	}
</style>
