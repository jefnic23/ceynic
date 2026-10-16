<script lang="ts">
	import Button from '$lib/components/shared/Button.svelte';
	import Card from '$lib/components/shared/Card.svelte';
	import { ButtonStyle } from '$lib/enums/buttonStyle';
	import type { PageServerData } from './$types';

	interface Props {
		data: PageServerData;
	}

	let { data }: Props = $props();

	function welcomeMessage(user: { firstName: string | null } | null): string {
		const name = user?.firstName?.trim();
		return name ? `Welcome, ${name}.` : 'Welcome.';
	}
</script>

<div class="wrapper">
	<Card width="100%">
		{#await data.user}
			<h1>Welcome.</h1>
		{:then user}
			<h1>{welcomeMessage(user)}</h1>
		{/await}
	</Card>
	<Card width="100%">
		<h2>Pending orders</h2>
		{#await data.pendingOrders}
			<p>Loading pending orders...</p>
		{:then orders}
			{#if orders.length === 0}
				<p>No pending orders.</p>
			{:else}
				<ul>
					{#each orders as order (order.orderId)}
						<li>
							<div class="order-info">
								<strong>Order #{order.orderId}</strong>
								<span>{new Date(order.createTime).toLocaleString()}</span>
							</div>
							<a href="/admin/orders/{order.orderId}" data-sveltekit-preload-data>
								<Button style={ButtonStyle.Info}>Details</Button>
							</a>
						</li>
					{/each}
				</ul>
			{/if}
		{/await}
	</Card>
</div>

<style>
	.wrapper {
		display: flex;
		flex-direction: column;
		gap: 1.5rem;
		width: 100%;
		max-width: 850px;
		min-width: 0;
	}

	h1, h2 {
		margin: 0 0 1rem;
	}

	h1 {
		margin: 0;
	}

	p {
		margin: 0;
	}

	ul {
		list-style: none;
		margin: 0;
		padding: 0;
	}

	li {
		display: flex;
		align-items: center;
		justify-content: space-between;
		flex-wrap: wrap;
		gap: 1rem;
		padding: 1rem 0;
		border-top: 1px solid #e5e7eb;
	}

	.order-info {
		display: flex;
		flex-direction: column;
		gap: 0.25rem;
		min-width: 0;
		overflow-wrap: anywhere;
	}

	.order-info span {
		color: #6b7280;
	}
</style>
