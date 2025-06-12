<script lang="ts">
	import { enhance } from '$app/forms';
	import { page } from '$app/state';
	import Button from '$lib/components/shared/Button.svelte';
	import Card from '$lib/components/shared/Card.svelte';
	import { ButtonStyle } from '$lib/enums/buttonStyle';
	import type { Address, Item, OrderDetails } from '$lib/interfaces/OrderDetails';
	import type { PageServerData } from './$types';

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
		return formatCurrency(
			order.purchaseUnits?.reduce((sum, purchaseUnit) => {
				return sum + (parseFloat(purchaseUnit?.amount?.value as string));
			}, 0.0)
		);
	}
</script>

{#snippet address(order: OrderDetails)}
	{@const address: Address | undefined = order.purchaseUnits?.[0]?.shipping?.address}
	<div>
		{address?.addressLine1}
		{address?.addressLine2}, 
		{address?.adminArea2}, 
		{address?.adminArea1}, 
		{address?.postalCode}
	</div>
	<div>{address?.countryCode}</div>
{/snippet}

<div class="wrapper">
	{#await data.order}
		<div>loading products...</div>
	{:then order}
        <div>
            <h2>Order #{order.id}</h2>
            <div>Status: {order.purchaseUnits?.[0]?.payments?.authorizations?.[0]?.status === "CREATED" ? "Pending" : "Captured"}</div>
        </div>
		<Card>
			<table>
				<thead>
					<tr>
						<th>Product Description</th>
						<th>Amount</th>
					</tr>
				</thead>
				<tbody>
					{#each order.purchaseUnits as purchaseUnit}
						{#each (purchaseUnit?.items as Item[]) as item}
							<tr>
								<td>{item.description}</td>
								<td>${item.unitAmount?.value}</td>
							</tr>
						{/each}
					{/each}
				</tbody>
			</table>
			<div>Order total: {getTotalAmount(order)}</div>
		</Card>
		<Card>
			<div>
				<h2>Customer Details</h2>
				<div>{order.payer.name.givenName} {order.payer.name.surname}</div>
				<div>{order.payer.emailAddress}</div>
				{@render address(order)}
			</div>
		</Card>
		<Card>
			<div>
				<h2>Order History</h2>
				<div>Order placed: {new Date(order.createTime).toLocaleString()}</div>
			</div>
		</Card>
        <form method="POST" use:enhance>
			{#if order.purchaseUnits?.[0]?.payments?.authorizations?.[0]?.status === "CREATED"}
				<Button name={"action"} value={"capture"}>Complete Order</Button>
				<Button name={"action"} value={"void"} style={ButtonStyle.Cancel}>Void</Button>
			{:else if order.purchaseUnits?.[0]?.payments?.authorizations?.[0]?.status === "CAPTURED"}
				<Button name={"action"} value={"refund"} style={ButtonStyle.Info}>Refund</Button>
			{/if}
        </form>
	{/await}
</div>
