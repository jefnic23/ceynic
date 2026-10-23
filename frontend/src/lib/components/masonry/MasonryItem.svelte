<script lang="ts">
	import ProductImage from '$lib/components/ProductImage.svelte';
	import PinterestSave from '$lib/components/ecomm/PinterestSave.svelte';
	import type { ProductOut } from "$lib/interfaces/ProductOut";
	import { page } from "$app/state";

	interface Props {
		product: ProductOut;
		loaded?: boolean;
		load: CallableFunction;
		pinterestEnabled: Promise<boolean>;
	}

	let { product, loaded = false, load, pinterestEnabled }: Props = $props();
</script>

<div
	class="masonry-item pinterest-save-target {loaded ? 'visible' : ''}"
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
			/>
		</a>
		<PinterestSave
			enabled={pinterestEnabled}
			imageUrl={product.images?.[0]?.url ? new URL(product.images[0].url, page.url).href : undefined}
			productUrl={new URL(`/products/${product.id}`, page.url).href}
			description={product.title}
		/>
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
