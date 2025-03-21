<script lang="ts">
	import type { PageData } from './$types';
	import { page } from '$app/stores';
	import { goto } from '$app/navigation';
	import Dropdown from '$lib/components/Dropdown.svelte';
	import Skeleton from '$lib/components/Skeleton.svelte';
	import Button from '$lib/components/shared/Button.svelte';
	import { ButtonStyle } from '$lib/enums/buttonStyle';
	import { ProductFilter } from '$lib/enums/productFilter';
	import type { SizeRanges } from '$lib/interfaces/sizeRanges';
	import type { PriceRange } from '$lib/interfaces/priceRange';
	import ProductCard from '$lib/components/ProductCard.svelte';

	export let data: PageData;

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

	let mediums: string[] = $page.url.searchParams.getAll('medium') || [];

	function handleMedium(medium: string) {
		if (mediums.includes(medium)) {
			mediums = mediums.filter(m => m !== medium);
		} else {
			mediums = [...mediums, medium];
		}
		mediumsChanged = true;
	}

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
		if ($page.url.searchParams.size === 0) return;
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

	function handleWheel(
		event: WheelEvent,
		value: number,
		setValue: (newValue: number) => void,
		setFlag: (newFlag: boolean) => void,
		relatedValue?: number,
		isMin?: boolean,
	): void {
		const input = event.target as HTMLInputElement;

		if (document.activeElement === input) {
			event.preventDefault(); // Prevent page scrolling behavior

			const step = Number(input.step) || 1;
			const min = Number(input.min) || -Infinity;
			const max = Number(input.max) || Infinity;

			// Determine new value based on scroll direction
			let newValue = value + (event.deltaY < 0 ? step : -step);

			// Clamp the value between min and max
			newValue = Math.max(min, Math.min(max, newValue));

			// If this is a min value, make sure it doesn't exceed max
			if (isMin && relatedValue !== undefined) {
				newValue = Math.min(newValue, relatedValue);
			}

			// If this is a max value, make sure it doesn't go below min
			if (!isMin && relatedValue !== undefined) {
				newValue = Math.max(newValue, relatedValue);
			}

			// Update the bound value
			setValue(newValue);

			// Mark the value as updated
			setFlag(true);
		}
	}
</script>

