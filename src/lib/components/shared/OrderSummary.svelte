<script lang="ts">
	import type { Snippet } from 'svelte';
	import Card from './Card.svelte';

	let { children }: { children?: Snippet } = $props();
</script>

<Card width="100%">
	<h2>Order summary</h2>
	{@render children?.()}
</Card>

<style>
	h2 { margin-block: 0; }
</style>
