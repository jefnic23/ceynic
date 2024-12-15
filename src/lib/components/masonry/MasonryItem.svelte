<script lang="ts">
	import type { ProductsOut } from "$lib/interfaces/product";
	import { createEventDispatcher } from "svelte";

    export let product: ProductsOut;
    export let loaded: boolean = false;

    const dispatch = createEventDispatcher();

    const onLoad = () => {
		dispatch('load', { id: product.id });
	};
</script>

<div
	class="masonry-item {loaded ? 'visible' : ''}"
	style="opacity: {loaded ? 1 : 0};"
>
	{#if product.imageUrl}
		<a href="/products/{product.id}" data-sveltekit-preload-data>
			<img src={product.imageUrl} alt={product.title} on:load={onLoad} />
		</a>
	{/if}
</div>

<style>
	.masonry-item {
		margin-bottom: 34px;
		display: inline-block;
		vertical-align: top;
		opacity: 0;
		transition: opacity 0.5s ease-in-out;
	}

	.masonry-item.visible {
		opacity: 1;
	}

	img {
		max-width: 225px;
		object-fit: contain;
		transition: all 0.5s ease-in-out;
		backface-visibility: hidden;
	}
</style>