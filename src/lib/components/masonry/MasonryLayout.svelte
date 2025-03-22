<script lang="ts">
	import Skeleton from '$lib/components/Skeleton.svelte';
	import MasonryItem from '$lib/components/masonry/MasonryItem.svelte';
	import type { ProductsOut } from '$lib/interfaces/product';

	export let products: ProductsOut[] = [];
	let loadedImages = new Set<number>();

	const handleImageLoad = (id: number) => {
		loadedImages.add(id);
		loadedImages = new Set(loadedImages);
	};
</script>

<div class="masonry-layout">
	{#if products.length === 0}
		<Skeleton placeholderCount={12} randomizeHeights={true} type="image" />
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
		column-gap: 34px;
		column-fill: initial;
		max-width: 1002px;
	}

    /* Masonry on large screens */
	@media only screen and (min-width: 1100px) {
		.masonry-layout {
			column-count: 4;
		}
	}

	/* Masonry on medium-sized screens */
	@media only screen and (max-width: 1099px) and (min-width: 850px) {
		.masonry-layout {
			column-count: 3;
			width: 743px;
		}
	}

	/* Masonry on small screens */
	@media only screen and (max-width: 849px) and (min-width: 600px) {
		.masonry-layout {
			column-count: 2;
			width: 484px;
		}
	}

	@media only screen and (max-width: 599px) {
		.masonry-layout {
			column-count: 2;
			column-gap: 13px;
			width: 363px;
		}
	}
</style>
