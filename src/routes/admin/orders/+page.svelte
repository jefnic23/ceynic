<script lang="ts">
	import Button from "$lib/components/shared/Button.svelte";
	import Table from "$lib/components/shared/Table.svelte";
	import { ButtonStyle } from "$lib/enums/buttonStyle";
	import Icon from "@iconify/svelte";
	import type { OrderOut } from "$lib/interfaces/OrderOut";
	import type { PageServerData } from "./$types";
	import Card from "$lib/components/shared/Card.svelte";

	interface Props {
		data: PageServerData;
	}

	let { data }: Props = $props();
	const orderColumns = [
		{ label: 'Order ID', sortValue: (order: OrderOut) => order.orderId },
		{ label: 'Create Time', sortValue: (order: OrderOut) => new Date(order.createTime).getTime() },
		{ label: 'Status', sortValue: (order: OrderOut) => order.status },
		{ label: 'Actions' }
	];
</script>

<div class="wrapper">
	<Card width="100%">
		<h1>Orders</h1>
		{#await data.orders}
			<div>Loading orders...</div>
		{:then orders}
			<Table label="Orders" rows={orders} columns={orderColumns} emptyMessage="No orders found.">
				{#snippet row(order)}
					<tr>
						<td>{order.orderId}</td>
						<td>{new Date(order.createTime).toLocaleString()}</td>
						<td><span class="status">{order.status}</span></td>
						<td>
							<a href="/admin/orders/{order.orderId}" data-sveltekit-preload-data>
								<Button style={ButtonStyle.Info}>
									<div>Details</div>
									<Icon icon="material-symbols:edit-rounded" width={16} height={16} />
								</Button>
							</a>
						</td>
					</tr>
				{/snippet}
			</Table>
		{/await}
	</Card>
</div>

<!-- add modal for order editing and remove slug -->

<style>
	.wrapper {
		width: 100%;
		min-width: 0;
	}

	.status {
		display: inline-flex;
		padding: 0.25rem 0.5rem;
		border-radius: 9999px;
		background: #f3f4f6;
		color: #374151;
		font-size: 0.75rem;
		font-weight: 600;
	}
</style>
