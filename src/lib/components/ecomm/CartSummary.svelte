<script lang="ts">
	import type { Snippet } from 'svelte';
	import Card from '$lib/components/shared/Card.svelte';
	import { currencyFormatter } from '$lib/utils/formatters';

	let { count, subtotal, children }: { count: number; subtotal: number; children?: Snippet } = $props();
</script>

<Card width="100%">
	<div class="summary-content">
		<h2>Order Summary</h2>
		<div class="subtotal"><span>Subtotal ({count}):</span><span class="price">{currencyFormatter.format(subtotal)}</span></div>
		{@render children?.()}
	</div>
</Card>

<style>
	.summary-content { display: flex; flex-direction: column; align-items: center; gap: 1rem; }
	h2 { margin-block: 0; }
	.subtotal { display: flex; justify-content: space-between; gap: 1rem; inline-size: 100%; }
</style>
