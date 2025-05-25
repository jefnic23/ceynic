<script lang="ts">
	import type { ProductsOut } from "$lib/interfaces/ProductsOut";
	import { page } from "$app/state";
	import { onMount } from "svelte";

	interface Props {
		product: ProductsOut;
		loaded?: boolean;
		load: CallableFunction;
	}

	let { product, loaded = false, load }: Props = $props();

	let isMobile = $state(false);

	onMount(() => {
		isMobile = window.innerWidth <= 768;
	});
</script>

<div
	class="masonry-item {loaded ? 'visible' : ''}"
	style="opacity: {loaded ? 1 : 0};"
>
	{#if product.imageUrl}
		<a href="/products/{product.id}" data-sveltekit-preload-data>
			<img 
				src={product.imageUrl} 
				alt={product.title} 
				onload={() => load(product.id)}
				loading="lazy"
				data-pin-do={!isMobile ? "buttonPin" : undefined}
				data-pin-media={!isMobile ? product.imageUrl : undefined}
				data-pin-url={!isMobile ? page.url : undefined}
				data-pin-description={!isMobile ? product.title : undefined}
				data-pin-no-hover={isMobile ? "true" : undefined}
			/>
		</a>
	{/if}
</div>

<style>
	.masonry-item {
		position: relative;
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
		width: 100%;
		object-fit: contain;
		transition: all 0.5s ease-in-out;
		backface-visibility: hidden;
	}
</style>