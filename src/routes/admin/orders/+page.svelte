<!-- @migration-task Error while migrating Svelte code: `<th>` is invalid inside `<thead>` -->
<script lang="ts">
	import Button from "$lib/components/shared/Button.svelte";
	import Table from "$lib/components/shared/Table.svelte";
	import { ButtonStyle } from "$lib/enums/buttonStyle";
	import Icon from "@iconify/svelte";
	import type { PageServerData } from "./$types";
	import Card from "$lib/components/shared/Card.svelte";

	interface Props {
		data: PageServerData;
	}

	let { data }: Props = $props();
</script>

<div class="wrapper">
	<Card width="100%">
		<h1>Orders</h1>
		{#await data.orders}
			<div>loading products...</div>
		{:then orders}
			<Table label="Orders">
				<thead>
					<tr>
						<th>Order ID</th>
						<th>Create Time</th>
						<th>Status</th>
						<th>Actions</th>
					</tr>
				</thead>
				<tbody>
					{#each orders as order}
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
					{:else}
						<tr><td colspan="4">No orders found.</td></tr>
					{/each}
				</tbody>
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
