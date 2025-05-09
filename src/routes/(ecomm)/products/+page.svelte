<script lang="ts">
	import { slide } from 'svelte/transition';
	import type { PageData } from './$types';
	import { page } from '$app/stores';
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

	export let data: PageData;

	let isMobile = false;
	let showFilters = false;

	$: {
		if (showFilters) {
			document.body.classList.add('no-scroll');
		} else {
			document.body.classList.remove('no-scroll');
		}
	}

	onMount(() => {
		const checkMobile = () => {
			isMobile = window.matchMedia("(max-width: 974px)").matches;
		};

		checkMobile();
		window.addEventListener("resize", checkMobile);
		return () => window.removeEventListener("resize", checkMobile);
	});

	onDestroy(() => {
		document.body.classList.remove('no-scroll');
	});

	function toggleSidebar() {
		showFilters = !showFilters;
	}

	let sort: string = '';
	const sortOptions = [
		{ value: 'newest', label: 'Newest' },
		{ value: 'oldest', label: 'Oldest' },
		{ value: 'price_asc', label: 'Lowest Price' },
		{ value: 'price_desc', label: 'Highest Price' },
		{ value: 'size_asc', label: 'Smallest' },
		{ value: 'size_desc', label: 'Largest' }
	];
	
	let mediumsChanged: boolean = false;
	let minPriceChanged: boolean = false;
	let maxPriceChanged: boolean = false;
	let minWidthChanged: boolean = false;
	let maxWidthChanged: boolean = false;
	let minHeightChanged: boolean = false;
	let maxHeightChanged: boolean = false;
	$: filterApplied = mediumsChanged || minPriceChanged || maxPriceChanged || minWidthChanged || maxWidthChanged || minHeightChanged || maxHeightChanged;

	let mediums: string[] = $page.url.searchParams.getAll('medium') || [];

	function handleMedium(medium: string) {
		if (mediums.includes(medium)) {
			mediums = mediums.filter(m => m !== medium);
		} else {
			mediums = [...mediums, medium];
		}
		mediumsChanged = true;
	}

	async function loadMediumCounts(): Promise<MediumCount[]> {
		return await data.mediumCounts;
	}

	let mediumCountsPromise = loadMediumCounts();

	let minPrice: number = parseInt($page.url.searchParams.get(ProductFilter.MinPrice) as string) || 0;
	let maxPrice: number = parseInt($page.url.searchParams.get(ProductFilter.MaxPrice) as string) || 0;

	async function loadPriceRange(): Promise<PriceRange> {
		const range = await data.priceRange;
		minPrice = Math.floor(range?.minimum) || 0;
		maxPrice = Math.floor(range?.maximum) || 0;
		return range;
	}

	let priceRangePromise = loadPriceRange();

	let minWidth: number = parseInt($page.url.searchParams.get(ProductFilter.MinWidth) as string) || 0;
	let maxWidth: number = parseInt($page.url.searchParams.get(ProductFilter.MaxWidth) as string) || 0;
	let minHeight: number = parseInt($page.url.searchParams.get(ProductFilter.MinHeight) as string) || 0;
	let maxHeight: number = parseInt($page.url.searchParams.get(ProductFilter.MaxHeight) as string) || 0;

	async function loadSizeRanges(): Promise<SizeRanges> {
		const range = await data.sizeRanges;
		minWidth = Math.floor(range?.widthMinimum) || 0;
		maxWidth = Math.floor(range?.widthMaximum) || 0;
		minHeight = Math.floor(range?.heightMinimum) || 0;
		maxHeight = Math.floor(range?.heightMaximum) || 0;
		return range;
	}

	let sizeRangesPromise = loadSizeRanges();

	async function handleSort(event: CustomEvent) {
		const url = new URL(window.location.href);
		url.searchParams.set('sort', event.detail);
		await goto(url, { replaceState: true, keepFocus: true });
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

		if (url.searchParams.size === 0)  return;

		await goto(url, { replaceState: true, keepFocus: true });
	}

	async function handleClear() {
		if (isMobile) toggleSidebar();
		if ($page.url.searchParams.size === 0 && !filterApplied) return;
		mediums = [];
		await loadPriceRange();
		await loadSizeRanges();
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
    <div class="backdrop" on:click={toggleSidebar}></div>
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
					<button  class="close-button" on:click={toggleSidebar}>&times;</button>
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
					<Dropdown options={sortOptions} bind:selected={sort} on:change={handleSort} />
				</div>
			</div>
		{/if}
		<div class="row">
			<div class="column">
				{#await mediumCountsPromise}
					<Skeleton />
				{:then mediumCounts}
					<h4>Medium</h4>
					<div class="column">
						{#each mediumCounts as mediumCount}
							<div class="row justify-left">
								<input
									type="checkbox"
									id={mediumCount.name}
									name={mediumCount.name}
									value={mediumCount.id}
									checked={mediums.includes(mediumCount.name)}
									on:click={() => handleMedium(mediumCount.name)}
								/>
								<label for={mediumCount.name}>{mediumCount.name} ({mediumCount.count})</label>
							</div>
						{/each}
					</div>
				{/await}
			</div>
		</div>
		<div class="row">
			<div class="column">
				{#await priceRangePromise}
					<Skeleton />
				{:then priceRange}
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
							min={priceRange?.minimum}
							max={priceRange?.maximum}
							className={"price"}
						/>
						<ScrollableInput
							bind:value={maxPrice}
							bind:relatedValue={minPrice}
							bind:isChanged={maxPriceChanged}
							isMinimum={false}
							id={"maxPrice"}
							label={"Max"}
							min={priceRange?.minimum}
							max={priceRange?.maximum}
							className={"price"}
						/>
					</div>
				{/await}
			</div>
		</div>
		<div class="row">
			<div class="column">
				{#await sizeRangesPromise}
					<Skeleton />
				{:then sizeRanges}
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
									min={sizeRanges?.widthMinimum}
									max={sizeRanges?.widthMaximum}
									className={"size"}
								/>
								<ScrollableInput
									bind:value={maxWidth}
									bind:relatedValue={minWidth}
									bind:isChanged={maxWidthChanged}
									isMinimum={false}
									id={"maxWidth"}
									label={"Max"}
									min={sizeRanges?.widthMinimum}
									max={sizeRanges?.widthMaximum}
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
									min={sizeRanges?.heightMinimum}
									max={sizeRanges?.heightMaximum}
									className={"size"}
								/>
								<ScrollableInput
									bind:value={maxHeight}
									bind:relatedValue={minHeight}
									bind:isChanged={maxHeightChanged}
									isMinimum={false}
									id={"maxHeight"}
									label={"Max"}
									min={sizeRanges?.heightMinimum}
									max={sizeRanges?.heightMaximum}
									className={"size"}
								/>
							</div>
						</div>
					</div>
				{/await}
			</div>
		</div>
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
					<button on:click={toggleSidebar}><Filter /> Filter & Sort</button>
				{:else}
					<Dropdown options={sortOptions} bind:selected={sort} on:change={handleSort} />
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
