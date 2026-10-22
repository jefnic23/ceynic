<script lang="ts">
	import { enhance } from '$app/forms';
	import Button from '$lib/components/shared/Button.svelte';
	import Card from '$lib/components/shared/Card.svelte';
	import { ButtonStyle } from '$lib/enums/buttonStyle';
	import type { OrderDetails } from '$lib/interfaces/OrderDetails';
	import type { PageServerData } from './$types';
	import PageContainer from '$lib/components/shared/PageContainer.svelte';
	import OrderLine from '$lib/components/shared/OrderLine.svelte';
	import OrderSummary from '$lib/components/shared/OrderSummary.svelte';
	import { formatAddress } from '$lib/utils/formatters';

	interface Props {
		data: PageServerData;
	}

	let { data }: Props = $props();

	function formatCurrency(amount: number, currency = 'USD'): string {
		return new Intl.NumberFormat('en-US', {
			style: 'currency',
			currency
		}).format(amount);
	}

	function getTotalAmount(order: OrderDetails): string {
		return order.total ? formatCurrency(Number(order.total.value), order.total.currencyCode) : '';
	}

</script>

<PageContainer>
	<div class="order-page">
	{#await data.order}
		<div>Loading order...</div>
	{:then order}
		<header>
			<h1>Order #{order.id}</h1>
			<p>Status: {order.status}</p>
		</header>
		<OrderSummary>
			{#each order.items as item}
				<OrderLine>
					<span>{item.name} × {item.quantity}</span>
					{#if item.unitAmount}
						<span>{formatCurrency(Number(item.unitAmount.value), item.unitAmount.currencyCode)}</span>
					{/if}
				</OrderLine>
			{/each}
			<OrderLine total>
				<strong>Order total</strong>
				<strong>{getTotalAmount(order)}</strong>
			</OrderLine>
		</OrderSummary>
		<Card width="100%">
			<div class="details">
				<h2>Customer details</h2>
				<div>
					<p>{order.customer.name}</p>
					<p>{order.customer.email}</p>
					{#if order.shippingAddress}
						<p>{formatAddress(order.shippingAddress)}</p>
					{/if}
				</div>
			</div>
		</Card>
		<Card width="100%">
			<div class="details">
				<h2>Order history</h2>
				<p>Order placed: {new Date(order.createTime).toLocaleString()}</p>
			</div>
		</Card>
		<form method="POST" use:enhance>
			<input type="hidden" name="recordId" value={order.recordId} />
			{#if order.status === 'PENDING'}
				<Button name={"action"} value={"capture"}>Complete Order</Button>
				<Button name={"action"} value={"void"} style={ButtonStyle.Cancel}>Void</Button>
			{:else if order.status === 'COMPLETED'}
				<Button name={"action"} value={"refund"} style={ButtonStyle.Info}>Refund</Button>
			{/if}
		</form>
	{/await}
	</div>
</PageContainer>

<style>
	.order-page {
		display: flex;
		flex-direction: column;
		gap: 1.5rem;
	}

	h1, h2, p {
		margin-block: 0;
	}

	header, form {
		display: flex;
		flex-direction: column;
		gap: 0.75rem;
	}

	form {
		flex-direction: row;
		flex-wrap: wrap;
	}

	.details {
		display: flex;
		flex-direction: column;
		gap: 0.75rem;
	}
</style>
