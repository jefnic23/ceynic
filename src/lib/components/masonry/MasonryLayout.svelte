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
		column-gap: 55px;
		column-fill: initial;
		width: 100%;
	}

    /* Masonry on large screens */
	@media only screen and (min-width: 850px) {
		.masonry-layout {
			column-count: 3;
		}
	}

	/* Masonry on small screens */
	@media only screen and (max-width: 849px) and (min-width: 600px) {
		.masonry-layout {
			column-count: 2;
		}
	}

	@media only screen and (max-width: 599px) {
		.masonry-layout {
			column-count: 1;
		}
	}
</style>
