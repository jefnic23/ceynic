<script lang="ts">
	import type { Snippet } from 'svelte';
	let { items, summary }: { items: Snippet; summary: Snippet } = $props();
</script>

<div class="cart-layout">
	<div class="items">{@render items()}</div>
	<div class="summary">{@render summary()}</div>
</div>

<style>
	.cart-layout { display: flex; flex-wrap: wrap; align-items: start; gap: 2rem; inline-size: 100%; container-type: inline-size; }
	.items { flex: 999 1 30rem; min-inline-size: 0; }
	.summary { display: flex; flex: 1 1 17rem; flex-direction: column; align-items: flex-end; gap: 2rem; min-inline-size: 0; }
	@container (width < 50rem) { .summary { align-items: center; } }
</style>
