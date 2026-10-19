<script lang="ts">
	import type { Snippet } from 'svelte';

	let { max = '750px', children }: { max?: string; children?: Snippet } = $props();
</script>

<div class="page-container" style:--page-max={max}>
	{@render children?.()}
</div>

<style>
	.page-container {
		--gutter: 0px;
		--content: var(--page-max);
		--breakout: var(--page-max);
		display: grid;
		inline-size: 100%;
		min-inline-size: 0;
		grid-template-columns:
			[full-width-start] minmax(var(--gutter), 1fr)
			[breakout-start] minmax(0, calc((var(--breakout) - var(--content)) / 2))
			[content-start] min(100% - var(--gutter) * 2, var(--content)) [content-end]
			minmax(0, calc((var(--breakout) - var(--content)) / 2)) [breakout-end]
			minmax(var(--gutter), 1fr) [full-width-end];
	}
	.page-container > :global(*) { grid-column: content; min-inline-size: 0; }
	.page-container > :global(.breakout) { grid-column: breakout; }
	.page-container > :global(.full-width) { grid-column: full-width; display: grid; grid-template-columns: inherit; }
	.page-container > :global(.full-width) > :global(*) { grid-column: content; }
</style>
