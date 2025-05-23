<script lang="ts">
	import { slide } from 'svelte/transition';
	import type { PageData } from './$types';
	import { page } from '$app/state';
	import { goto } from '$app/navigation';
	import Dropdown from '$lib/components/Dropdown.svelte';
	import Skeleton from '$lib/components/shared/Skeleton.svelte';
	import Button from '$lib/components/shared/Button.svelte';
	import { ButtonStyle } from '$lib/enums/buttonStyle';
	import { ProductFilter } from '$lib/enums/productFilter';
	import type { SizeRanges } from '$lib/interfaces/sizeRanges';
	import type { PriceRange } from '$lib/interfaces/priceRange';
	import ProductCard from '$lib/components/ProductCard.svelte';
	import { onDestroy, onMount } from 'svelte';
	import Filter from '$lib/icons/Filter.svelte';
	import type { MediumCount } from '$lib/interfaces/mediumCount';
	import ScrollableInput from '$lib/components/shared/ScrollableInput.svelte';
	import type { ProductMetadata } from '$lib/interfaces/product_metadata';

	interface Props {
		data: PageData;
	}

	let { data }: Props = $props();

	let isMobile = $state(false);
	let showFilters = $state(false);

	$effect(() => {
		if (showFilters) {
			document?.body?.classList?.add('no-scroll');
		} else {
			document?.body?.classList?.remove('no-scroll');
		}
	});

	onMount(() => {
		const checkMobile = () => {
			isMobile = window.matchMedia("(max-width: 974px)").matches;
		};

		checkMobile();
		window.addEventListener("resize", checkMobile);
		return () => window.removeEventListener("resize", checkMobile);
	});

	onDestroy(() => {
		document?.body?.classList?.remove('no-scroll');
	});

	function toggleSidebar() {
		showFilters = !showFilters;
	}

	let sort: string = $state('');
	const sortOptions = [
		{ value: 'newest', label: 'Newest' },
		{ value: 'oldest', label: 'Oldest' },
		{ value: 'price_asc', label: 'Lowest Price' },
		{ value: 'price_desc', label: 'Highest Price' },
		{ value: 'size_asc', label: 'Smallest' },
		{ value: 'size_desc', label: 'Largest' }
	];
	
	let mediumsChanged: boolean = $state(false);
	let minPriceChanged: boolean = $state(false);
	let maxPriceChanged: boolean = $state(false);
	let minWidthChanged: boolean = $state(false);
	let maxWidthChanged: boolean = $state(false);
	let minHeightChanged: boolean = $state(false);
	let maxHeightChanged: boolean = $state(false);
	let filterApplied = $derived(mediumsChanged || minPriceChanged || maxPriceChanged || minWidthChanged || maxWidthChanged || minHeightChanged || maxHeightChanged);

	let mediums: string[] = $state(page.url.searchParams.getAll('medium') || []);

	function handleMedium(medium: string) {
		if (mediums.includes(medium)) {
			mediums = mediums.filter(m => m !== medium);
		} else {
			mediums = [...mediums, medium];
		}
		mediumsChanged = true;
	}

	let minPrice: number = $state(parseInt(page.url.searchParams.get(ProductFilter.MinPrice) as string) || 0);
	let maxPrice: number = $state(parseInt(page.url.searchParams.get(ProductFilter.MaxPrice) as string) || 0);
	let minWidth: number = $state(parseInt(page.url.searchParams.get(ProductFilter.MinWidth) as string) || 0);
	let maxWidth: number = $state(parseInt(page.url.searchParams.get(ProductFilter.MaxWidth) as string) || 0);
	let minHeight: number = $state(parseInt(page.url.searchParams.get(ProductFilter.MinHeight) as string) || 0);
	let maxHeight: number = $state(parseInt(page.url.searchParams.get(ProductFilter.MaxHeight) as string) || 0);

	async function loadMetadata(): Promise<ProductMetadata> {
		const metadata = await data.metadata;

		minPrice = Math.floor(metadata?.priceRange?.minimum || 0);
		maxPrice = Math.floor(metadata?.priceRange?.maximum || 0);
		minWidth = Math.floor(metadata?.sizeRanges?.widthMinimum || 0);
		maxWidth = Math.floor(metadata?.sizeRanges?.widthMaximum || 0);
		minHeight = Math.floor(metadata?.sizeRanges?.heightMinimum || 0);
		maxHeight = Math.floor(metadata?.sizeRanges?.heightMaximum || 0);

		return metadata as ProductMetadata;
	}

	let loadMetadataPromise = loadMetadata();

	async function handleSort(event: CustomEvent) {
		const url = new URL(window.location.href);
		url.searchParams.set('sort', event.detail);
		if(!isMobile) await goto(url, { replaceState: true, keepFocus: true });
	}

	async function handleFilter() {
		if (isMobile) toggleSidebar();

		const url = new URL(window.location.href);

		if (mediumsChanged) {
			url.searchParams.delete('medium');
			mediums.forEach(m => url.searchParams.append(ProductFilter.Medium, m));
		}

		if (minPriceChanged) url.searchParams.set(ProductFilter.MinPrice, minPrice.toString());
		if (maxPriceChanged) url.searchParams.set(ProductFilter.MaxPrice, maxPrice.toString());
		if (minWidthChanged) url.searchParams.set(ProductFilter.MinWidth, minWidth.toString());
		if (maxWidthChanged) url.searchParams.set(ProductFilter.MaxWidth, maxWidth.toString());
		if (minHeightChanged) url.searchParams.set(ProductFilter.MinHeight, minHeight.toString());
		if (maxHeightChanged) url.searchParams.set(ProductFilter.MaxHeight, maxHeight.toString());
		if (sort !== "") url.searchParams.set('sort', sort)

		if (url.searchParams.size === 0)  return;

		await goto(url, { replaceState: true, keepFocus: true });
	}

	async function handleClear() {
		if (isMobile) {
			toggleSidebar();
			sort = "";
		};
		if (page.url.searchParams.size === 0 && !filterApplied) return;
		mediums = [];
		await loadMetadata();
		mediumsChanged = false;
		minPriceChanged = false;
		maxPriceChanged = false;
		minWidthChanged = false;
		maxWidthChanged = false;
		minHeightChanged = false;
		maxHeightChanged = false;
		await goto('products', { replaceState: true, keepFocus: true });
	}
