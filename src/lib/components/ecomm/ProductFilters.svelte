<script lang="ts">
	import { page } from '$app/state';
	import { goto } from '$app/navigation';
	import type { ProductMetadata } from '$lib/interfaces/ProductMetadata';
	import { ProductFilter } from '$lib/enums/productFilter';
	import Sort from '$lib/components/Sort.svelte';
	import Skeleton from '$lib/components/shared/Skeleton.svelte';
	import Button from '$lib/components/shared/Button.svelte';
	import { ButtonStyle } from '$lib/enums/buttonStyle';
	import RangeFilter from './RangeFilter.svelte';

	let { metadata, open = $bindable(false) }: { metadata: Promise<ProductMetadata | null>; open?: boolean } = $props();
	let sort = $state('');
	const sortOptions = [
		{ value: 'newest', label: 'Newest' }, { value: 'oldest', label: 'Oldest' },
		{ value: 'price_asc', label: 'Lowest Price' }, { value: 'price_desc', label: 'Highest Price' },
		{ value: 'size_asc', label: 'Smallest' }, { value: 'size_desc', label: 'Largest' }
	];
	let mediums = $state<string[]>(page.url.searchParams.getAll(ProductFilter.Medium));
	let mediumsChanged = $state(false);
	let minPriceChanged = $state(false);
	let maxPriceChanged = $state(false);
	let minWidthChanged = $state(false);
	let maxWidthChanged = $state(false);
	let minHeightChanged = $state(false);
	let maxHeightChanged = $state(false);
	let soldChanged = $state(false);
	let includeSold = $state(page.url.searchParams.get(ProductFilter.Sold) === 'true');
	let filterApplied = $derived(mediumsChanged || minPriceChanged || maxPriceChanged || minWidthChanged || maxWidthChanged || minHeightChanged || maxHeightChanged || soldChanged);
	let minPrice = $state(Number(page.url.searchParams.get(ProductFilter.MinPrice)) || 0);
	let maxPrice = $state(Number(page.url.searchParams.get(ProductFilter.MaxPrice)) || 0);
	let minWidth = $state(Number(page.url.searchParams.get(ProductFilter.MinWidth)) || 0);
	let maxWidth = $state(Number(page.url.searchParams.get(ProductFilter.MaxWidth)) || 0);
	let minHeight = $state(Number(page.url.searchParams.get(ProductFilter.MinHeight)) || 0);
	let maxHeight = $state(Number(page.url.searchParams.get(ProductFilter.MaxHeight)) || 0);

	async function loadMetadata() {
		const result = await metadata;
		minPrice = Math.floor(result?.priceRange?.minimum as number || 0);
		maxPrice = Math.floor(result?.priceRange?.maximum as number || 0);
		minWidth = Math.floor(result?.sizeRanges?.widthMinimum || 0);
		maxWidth = Math.floor(result?.sizeRanges?.widthMaximum || 0);
		minHeight = Math.floor(result?.sizeRanges?.heightMinimum || 0);
		maxHeight = Math.floor(result?.sizeRanges?.heightMaximum || 0);
		return result;
	}
	let metadataPromise = loadMetadata();

	function toggleMedium(medium: string) {
		mediums = mediums.includes(medium) ? mediums.filter((value) => value !== medium) : [...mediums, medium];
		mediumsChanged = true;
	}

	async function handleSort() {
		if (open) return;
		const url = new URL(page.url);
		url.searchParams.set('sort', sort);
		await goto(url, { replaceState: true, keepFocus: true });
	}

	async function handleFilter() {
		open = false;
		const url = new URL(page.url);
		if (mediumsChanged) {
			url.searchParams.delete(ProductFilter.Medium);
			mediums.forEach((medium) => url.searchParams.append(ProductFilter.Medium, medium));
		}
		const ranges = [
			[ProductFilter.MinPrice, minPriceChanged, minPrice], [ProductFilter.MaxPrice, maxPriceChanged, maxPrice],
			[ProductFilter.MinWidth, minWidthChanged, minWidth], [ProductFilter.MaxWidth, maxWidthChanged, maxWidth],
			[ProductFilter.MinHeight, minHeightChanged, minHeight], [ProductFilter.MaxHeight, maxHeightChanged, maxHeight]
		] as const;
		for (const [key, changed, value] of ranges) if (changed) url.searchParams.set(key, String(value));
		if (soldChanged) {
			if (includeSold) url.searchParams.set(ProductFilter.Sold, 'true');
			else url.searchParams.delete(ProductFilter.Sold);
		}
		if (sort) url.searchParams.set('sort', sort);
		if (url.searchParams.size === 0 && page.url.searchParams.size === 0) return;
		await goto(url, { replaceState: true, keepFocus: true });
	}

	async function handleClear() {
		open = false;
		sort = '';
		if (page.url.searchParams.size === 0 && !filterApplied) return;
		mediums = [];
		await loadMetadata();
		mediumsChanged = false;
		minPriceChanged = false; maxPriceChanged = false;
		minWidthChanged = false; maxWidthChanged = false;
		minHeightChanged = false; maxHeightChanged = false;
		includeSold = false;
		soldChanged = false;
		await goto('/products', { replaceState: true, keepFocus: true });
	}

