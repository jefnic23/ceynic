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
	<div class="dashboard-grid">
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
		<Card width="100%">
			<h2>Orders per month</h2>
			{#await data.monthlyOrders}
				<p>Loading order counts...</p>
			{:then months}
				{@const chartMax = Math.max(2, Math.ceil(Math.max(...months.map((month) => month.count)) / 2) * 2)}
				<div class="chart-scroll">
					<div class="chart">
						<div class="y-axis" aria-hidden="true">
							<span>{chartMax}</span>
							<span>{chartMax / 2}</span>
							<span>0</span>
						</div>
						<div class="plot">
							<div class="gridline top" aria-hidden="true"></div>
							<div class="gridline middle" aria-hidden="true"></div>
							<div class="gridline bottom" aria-hidden="true"></div>
							<ul class="monthly-orders" aria-label="Orders per month for the last six months">
								{#each months as month (month.label)}
									<li style:--bar-height="{(month.count / chartMax) * 100}%">
										<span class="bar-value">{month.count}</span>
										<div class="bar" aria-hidden="true"></div>
										<span class="month-label">{month.label}</span>
									</li>
								{/each}
							</ul>
						</div>
					</div>
				</div>
			{/await}
		</Card>
	</div>
</div>

<style>
	.wrapper {
		display: flex;
		flex-direction: column;
		gap: 1.5rem;
		width: 100%;
		max-width: 1200px;
		min-width: 0;
	}

	.dashboard-grid {
		display: grid;
		grid-template-columns: repeat(2, minmax(0, 1fr));
		gap: 1.5rem;
		width: 100%;
	}

	@media (max-width: 900px) {
		.dashboard-grid {
			grid-template-columns: minmax(0, 1fr);
		}
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

	.chart-scroll {
		overflow-x: auto;
		padding-top: 1.5rem;
	}

	.chart {
		display: grid;
		grid-template-columns: auto minmax(0, 1fr);
		gap: 0.5rem;
		min-width: 22rem;
		padding-bottom: 2.5rem;
	}

	.y-axis {
		display: flex;
		flex-direction: column;
		justify-content: space-between;
		align-items: flex-end;
		height: 10rem;
		color: #6b7280;
		font-size: 0.75rem;
		line-height: 1;
	}

	.plot {
		position: relative;
		height: 10rem;
	}

	.gridline {
		position: absolute;
		left: 0;
		right: 0;
		border-top: 1px solid #e5e7eb;
	}

	.gridline.top {
		top: 0;
	}

	.gridline.middle {
		top: 50%;
	}

	.gridline.bottom {
		bottom: 0;
	}

	.monthly-orders {
		position: relative;
		display: grid;
		grid-template-columns: repeat(6, minmax(0, 1fr));
		gap: 0.375rem;
		height: 100%;
	}

	.monthly-orders li {
		position: relative;
		display: flex;
		align-items: flex-end;
		justify-content: center;
		padding: 0;
		border: 0;
	}

	.bar {
		width: 70%;
		max-width: 3rem;
		height: var(--bar-height);
		border-radius: 0.25rem 0.25rem 0 0;
		background: #2196f3;
	}

	.bar-value {
		position: absolute;
		bottom: calc(var(--bar-height) + 0.25rem);
		font-size: 0.75rem;
		font-weight: 600;
	}

	.month-label {
		position: absolute;
		top: calc(100% + 0.5rem);
		font-size: 0.75rem;
		text-align: center;
		color: #6b7280;
	}
</style>