</script>

{#if isMobile && showFilters}
    <div class="backdrop" onclick={toggleSidebar}></div>
{/if}

<div class="container">
	<aside 
		class="column filters" 
		class:is-mobile={isMobile} 
		class:open={showFilters}
		transition:slide="{{ duration: 377 }}"
	>
		<div class="row">
			{#if isMobile && showFilters}
				<div class="column">
					Filter
				</div>
				<div class="column">
					<button class="close-button" onclick={toggleSidebar}>&times;</button>
				</div>
			{:else}
				<div class="column">
					Filter
				</div>
			{/if}
		</div>
		{#if isMobile}
			<div class="row" style:margin-top="1.33em">
				<div class="column">
					<Dropdown options={sortOptions} bind:selected={sort} change={handleSort} />
				</div>
			</div>
		{/if}
		{#await loadMetadataPromise}
			<div class="row">
				<div class="column">
					<Skeleton />
					<Skeleton />
					<Skeleton />
				</div>
			</div>
		{:then metadata} 
			<div class="row">
				<div class="column">
					<h4>Medium</h4>
					<div class="column">
						{#each metadata?.mediumCounts || [] as mediumCount}
							<div class="row justify-left">
								<input
									type="checkbox"
									id={mediumCount.name}
									name={mediumCount.name}
									value={mediumCount.id}
									checked={mediums.includes(mediumCount.name)}
									onclick={() => handleMedium(mediumCount.name)}
								/>
								<label for={mediumCount.name}>{mediumCount.name} ({mediumCount.count})</label>
							</div>
						{/each}
					</div>
				</div>
			</div>
			<div class="row">
				<div class="column">
					<div class="row">
						<h4>Price</h4>
					</div>
					<div class="row">
						<ScrollableInput
							bind:value={minPrice}
							bind:relatedValue={maxPrice}
							bind:isChanged={minPriceChanged}
							isMinimum={true}
							id={"minPrice"}
							label={"Min"}
							min={Math.floor(metadata?.priceRange?.minimum || 0)}
							max={Math.floor(metadata?.priceRange?.maximum || 0)}
							className={"price"}
						/>
						<ScrollableInput
							bind:value={maxPrice}
							bind:relatedValue={minPrice}
							bind:isChanged={maxPriceChanged}
							isMinimum={false}
							id={"maxPrice"}
							label={"Max"}
							min={Math.floor(metadata?.priceRange?.minimum || 0)}
							max={Math.floor(metadata?.priceRange?.maximum || 0)}
							className={"price"}
						/>
					</div>
				</div>
			</div>
			<div class="row">
				<div class="column">
					<div class="row">
						<div class="column">
							<div class="row">
								<h4>Width</h4>
							</div>
							<div class="row">
								<ScrollableInput
									bind:value={minWidth}
									bind:relatedValue={maxWidth}
									bind:isChanged={minWidthChanged}
									isMinimum={true}
									id={"minWidth"}
									label={"Min"}
									min={Math.floor(metadata?.sizeRanges?.widthMinimum || 0)}
									max={Math.floor(metadata?.sizeRanges?.widthMaximum || 0)}
									className={"size"}
								/>
								<ScrollableInput
									bind:value={maxWidth}
									bind:relatedValue={minWidth}
									bind:isChanged={maxWidthChanged}
									isMinimum={false}
									id={"maxWidth"}
									label={"Max"}
									min={Math.floor(metadata?.sizeRanges?.widthMinimum || 0)}
									max={Math.floor(metadata?.sizeRanges?.widthMaximum || 0)}
									className={"size"}
								/>
							</div>
						</div>
					</div>
					<div class="row">
						<div class="column">
							<div class="row">
								<h4>Height</h4>
							</div>
							<div class="row">
								<ScrollableInput
									bind:value={minHeight}
									bind:relatedValue={maxHeight}
									bind:isChanged={minHeightChanged}
									isMinimum={true}
									id={"minHeight"}
									label={"Min"}
									min={Math.floor(metadata?.sizeRanges?.heightMinimum || 0)}
									max={Math.floor(metadata?.sizeRanges?.heightMaximum || 0)}
									className={"size"}
								/>
								<ScrollableInput
									bind:value={maxHeight}
									bind:relatedValue={minHeight}
									bind:isChanged={maxHeightChanged}
									isMinimum={false}
									id={"maxHeight"}
									label={"Max"}
									min={Math.floor(metadata?.sizeRanges?.heightMinimum || 0)}
									max={Math.floor(metadata?.sizeRanges?.heightMaximum || 0)}
									className={"size"}
								/>
							</div>
						</div>
					</div>
				</div>
			</div>
		{/await}
		<div class="filter-buttons">
			<Button text={"Filter"} on:click={handleFilter} />
			<Button text={"Clear"} style={ButtonStyle.Cancel} on:click={handleClear} />
		</div>
	</aside>
	<div class="column products">
		{#await data.products}
			<div class="product-grid">
				<Skeleton />
			</div>
		{:then products}
			<div class="row {isMobile ? "align-center" : ""}" style:justify-content={"space-between"}>
				Results: {products.length}
				{#if isMobile}
					<Button text={"Filter & Sort"} style={ButtonStyle.Neutral} on:click={toggleSidebar}><Filter /></Button>
				{:else}
					<Dropdown options={sortOptions} bind:selected={sort} change={handleSort} />
				{/if}
			</div>
			<div class="product-grid">
				{#each products as product}
					{#if product.imageUrl}
						<ProductCard product={product} />
					{/if}
				{/each}
			</div>
		{:catch error}
			<div>Something went wrong: {error.message}</div>
		{/await}
	</div>
</div>

<style>
	.container {
		display: grid;
		grid-template-columns: 250px 1fr;
		gap: 1rem;
		padding: 1rem;
		width: 100%; 
		max-width: 1600px;
	}

	.products {
		row-gap: 1rem;
		transition: filter 0.3s ease;
	}

	.product-grid {
		display: grid;
		grid-template-columns: repeat(auto-fit, minmax(298px, 1fr));
		gap: 1rem;
	}

	.filters {
		transition: transform 0.3s ease-in-out;
		z-index: 1000;
	}

	.row {
		display: flex;
		flex-direction: row;
		column-gap: 1rem;
		width: 100%;
	}

	.column {
		display: flex;
		flex-direction: column;
		width: 100%;
		height: 100%;
	}

	.filter-buttons {
		margin-top: 1.33em;
	}

	.close-button {
		background: none;
		border: none;
		font-size: 1.5em;
		cursor: pointer;
		color: #333;
		margin-left: auto;
		transition:
			transform 0.2s ease,
			color 0.2s ease;
	}

	.close-button:hover {
		transform: scale(1.2);
		color: #000;
	}

	.align-center {
		align-items: center;
	}

	@media only screen and (max-width: 974px) {
		.filters {
			position: fixed;
			z-index: 99999;
		}

		.container {
			grid-template-columns: 1fr;
		}

		aside {
			position: fixed;
			top: 0;
			left: 0;
			width: 80%;
			max-width: 300px;
			height: 100%;
			background: white;
			z-index: 20;
			padding: 1rem;
			box-shadow: 2px 0 10px rgba(0,0,0,0.2);
			transform: translateX(-100%);
			transition: transform 0.3s ease;
		}

		aside.open {
			transform: translateX(0);
			z-index: 99999;
			overflow-y: scroll;
		}

		.backdrop {
			position: fixed;
			top: 0;
			left: 0;
			width: 100%;
			height: 100%;
			background: rgba(0,0,0,0.4);
			filter: blur(4px);
			pointer-events: auto;
			z-index: 9999;
		}
	}

	@media only screen and (max-width: 400px) {
		.product-grid {
			grid-template-columns: 1fr;
		}
	}
</style>
