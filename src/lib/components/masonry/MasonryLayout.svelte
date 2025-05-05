<script lang="ts">
	import Skeleton from '$lib/components/Skeleton.svelte';
	import MasonryItem from '$lib/components/masonry/MasonryItem.svelte';
	import type { ProductsOut } from '$lib/interfaces/product';

	export let products: ProductsOut[] = [];
	let loadedImages = new Set<number>();

	function handleImageLoad (id: number) {
		loadedImages.add(id);
		loadedImages = new Set(loadedImages);
	};

	function randomAspectRatio() {
		// Choose ratios between 3:4 (0.75) and 9:16 (0.5625)
		const min = 0.56;
		const max = 0.75;
		const ratio = Math.random() * (max - min) + min;
		return ratio.toFixed(2);
	}
</script>

<div class="masonry-layout">
	{#if products.length === 0}
		{#each Array(12) as _}
			<div class="masonry-skeleton-item" style="aspect-ratio: 1 / {randomAspectRatio()};">
				<Skeleton />
			</div>
		{/each}
	{:else}
		{#each products as product}
			<MasonryItem
				product={product}
				loaded={loadedImages.has(product.id)}
				on:load={() => handleImageLoad(product.id)}
			/>
		{/each}
	{/if}
</div>

<style>
	.masonry-layout {
		transition: all 0.5s ease-in-out;
		column-gap: 55px;
		column-fill: initial;
		width: 100%;
	}

	.masonry-skeleton-item {
		margin-bottom: 34px;
		width: 100%;
		display: inline-block;
		vertical-align: top;
	}

	/* Masonry on large screens */
	@media only screen and (min-width: 992px) {
		.masonry-layout {
			column-count: 3;
		}
	}

	/* Masonry on small screens */
	@media only screen and (min-width: 768px) and (max-width: 991px) {
		.masonry-layout {
			column-count: 2;
		}
	}

	@media only screen and (max-width: 767px) {
		.masonry-layout {
			column-count: 1;
		}
	}
</style>
