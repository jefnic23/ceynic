<!-- @migration-task Error while migrating Svelte code: `<th>` is invalid inside `<thead>` -->
<script lang="ts">
	import Button from "$lib/components/shared/Button.svelte";
	import { ButtonStyle } from "$lib/enums/buttonStyle";
	import Icon from "@iconify/svelte";
	import type { PageServerData } from "./$types";

	interface Props {
		data: PageServerData;
	}

	let { data }: Props = $props();
</script>

<div class="wrapper">
	{#await data.orders}
		<div>loading products...</div>
	{:then orders}
		<table>
			<thead>
				<tr>
					<th>Order ID</th>
					<th>Create Time</th>
					<th>Status</th>
					<th></th>
				</tr>
			</thead>
			<tbody>
				{#each orders as order}
					<tr>
						<td>{order.orderId}</td>
						<td>{new Date(order.createTime).toLocaleString()}</td>
						<td>{order.status}</td>
						<td>
							<a href="/admin/orders/{order.id}" data-sveltekit-preload-data>
								<Button style={ButtonStyle.Info}>
									<div>Details</div>
									<Icon icon="material-symbols:edit-rounded" width={16} height={16} />
								</Button>
							</a>
						</td>
					</tr>
				{/each}
			</tbody>
		</table>
	{/await}
</div>
