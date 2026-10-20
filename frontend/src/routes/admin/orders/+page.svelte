<script lang="ts">
	import ButtonLink from '$lib/components/shared/ButtonLink.svelte';
	import Table from "$lib/components/shared/Table.svelte";
	import Icon from "@iconify/svelte";
	import type { OrderOut } from "$lib/interfaces/OrderOut";
	import type { PageServerData } from "./$types";
	import Card from "$lib/components/shared/Card.svelte";
	import PageContainer from '$lib/components/shared/PageContainer.svelte';
	import StatusBadge from '$lib/components/shared/StatusBadge.svelte';

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

<PageContainer max="100%">
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
						<td><StatusBadge>{order.status}</StatusBadge></td>
						<td>
							<ButtonLink href="/admin/orders/{order.orderId}">
								Details <Icon icon="material-symbols:edit-rounded" width={16} height={16} />
							</ButtonLink>
						</td>
					</tr>
				{/snippet}
			</Table>
		{/await}
	</Card>
</PageContainer>

<!-- add modal for order editing and remove slug -->
