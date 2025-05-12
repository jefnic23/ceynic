<script lang="ts">
	import Hamburger from "$lib/components/Hamburger.svelte";

    let open: boolean = false;
</script>

<div class="wrapper">
	<div class="hamburger">
		<Hamburger bind:open={open} />
	</div>

	<aside class:open>
		<slot />
	</aside>
</div>

<style>
    .wrapper {
		display: flex;
		flex-direction: column;
		align-items: flex-start;
		position: relative;
		z-index: 9999;
		height: 100vh;
		background-color: #f9f9f9;
		border-right: 1px solid #e0e0e0;
	}

	.hamburger {
		padding: 1rem;
		width: 72px;
		display: flex;
		justify-content: center;
	}

	aside {
		height: 100%;
		width: 72px;
		overflow: hidden;
		transition: width 0.3s ease;
		display: flex;
		flex-direction: column;
		align-items: stretch;
	}

	aside.open {
		width: 200px;
	}

	aside:not(.open) :global(.label) {
		display: none;
	}
</style>