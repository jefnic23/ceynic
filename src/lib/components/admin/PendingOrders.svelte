<script lang="ts">
	import type { OrderOut } from '$lib/interfaces/OrderOut';
	import ButtonLink from '$lib/components/shared/ButtonLink.svelte';
	let { orders }: { orders: OrderOut[] } = $props();
</script>

{#if orders.length === 0}
	<p>No pending orders.</p>
{:else}
	<ul>
		{#each orders as order (order.orderId)}
			<li>
				<div class="order-info"><strong>Order #{order.orderId}</strong><span>{new Date(order.createTime).toLocaleString()}</span></div>
				<ButtonLink href="/admin/orders/{order.orderId}">Details</ButtonLink>
			</li>
		{/each}
	</ul>
{/if}

<style>
	p { margin-block: 0; }
	ul { list-style: none; margin: 0; padding: 0; }
	li { display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 1rem; padding-block: 1rem; border-block-start: 1px solid var(--border); }
	.order-info { display: flex; flex-direction: column; gap: 0.25rem; min-inline-size: 0; overflow-wrap: anywhere; }
	.order-info span { color: var(--ink-muted); }
</style>
