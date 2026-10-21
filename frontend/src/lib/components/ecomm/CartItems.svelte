<script lang="ts">
	import type { ProductOut } from '$lib/interfaces/ProductOut';
	import Card from '$lib/components/shared/Card.svelte';
	import CartItem from './CartItem.svelte';

	let { products, unavailableIds, remove }: { products: ProductOut[]; unavailableIds: number[]; remove: (product: ProductOut) => void } = $props();
</script>

<Card width="100%">
	<div class="cart-items">
		{#each products as product (product.id)}
			<CartItem {product} unavailable={unavailableIds.includes(product.id)} {remove} />
		{/each}
	</div>
</Card>

<style>
	.cart-items { display: flex; flex-direction: column; gap: 2rem; }
</style>
