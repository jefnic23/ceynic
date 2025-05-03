<script lang="ts">
	import { enhance } from '$app/forms';
	import AnimatedButton from '$lib/components/shared/AnimatedButton.svelte';
	import Button from '$lib/components/shared/Button.svelte';
	import Card from '$lib/components/shared/Card.svelte';
	import { ButtonStyle } from '$lib/enums/buttonStyle';
	import Edit from '$lib/icons/Edit.svelte';
	import type { OrderOut } from '$lib/interfaces/order';
	import type { PageServerData } from './$types';

	export let data: PageServerData;

	function formatCurrency(amount: number, currency = 'USD'): string {
		return new Intl.NumberFormat('en-US', {
			style: 'currency',
			currency
		}).format(amount);
	}

	function getTotalAmount(order: OrderOut): string {
		return formatCurrency(
			order.purchaseUnits.reduce((sum, purchaseUnit) => {
				return sum + purchaseUnit.amount.value;
			}, 0)
		);
	}
</script>

<div class="wrapper">
	{#await data.order}
		<div>loading products...</div>
	{:then order}
        <div>
            <h2>Order #{order.id}</h2>
            <div>Status: {order.status}</div>
        </div>
		<Card>
			<table>
				<thead>
					<th>Product Description</th>
					<th>Amount</th>
				</thead>
				<tbody>
					{#each order.purchaseUnits as purchaseUnit}
						<tr>
							<td>{purchaseUnit.description}</td>
							<td>${purchaseUnit.amount.value}</td>
						</tr>
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
				<div>
					{order.purchaseUnits[0].shipping.address.addressLine1}
					{order.purchaseUnits[0].shipping.address.addressLine2}, 
                    {order.purchaseUnits[0].shipping.address.adminArea2}, 
                    {order.purchaseUnits[0].shipping.address.adminArea1}, 
                    {order.purchaseUnits[0].shipping.address.postalCode}
				</div>
				<div>{order.purchaseUnits[0].shipping.address.countryCode}</div>
			</div>
		</Card>
		<Card>
			<div>
				<h2>Order History</h2>
				<div>Order placed: {new Date(order.createTime).toLocaleString()}</div>
			</div>
		</Card>
        <form action="/admin/orders/{order.id}" method="POST" use:enhance>
			{#if order.purchaseUnits[0].payments.authorizations[0].status === "CREATED"}
				<Button name={"action"} value={"capture"}>Complete Order</Button>
				<Button name={"action"} value={"void"} style={ButtonStyle.Cancel}>Void</Button>
			{:else if order.purchaseUnits[0].payments.authorizations[0].status === "CAPTURED"}
				<Button name={"action"} value={"refund"} style={ButtonStyle.Info}>Refund</Button>
			{/if}
        </form>
	{/await}
</div>
