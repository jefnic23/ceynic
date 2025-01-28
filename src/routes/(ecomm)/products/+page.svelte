<script lang="ts">
	import type { PageData } from './$types';
	import { goto } from '$app/navigation';
	import Dropdown from '$lib/components/Dropdown.svelte';
	import Skeleton from '$lib/components/Skeleton.svelte';
	import Button from '$lib/components/Button.svelte';
	import { ButtonStyle } from '$lib/enums/buttonStyle';
	import { ProductFilter } from '$lib/enums/productFilter';

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
	
	let filters: string[] = [];
	let mediumsChanged: boolean = false;
	let minPriceChanged: boolean = false;
	let maxPriceChanged: boolean = false;
	let minWidthChanged: boolean = false;
	let maxWidthChanged: boolean = false;
	let minHeightChanged: boolean = false;
	let maxHeightChanged: boolean = false;

	let mediums: number[];
	let minPrice: number = 0;
	let maxPrice: number = 0;

	function handleMediums() {
		// todo
	}

	async function loadPriceRange() {
		const range = await data.priceRange;
		minPrice = range?.minimum || 0;
		maxPrice = range?.maximum || 0;
		return range;
	}

	let priceRangePromise = loadPriceRange();

	let minWidth: number = 0;
	let maxWidth: number = 0;
	let minHeight: number = 0;
	let maxHeight: number = 0;

	async function loadSizeRanges() {
		const range = await data.sizeRanges;
		minWidth = range?.widthMinimum || 0;
		maxWidth = range?.widthMaximum || 0;
		minHeight = range?.heightMinimum || 0;
		maxHeight = range?.heightMaximum || 0;
		return range;
	}

	let sizeRangesPromise = loadSizeRanges();

	async function handleSort(event: CustomEvent) {
		sort = event.detail;

		let queryParams = `sort=${sort}`;

		if (filters.length > 0) queryParams = `${queryParams}&${filters.join('&')}`;

		goto(`products?sort=${sort}`, { replaceState: true, keepFocus: true });
	}

	function addFilter(name: string, value: number) {
		filters = [...filters, `${name}=${value}`];
	}

	async function handleFilter() {
		if (minPriceChanged) addFilter(ProductFilter.MinPrice, minPrice);
		if (maxPriceChanged) addFilter(ProductFilter.MaxPrice, maxPrice);
		if (minWidthChanged) addFilter(ProductFilter.MinWidth, minWidth);
		if (maxWidthChanged) addFilter(ProductFilter.MaxWidth, maxPrice);
		if (minHeightChanged) addFilter(ProductFilter.MinHeight, minHeight);
		if (maxHeightChanged) addFilter(ProductFilter.MaxHeight, maxHeight);

		if (filters.length === 0)  return;

		let queryParams = filters.join('&');
		
		if (sort) queryParams = `sort=${sort}&${queryParams}` ;

		goto(`products?${queryParams}`, { replaceState: true, keepFocus: true });
	}

	async function handleClear() {
		if (filters.length === 0) return;
		filters = [];
		goto('products');
	}

	function handleWheel(
		event: WheelEvent,
		value: number,
		setValue: (newValue: number) => void,
		relatedValue?: number,
		isMin?: boolean
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
		}
	}
</script>

