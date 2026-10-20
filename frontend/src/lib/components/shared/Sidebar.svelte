<script lang="ts">
	import Hamburger from "$lib/components/Hamburger.svelte";
	interface Props {
		children?: import('svelte').Snippet;
	}

	let { children }: Props = $props();

    let open: boolean = $state(false);
</script>

<div class="wrapper">
	<div class="hamburger">
		<Hamburger bind:open={open} />
	</div>

	<aside class:open>
		{@render children?.()}
	</aside>
</div>

<style>
    .wrapper {
		display: flex;
		flex-direction: column;
		align-items: flex-start;
		inset-block-start: 0;
		position: sticky;
		z-index: 9999;
		block-size: 100dvh;
		background-color: var(--surface-muted);
		border-inline-end: 1px solid var(--border);
	}

	.hamburger {
		padding: 1rem;
		inline-size: 80px;
		display: flex;
		justify-content: center;
	}

	aside {
		block-size: 100%;
		inline-size: 80px;
		overflow: clip;
		display: flex;
		flex-direction: column;
		align-items: stretch;
	}

	aside.open {
		inline-size: 200px;
	}

	aside:not(.open) :global(.label) {
		display: none;
	}
	@media (prefers-reduced-motion: no-preference) { aside { transition: inline-size 250ms var(--ease-out); } }
</style>
