<script lang="ts">
	import type { ProductOut } from '$lib/interfaces/ProductOut';
	import ProductCard from '$lib/components/ProductCard.svelte';
	let { products }: { products: ProductOut[] } = $props();
</script>

<div class="product-grid">
	{#each products as product (product.id)}
		{#if (product.images?.length ?? 0) > 0}
			<ProductCard {product} />
		{/if}
	{/each}
</div>

<style>
	.product-grid {
		display: grid;
		grid-template-columns: repeat(auto-fill, minmax(min(100%, 298px), 1fr));
		gap: 1rem;
	}
</style>
