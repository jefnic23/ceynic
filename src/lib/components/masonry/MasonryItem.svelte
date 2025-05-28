<script lang="ts">
	import type { ProductImageOut, ProductOut } from "$lib/interfaces/ProductOut";
	import { page } from "$app/state";
	import { onMount } from "svelte";
	import { CldImage } from "svelte-cloudinary";

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
	style="opacity: {loaded ? 1 : 0};"
>
	{#if (product.images?.length as number) > 0}
		<a href="/products/{product.id}" data-sveltekit-preload-data>
			<CldImage 
				src={(product.images as ProductImageOut[])[0]?.publicId} 
				alt={product.title} 
				width={(product.images as ProductImageOut[])[0]?.width}
				height={(product.images as ProductImageOut[])[0]?.height}
				loading={"lazy"}
				onload={() => load(product.id)}
				data-pin-do={!isMobile ? "buttonPin" : undefined}
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
</style>