</script>

<aside class:open class="filters" aria-label="Filter and sort products">
	<div class="heading"><h4>Filter &amp; Sort</h4><button class="close-button" type="button" aria-label="Close filters" onclick={() => open = false}>&times;</button></div>
	<Sort options={sortOptions} bind:selected={sort} change={handleSort} />
	{#await metadataPromise}
		<div class="loading"><Skeleton /><Skeleton /><Skeleton /></div>
	{:then details}
		{#if details}
			<div class="group">
				<h4>Medium</h4>
				{#each details.mediumCounts || [] as mediumCount}
					<label class="choice"><input type="checkbox" name={mediumCount.name} value={mediumCount.id} checked={mediums.includes(mediumCount.name)} onchange={() => toggleMedium(mediumCount.name)} />{mediumCount.name} ({mediumCount.count})</label>
				{/each}
			</div>
			<RangeFilter title="Price" bind:minimum={minPrice} bind:maximum={maxPrice} bind:minimumChanged={minPriceChanged} bind:maximumChanged={maxPriceChanged} lower={Math.floor(details.priceRange?.minimum as number || 0)} upper={Math.floor(details.priceRange?.maximum as number || 0)} unit="price" />
			<RangeFilter title="Width" bind:minimum={minWidth} bind:maximum={maxWidth} bind:minimumChanged={minWidthChanged} bind:maximumChanged={maxWidthChanged} lower={Math.floor(details.sizeRanges?.widthMinimum || 0)} upper={Math.floor(details.sizeRanges?.widthMaximum || 0)} unit="size" />
			<RangeFilter title="Height" bind:minimum={minHeight} bind:maximum={maxHeight} bind:minimumChanged={minHeightChanged} bind:maximumChanged={maxHeightChanged} lower={Math.floor(details.sizeRanges?.heightMinimum || 0)} upper={Math.floor(details.sizeRanges?.heightMaximum || 0)} unit="size" />
		{/if}
	{/await}
	<div class="group"><h4>Availability</h4><label class="choice"><input type="checkbox" checked={includeSold} onchange={(event) => { includeSold = event.currentTarget.checked; soldChanged = true; }} />Sold</label></div>
	<div class="filter-actions"><Button onclick={handleFilter}>Filter</Button><Button onclick={handleClear} style={ButtonStyle.Cancel}>Clear</Button></div>
</aside>

<style>
	.filters { position: sticky; inset-block-start: 182px; align-self: start; display: flex; flex-direction: column; gap: 1rem; inline-size: 100%; min-inline-size: 0; }
	.heading { display: flex; align-items: center; justify-content: space-between; }
	h4 { margin-block: 0 0.5rem; }
	.choice { display: flex; align-items: center; gap: 0.5rem; }
	.choice input { flex: none; }
	.group { display: flex; flex-direction: column; gap: 0.5rem; }
	.loading { display: flex; flex-direction: column; gap: 1rem; }
	.filter-actions { display: flex; gap: 0.5rem; margin-block-start: 0.33em; }
	.close-button { display: none; background: none; border: 0; color: var(--ink-muted); font-size: 2rem; cursor: pointer; }
	.close-button:active { color: var(--ink); }
	@media (hover: hover) and (pointer: fine) { .close-button:hover { color: var(--ink); } }
	@media (width <= 974px) {
		:global(html:has(.filters.open)) { overflow: hidden; }
		.filters { position: fixed; z-index: 100; inset: 0; block-size: 100dvh; padding: 1rem; background: var(--surface); box-shadow: 2px 0 10px color-mix(in oklch, var(--ink) 20%, transparent); overflow-y: auto; visibility: hidden; transform: translateX(-100%); }
		.filters.open { visibility: visible; transform: translateX(0); }
		.close-button { display: block; }
	}
	@media (width <= 974px) and (prefers-reduced-motion: no-preference) {
		.filters { transition: transform 250ms var(--ease-out), visibility 250ms; }
	}
</style>
