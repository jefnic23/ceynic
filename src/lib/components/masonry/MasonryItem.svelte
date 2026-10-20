<script lang="ts">
	import ProductImage from '$lib/components/ProductImage.svelte';
	import type { ProductOut } from "$lib/interfaces/ProductOut";
	import { page } from "$app/state";
	import { onMount } from "svelte";

	interface Props {
		product: ProductOut;
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
>
	{#if (product.images?.length as number) > 0}
		<a href="/products/{product.id}" data-sveltekit-preload-data>
			<ProductImage
				url={product.images?.[0]?.url}
				alt={product.title} 
				width={product.images?.[0]?.width}
				height={product.images?.[0]?.height}
				fill
				loading={"lazy"}
				onload={() => load(product.id)}
				data-pin-media={!isMobile && product.images?.[0]?.url ? new URL(product.images[0].url, page.url).href : undefined}
				data-pin-url={!isMobile ? new URL(`/products/${product.id}`, page.url).href : undefined}
				data-pin-description={!isMobile ? product.title : undefined}
				data-pin-no-hover={isMobile ? "true" : undefined}
			/>
		</a>
	{/if}
</div>

<style>
	.masonry-item {
		position: relative;
		inline-size: 100%;
		opacity: 0;
		transition: opacity 0.5s ease-in-out;
	}

	.masonry-item.visible {
		opacity: 1;
	}

	a {
		display: block;
	}
</style>
