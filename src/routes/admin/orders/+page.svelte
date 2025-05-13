<!-- @migration-task Error while migrating Svelte code: `<th>` is invalid inside `<thead>` -->
<script lang="ts">
	import AnimatedButton from "$lib/components/shared/AnimatedButton.svelte";
	import { ButtonStyle } from "$lib/enums/buttonStyle";
	import Edit from "$lib/icons/Edit.svelte";
	import type { PageServerData } from "./$types";

	export let data: PageServerData;
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
						<td>{order.id}</td>
						<td>{new Date(order.createTime).toLocaleString()}</td>
						<td>{order.status}</td>
						<td>
							<a href="/admin/orders/{order.id}" data-sveltekit-preload-data>
								<AnimatedButton text={"Details"} style={ButtonStyle.Info}>
									<Edit size={16} />
								</AnimatedButton>
							</a>
						</td>
					</tr>
				{/each}
			</tbody>
		</table>
	{/await}
</div>
