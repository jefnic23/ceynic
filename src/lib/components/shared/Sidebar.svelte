<script lang="ts">
	import Hamburger from "../Hamburger.svelte";

    let open: boolean = false;
</script>

<div class="wrapper">
	<Hamburger bind:open={open} />

	<aside class:open>
		<slot />
	</aside>
</div>

<style>
    .wrapper {
		display: flex;
		align-items: flex-start;
		position: relative;
		z-index: 9999;
		height: 100vh;
		position: fixed;
	}

	aside {
		height: 100%;
		width: 72px;
		overflow: hidden;
		background-color: #f9f9f9;
		border-right: 1px solid #e0e0e0;
		transition: width 0.3s ease;
		display: flex;
		flex-direction: column;
		padding-top: 3rem; /* Leave room for the hamburger */
		align-items: stretch;
	}

	aside.open {
		width: 200px;
	}

	aside:not(.open) :global(.label) {
		display: none;
	}
</style>