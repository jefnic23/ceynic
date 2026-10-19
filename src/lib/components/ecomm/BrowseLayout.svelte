<script lang="ts">
	import type { Snippet } from 'svelte';
	let { enabled, filters, children }: { enabled: boolean; filters?: Snippet; children?: Snippet } = $props();
</script>

<div class:enabled class="browse-layout">
	{#if enabled}{@render filters?.()}{/if}
	<div class="products">{@render children?.()}</div>
</div>

<style>
	.browse-layout { display: grid; grid-template-columns: minmax(0, 1fr); gap: 1rem; padding: 1rem; inline-size: 100%; max-inline-size: 1600px; }
	.browse-layout.enabled { grid-template-columns: 250px minmax(0, 1fr); }
	.products { display: flex; flex-direction: column; gap: 1rem; min-inline-size: 0; }
	@media (width <= 974px) { .browse-layout.enabled { grid-template-columns: minmax(0, 1fr); } }
</style>
