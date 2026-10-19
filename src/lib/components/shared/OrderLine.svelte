<script lang="ts">
	import type { Snippet } from 'svelte';

	let { total = false, children }: { total?: boolean; children?: Snippet } = $props();
</script>

<div class:total class="order-line">{@render children?.()}</div>

<style>
	.order-line {
		display: flex;
		justify-content: space-between;
		gap: 1rem;
		padding-block: 0.75rem;
	}
	.total { border-block-start: 1px solid var(--border); }
</style>
