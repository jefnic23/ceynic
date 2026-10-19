<script lang="ts">
	import type { Snippet } from 'svelte';

	let { href, children }: { href: string; children?: Snippet } = $props();
</script>

<a {href} data-sveltekit-preload-data>{@render children?.()}</a>

<style>
	a {
		display: inline-flex;
		align-items: center;
		justify-content: center;
		gap: 5px;
		border-radius: 0.25rem;
		padding-block: 0.5rem;
		padding-inline: 1.5rem;
		background: var(--info);
		color: var(--surface);
		text-decoration: none;
	}
	a:focus-visible { outline-color: var(--info); }
	a:active { filter: brightness(0.88); }
	@media (hover: hover) and (pointer: fine) { a:hover { filter: brightness(0.95); } }
</style>
