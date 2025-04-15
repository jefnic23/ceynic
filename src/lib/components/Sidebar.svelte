<script lang="ts">
	import { enhance } from "$app/forms";
	import Hamburger from "$lib/icons/Hamburger.svelte";
    import Home from '$lib/icons/Home.svelte';
	import Listing from '$lib/icons/Listing.svelte';
	import Logout from "$lib/icons/Logout.svelte";
	import Button from "$lib/components/shared/Button.svelte";

    let open: boolean = true;
</script>

<div class="wrapper">
	<button class="hamburger-button" on:click={() => open = !open}>
		<Hamburger />
	</button>

	<aside class:open>
	
		{#if open}
			<nav>
				<a href="/admin"><Home /> <span>Home</span></a>
				<a href="/admin/products"><Listing /> <span>Products</span></a>
				<form action="/admin/logout" method="POST" use:enhance>
					<button type="submit"><Logout /> <span>Log Out</span></button>
				</form>
			</nav>
		{/if}
	</aside>
</div>

<style>
    .wrapper {
		display: flex;
		align-items: flex-start;
		position: relative;
	}

	.hamburger-button {
		position: absolute;
		top: 1rem;
		left: 1rem;
		z-index: 2;
		background: none;
		border: none;
		cursor: pointer;
		padding: 0.5rem;
	}

	aside {
		height: 100vh;
		width: 80px;
		overflow: hidden;
		background-color: #f9f9f9;
		border-right: 1px solid #e0e0e0;
		transition: width 0.3s ease;
		display: flex;
		flex-direction: column;
		padding-top: 3rem; /* Leave room for the hamburger */
	}

	aside.open {
		width: 200px;
	}

	nav {
		display: flex;
		flex-direction: column;
		gap: 0.75rem;
		padding: 1rem;
	}

	nav a,
	nav form button {
		display: flex;
		align-items: center;
		gap: 0.5rem;
		text-transform: uppercase;
		color: rgba(0, 0, 0, 0.65);
		font-size: 0.875rem;
		text-decoration: none;
		background: none;
		border: none;
		padding: 0.5rem;
		transition: background 0.2s ease, color 0.2s ease;
		border-radius: 4px;
		width: 100%;
		cursor: pointer;
	}

	nav a:hover,
	nav form button:hover {
		background-color: #eaeaea;
		color: #000;
	}

	nav form {
		margin: 0;
	}
</style>