<script lang="ts">
	import type { Snippet } from 'svelte';
	import Card from './Card.svelte';

	let { children }: { children?: Snippet } = $props();
</script>

<div class="auth-page">
	<Card>
		<div class="auth-body">
			{@render children?.()}
		</div>
	</Card>
</div>

<style>
	.auth-page {
		display: flex;
		align-items: center;
		justify-content: center;
		min-block-size: 100svh;
		padding: 1rem;
	}

	.auth-body {
		display: flex;
		flex-direction: column;
		align-items: center;
		inline-size: min(377px, calc(100vw - 4rem));
	}
</style>
