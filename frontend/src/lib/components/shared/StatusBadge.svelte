<script lang="ts">
	import type { Snippet } from 'svelte';

	let { tone = 'neutral', children }: {
		tone?: 'neutral' | 'success' | 'error';
		children?: Snippet;
	} = $props();
</script>

<span class="badge {tone}">{@render children?.()}</span>

<style>
	.badge {
		display: inline-flex;
		align-items: center;
		gap: 0.25rem;
		padding-block: 0.25rem;
		padding-inline: 0.5rem;
		border-radius: 9999px;
		background: oklch(0.96 0.005 255);
		color: oklch(0.34 0.04 255);
		font-size: 0.75rem;
		font-weight: 600;
	}
	.success { background: oklch(0.97 0.03 145); color: oklch(0.44 0.12 145); }
	.error { background: oklch(0.97 0.025 25); color: oklch(0.44 0.16 25); }
</style>