<div class="row gap">
	<div class="column small">
		<div class="row">Filter</div>
		<div class="row">
			<div class="column">
				<h4>Medium</h4>
				{#await data.mediumCounts}
					<p>Loading mediums...</p>
				{:then mediumCounts}
					<div class="row justify-left">
						{#each mediumCounts as mediumCount}
							<input
								type="checkbox"
								id={mediumCount.name}
								name={mediumCount.name}
								value={mediumCount.id}
								on:click={() => mediumsChanged = true}
							/>
							<label for={mediumCount.name}>{mediumCount.name} ({mediumCount.count})</label>
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
						<div class="input-container">
							<label for="minimum">Min</label>
							<input
								id="minimum"
								type="number"
								min={priceRange?.minimum}
								max={priceRange?.maximum}
								step="1"
								bind:value={minPrice}
								on:change={() => minPriceChanged = true}
								on:wheel={(e) => handleWheel(e, minPrice, (newValue) => minPrice = newValue, maxPrice, true)}
							/>
						</div>
						<div class="input-container">
							<label for="maximum">Max</label>
							<input
								id="maximum"
								type="number"
								min={priceRange?.minimum}
								max={priceRange?.maximum}
								step="1"
								bind:value={maxPrice}
								on:change={() => maxPriceChanged = true}
								on:wheel={(e) => handleWheel(e, maxPrice, (newValue) => maxPrice = newValue, minPrice, false)}
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
								<div class="input-container">
									<label for="minWidth">Min</label>
									<input
										id="minWidth"
										type="number"
										min={sizeRanges?.widthMinimum}
										max={sizeRanges?.widthMaximum}
										step="1"
										bind:value={minWidth}
										on:change={() => minWidthChanged = true}
										on:wheel={(e) => handleWheel(e, minWidth, (newValue) => minWidth = newValue, maxWidth, true)}
									/>
								</div>
								<div class="input-container">
									<label for="maxWidth">Max</label>
									<input
										id="maxWidth"
										type="number"
										min={sizeRanges?.widthMinimum}
										max={sizeRanges?.widthMaximum}
										step="1"
										bind:value={maxWidth}
										on:change={() => maxWidthChanged = true}
										on:wheel={(e) => handleWheel(e, maxWidth, (newValue) => maxWidth = newValue, minWidth, false)}
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
								<div class="input-container">
									<label for="minHeight">Min</label>
									<input
										id="minHeight"
										type="number"
										min={sizeRanges?.heightMinimum}
										max={sizeRanges?.heightMaximum}
										step="1"
										bind:value={minHeight}
										on:change={() => minHeightChanged = true}
										on:wheel={(e) => handleWheel(e, minHeight, (newValue) => minHeight = newValue, maxHeight, true)}
									/>
								</div>
								<div class="input-container">
									<label for="maxHeight">Max</label>
									<input
										id="maxHeight"
										type="number"
										min={sizeRanges?.heightMinimum}
										max={sizeRanges?.heightMaximum}
										step="1"
										bind:value={maxHeight}
										on:change={() => maxHeightChanged = true}
										on:wheel={(e) => handleWheel(e, maxHeight, (newValue) => maxHeight = newValue, minHeight, true)}
									/>
								</div>
							</div>
						</div>
					</div>
				{/await}
			</div>
		</div>
		<div class="row justify-left">
			<Button text={"Filter"} on:click={handleFilter} />
			<Button text={"Clear"} style={ButtonStyle.Cancel} on:click={handleClear} />
		</div>
	</div>
	<div class="column large">
		{#await data.products}
			<div class="container">
				<Skeleton />
			</div>
		{:then products}
			<div class="row">
				<div>
					Results: {products.length}
				</div>
				<Dropdown options={sortOptions} bind:selected={sort} on:change={handleSort} />
			</div>
			<div class="container">
				{#each products as product}
					<div class="item">
						{#if product.imageUrl}
							<a href="/products/{product.id}" data-sveltekit-preload-data>
								<img src={product.imageUrl} alt={product.title} />
							</a>
						{/if}
						<div class="item-title">{product.title}</div>
						<div style="font-weight: 500;">${product.price}</div>
					</div>
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
		justify-content: space-between;
		align-items: center;
		column-gap: 1rem;
	}

	.column {
		display: flex;
		flex-direction: column;
		height: 100%;
		width: 100%;
	}

	.container {
		display: grid;
		grid-auto-columns: max-content;
		grid-auto-flow: dense;
		grid-auto-rows: minmax(100px, auto);
		grid-gap: 25px;
	}

	.item {
		grid-row: span 1;
		grid-column: span 1;
		margin: auto;
		max-width: 225px;
		line-height: normal;
	}

	.small {
		flex: 1;
		row-gap: 1rem;
		/* border-right: 1px solid #e7e7e7; */
	}

	.large {
		flex: 3;
		row-gap: 1rem;
	}

	.justify-left {
		justify-content: left;
	}

	.gap {
		column-gap: 1rem;
	}

	img {
		max-width: 225px;
		max-height: 225px;
		object-fit: contain;
	}

	.item-title {
		width: 100%;
		max-width: 225px;
		overflow: hidden;
		text-overflow: ellipsis;
		display: inline-block;
		white-space: nowrap;
		font-style: italic;
		color: rgb(112, 112, 112);
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

	.input-container input:focus + label,
	.input-container input:not(:placeholder-shown) + label {
		top: -10px; /* Move the label further up */
		font-size: 0.7em; /* Shrink the label */
		color: #007bff; /* Change color for emphasis */
	}

	/* Masonry on large screens */
	@media only screen and (min-width: 1100px) {
		.container {
			grid-template-columns: repeat(4, 1fr);
		}
	}

	/* Masonry on medium-sized screens */
	@media only screen and (max-width: 1099px) and (min-width: 850px) {
		.container {
			grid-template-columns: repeat(3, 1fr);
		}
	}

	/* Masonry on small screens */
	@media only screen and (max-width: 849px) and (min-width: 600px) {
		.container {
			grid-template-columns: repeat(2, 1fr);
		}
	}

	@media only screen and (max-width: 599px) {
		img {
			width: 175px;
			height: 175px;
		}
	}
</style>