<div class="row gap justify-center">
	<aside class="column filters">
		<div class="row">Filter</div>
		<div class="row">
			<div class="column">
				<h4>Medium</h4>
				{#await data.mediumCounts}
					<p>Loading mediums...</p>
				{:then mediumCounts}
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
				<div class="row">
					<h4>Price</h4>
				</div>
				{#await priceRangePromise}
					<p>Loading price range...</p>
				{:then priceRange}
					<div class="row">
						<div class="input-container price">
							<label for="minimum">Min</label>
							<input
								id="minimum"
								type="number"
								min={priceRange?.minimum}
								max={priceRange?.maximum}
								step="1"
								bind:value={minPrice}
								on:change={() => minPriceChanged = true}
								on:wheel={(e) => handleWheel(e, minPrice, (newValue) => minPrice = newValue, (newFlag) => minPriceChanged = newFlag, maxPrice, true)}
							/>
						</div>
						<div class="input-container price">
							<label for="maximum">Max</label>
							<input
								id="maximum"
								type="number"
								min={priceRange?.minimum}
								max={priceRange?.maximum}
								step="1"
								bind:value={maxPrice}
								on:change={() => maxPriceChanged = true}
								on:wheel={(e) => handleWheel(e, maxPrice, (newValue) => maxPrice = newValue, (newFlag) => maxPriceChanged = newFlag, minPrice, false)}
							/>
						</div>
					</div>
				{/await}
			</div>
		</div>
		<div class="row">
			<div class="column">
				{#await sizeRangesPromise}
					<p>Loading size range...</p>
				{:then sizeRanges}
					<div class="row">
						<div class="column">
							<div class="row">
								<h4>Width</h4>
							</div>
							<div class="row">
								<div class="input-container size">
									<label for="minWidth">Min</label>
									<input
										id="minWidth"
										type="number"
										min={sizeRanges?.widthMinimum}
										max={sizeRanges?.widthMaximum}
										step="1"
										bind:value={minWidth}
										on:change={() => minWidthChanged = true}
										on:wheel={(e) => handleWheel(e, minWidth, (newValue) => minWidth = newValue, (newFlag) => minWidthChanged = newFlag, maxWidth, true)}
									/>
								</div>
								<div class="input-container size">
									<label for="maxWidth">Max</label>
									<input
										id="maxWidth"
										type="number"
										min={sizeRanges?.widthMinimum}
										max={sizeRanges?.widthMaximum}
										step="1"
										bind:value={maxWidth}
										on:change={() => maxWidthChanged = true}
										on:wheel={(e) => handleWheel(e, maxWidth, (newValue) => maxWidth = newValue, (newFlag) => maxWidthChanged = newFlag, minWidth, false)}
									/>
								</div>
							</div>
						</div>
					</div>
					<div class="row">
						<div class="column">
							<div class="row">
								<h4>Height</h4>
							</div>
							<div class="row">
								<div class="input-container size">
									<label for="minHeight">Min</label>
									<input
										id="minHeight"
										type="number"
										min={sizeRanges?.heightMinimum}
										max={sizeRanges?.heightMaximum}
										step="1"
										bind:value={minHeight}
										on:change={() => minHeightChanged = true}
										on:wheel={(e) => handleWheel(e, minHeight, (newValue) => minHeight = newValue, (newFlag) => minHeightChanged = newFlag, maxHeight, true)}
									/>
								</div>
								<div class="input-container size">
									<label for="maxHeight">Max</label>
									<input
										id="maxHeight"
										type="number"
										min={sizeRanges?.heightMinimum}
										max={sizeRanges?.heightMaximum}
										step="1"
										bind:value={maxHeight}
										on:change={() => maxHeightChanged = true}
										on:wheel={(e) => handleWheel(e, maxHeight, (newValue) => maxHeight = newValue, (newFlag) => maxHeightChanged = newFlag, minHeight, false)}
									/>
								</div>
							</div>
						</div>
					</div>
				{/await}
			</div>
		</div>
		<div class="row justify-left filter-buttons">
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
			<div class="row justify-between">
				<div>
					Results: {products.length}
				</div>
				<Dropdown options={sortOptions} bind:selected={sort} on:change={handleSort} />
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
	.row {
		display: flex;
		flex-direction: row;
		width: 100%;
		column-gap: 1rem;
	}

	.column {
		display: flex;
		flex-direction: column;
		height: 100%;
		width: 100%;
	}

	.products {
		flex: 1;
		max-width: 1144px;
	}

	.product-grid {
		display: flex;
		flex-wrap: wrap;
		gap: 25px;
		justify-content: flex-start;
		margin-top: 13px;
	}

	.justify-center {
		justify-content: center;
	}

	.justify-left {
		justify-content: left;
	}

	.justify-between {
		justify-content: space-between;
	}

	.gap {
		column-gap: 1rem;
	}

	.input-container {
		position: relative;
		display: inline-block;
		width: 100%;
	}

	.input-container label {
		position: absolute;
		top: 21%; /* Adjust as needed */
		left: 13px; /* Adjust for padding */
		transform: translateY(-100%); /* Moves it upwards */
		background: white; /* To overlay on input without blending */
		padding: 0 5px; /* Space around the text */
		font-size: 0.8em; /* Adjust the size */
		transition: all 0.2s ease;
	}

	.input-container input {
		width: 100%;
		padding: 10px;
		font-size: 1em;
		box-sizing: border-box;
	}

	.price input {
		padding-left: 1rem; /* Add space for the dollar sign */
	}

	.price::before {
		content: '$';
		position: absolute;
		left: 0.5em; /* Adjust positioning as needed */
		top: 50%;
		transform: translateY(-50%);
		font-size: 1em;
		font-weight: bold;
		color: #333; /* Adjust color as needed */
	}

	.size::after {
		content: 'in.';
		position: absolute;
		right: 2rem; /* Adjust positioning as needed */
		top: 50%;
		transform: translateY(-50%);
		line-height: normal;
		font-size: 1em;
		font-weight: bold;
		color: #333; /* Adjust color as needed */
	}

	.input-container input:focus + label,
	.input-container input:not(:placeholder-shown) + label {
		top: -10px; /* Move the label further up */
		font-size: 0.7em; /* Shrink the label */
		color: #007bff; /* Change color for emphasis */
	}

	.filters {
		max-width: 250px;
		min-width: 250px;
	}

	.filter-buttons {
		margin-top: 1.33em;
	}

	@media only screen and (max-width: 1440px) and (min-width: 1150px) {
		.products {
			max-width: 854px;
		}
	}

	@media only screen and (max-width: 1149px) and (min-width: 857px) {
		.products {
			max-width: 560px;
		}
	}

	@media only screen and (max-width: 856px) {
		.products {
			max-width: calc(100% - 250px);
		}

		.product-grid {
			justify-content: center;
		}
	}
</style>
