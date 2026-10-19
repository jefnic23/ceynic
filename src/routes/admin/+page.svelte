<script lang="ts">
	import Card from '$lib/components/shared/Card.svelte';
	import type { PageServerData } from './$types';
	import PageContainer from '$lib/components/shared/PageContainer.svelte';
	import MonthlyOrdersChart from '$lib/components/admin/MonthlyOrdersChart.svelte';
	import PendingOrders from '$lib/components/admin/PendingOrders.svelte';

	interface Props {
		data: PageServerData;
	}

	let { data }: Props = $props();

	function welcomeMessage(user: { firstName: string | null } | null): string {
		const name = user?.firstName?.trim();
		return name ? `Welcome, ${name}.` : 'Welcome.';
	}
</script>

<PageContainer max="1200px">
	<div class="dashboard">
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
				<PendingOrders {orders} />
			{/await}
		</Card>
		<Card width="100%">
			<h2>Orders per month</h2>
			{#await data.monthlyOrders}
				<p>Loading order counts...</p>
			{:then months}
				<MonthlyOrdersChart {months} />
			{/await}
		</Card>
	</div>
	</div>
</PageContainer>

<style>
	.dashboard {
		display: flex;
		flex-direction: column;
		gap: 1.5rem;
	}

	.dashboard-grid {
		display: grid;
		grid-template-columns: repeat(auto-fit, minmax(min(100%, 26rem), 1fr));
		gap: 1.5rem;
		width: 100%;
	}

	h1, h2 {
		margin-block: 0 1rem;
	}

	h1 {
		margin-block: 0;
	}

	p {
		margin-block: 0;
	}

</style>
