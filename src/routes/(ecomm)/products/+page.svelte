<script lang="ts">
	import type { PageData } from './$types';
	import Button from '$lib/components/shared/Button.svelte';
	import { ButtonStyle } from '$lib/enums/buttonStyle';
	import Skeleton from '$lib/components/shared/Skeleton.svelte';
	import BrowseLayout from '$lib/components/ecomm/BrowseLayout.svelte';
	import ProductFilters from '$lib/components/ecomm/ProductFilters.svelte';
	import ProductGrid from '$lib/components/ecomm/ProductGrid.svelte';
	import Icon from '@iconify/svelte';

	let { data }: { data: PageData } = $props();
	let showFilters = $state(false);
</script>

<svelte:head><title>Browse</title></svelte:head>

<BrowseLayout enabled={data.sortAndFilterEnabled}>
	{#snippet filters()}
		<ProductFilters metadata={data.metadata} bind:open={showFilters} />
	{/snippet}
	{#await data.products}
		<Skeleton />
	{:then products}
		{#if data.sortAndFilterEnabled}
			<div class="filter-trigger">
				<Button onclick={() => showFilters = true} style={ButtonStyle.Neutral} aria-expanded={showFilters}>
					Filter &amp; Sort <Icon icon="material-symbols:filter-list-rounded" width={32} height={32} />
				</Button>
			</div>
		{/if}
		<ProductGrid {products} />
	{:catch error}
		<div>Something went wrong: {error.message}</div>
	{/await}
</BrowseLayout>

<style>
	.filter-trigger { display: none; }
	@media (width <= 974px) { .filter-trigger { display: flex; } }
</style>
