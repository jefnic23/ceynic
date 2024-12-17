<script lang="ts">
	import type { PageData } from './$types';
	import { goto } from '$app/navigation';
	import Dropdown from '$lib/components/Dropdown.svelte';
	import Slider from '$lib/components/Slider.svelte';

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

	async function handleSort(event: CustomEvent) {
		sort = event.detail;
		goto(`products?sort=${sort}`, { replaceState: true, keepFocus: true });
	}

	let currentMin: number;
	let currentMax: number;

	function handlePriceChange(event: CustomEvent) {
		const { min, max } = event.detail;
		currentMin = min;
		currentMax = max;
	}
</script>

<div class="row">
	<div class="column small">
		<div class="row">Filter</div>
		<div class="row">
			<div class="column">
				<div>Medium</div>
				<div class="column">
					<input type="checkbox" id="painting" name="painting" value="Painting" />
					<label for="painting">Painting</label>
					<input type="checkbox" id="print" name="print" value="Print" />
					<label for="print">Print</label>
				</div>
			</div>
		</div>
		<div class="row">
			<div class="column">
				<div>Price range</div>
				{#await data.priceRange}
					<Slider />
				{:then priceRange}
					<Slider
						min={priceRange?.minimum}
						max={priceRange?.maximum}
						bind:selectedMin={currentMin}
						bind:selectedMax={currentMax}
						on:change={handlePriceChange}
					/>
				{/await}
			</div>
		</div>
	</div>
	<div class="column large">
		{#await data.products}
			<div>loading products...</div>
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
						<div style="font-weight: bold;">${product.price}</div>
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
	}

	.column {
		display: flex;
		flex-direction: column;
		padding: 1rem;
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
	}

	.small {
		flex: 1;
		border-right: 1px solid #e7e7e7;
	}

	.large {
		flex: 3;
		row-gap: 1rem;
	}

	img {
		max-width: 225px;
		max-height: 225px;
		object-fit: contain;
	}

	.item-title {
		max-width: 225px;
		overflow: hidden;
		text-overflow: ellipsis;
		display: inline-block;
		white-space: nowrap;
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
