<script lang="ts">
	import { enhance } from "$app/forms";
    import Home from '$lib/icons/Home.svelte';
	import Listing from '$lib/icons/Listing.svelte';
	import Logout from "$lib/icons/Logout.svelte";
	import Button from "$lib/components/shared/Button.svelte";
	import ShoppingCart from "$lib/icons/ShoppingCart.svelte";
	import Settings from "$lib/icons/Settings.svelte";

    let open: boolean = true;
</script>

<div class="wrapper">
	<button class="hamburger-button" on:click={() => open = !open} class:open>
		<span></span>
		<span></span>
		<span></span>
		<span></span>
	</button>

	<aside class:open>
		<nav>
			<div>
				<a href="/admin">
					<Home /> 
					<span class="label">Home</span>
				</a>
				<a href="/admin/products">
					<Listing /> 
					<span class="label">Products</span>
				</a>
				<a href="/admin/orders">
					<ShoppingCart />
					<span class="label">Orders</span>
				</a>
				<a href="/admin/settings">
					<Settings />
					<span class="label">Settings</span>
				</a>
			</div>
			<form action="/admin/logout" method="POST" use:enhance>
				<button type="submit">
					<Logout /> 
					<span class="label">Log Out</span>
				</button>
			</form>
		</nav>
	</aside>
</div>

<style>
    .wrapper {
		display: flex;
		align-items: flex-start;
		position: relative;
	}

	aside {
		height: 100vh;
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

	nav {
		display: flex;
		flex-direction: column;
		justify-content: space-between;
		align-items: flex-start;
		height: 100%;
		padding: 1rem;
	}

	nav div {
		display: flex;
		flex-direction: column;
		gap: 0.75rem;
	}

	nav div a,
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
		line-height: normal;
	}

	nav div a:hover,
	nav form button:hover {
		background-color: #eaeaea;
		color: #000;
	}

	nav form {
		margin: 0;
	}

	/* Hide label when sidebar is collapsed */
	aside:not(.open) .label {
		display: none;
	}

	/* Optional: Center icon in collapsed mode */
	aside:not(.open) a,
	aside:not(.open) form button {
		justify-content: center;
	}

	/* hamburger button */
	.hamburger-button {
		position: absolute;
		top: 1rem;
		left: 24px;
		z-index: 2;
		width: 24px;
		height: 16px;
		background: none;
		border: none;
		cursor: pointer;
		padding: 0;
		-webkit-transform: rotate(0deg);
		-moz-transform: rotate(0deg);
		-o-transform: rotate(0deg);
		transform: rotate(0deg);
		-webkit-transition: .5s ease-in-out;
		-moz-transition: .5s ease-in-out;
		-o-transition: .5s ease-in-out;
		transition: .5s ease-in-out;
	}

	.hamburger-button span {
		display: block;
		position: absolute;
		height: 3px;
		width: 100%;
		background: #333;
		border-radius: 2px;
		-webkit-transform: rotate(0deg);
		-moz-transform: rotate(0deg);
		-o-transform: rotate(0deg);
		transform: rotate(0deg);
		-webkit-transition: .25s ease-in-out;
		-moz-transition: .25s ease-in-out;
		-o-transition: .25s ease-in-out;
		transition: .25s ease-in-out;
	}

	.hamburger-button span:nth-child(1) {
		top: 0px;
	}

	.hamburger-button span:nth-child(2), .hamburger-button span:nth-child(3) {
		top: 6px;
	}

	.hamburger-button span:nth-child(4) {
		top: 12px;
	}

	/* Animate into X when open */
	.hamburger-button.open span:nth-child(1) {
		top: 6px;
		width: 0%;
	}

	.hamburger-button.open span:nth-child(2) {
		-webkit-transform: rotate(45deg);
		-moz-transform: rotate(45deg);
		-o-transform: rotate(45deg);
		transform: rotate(45deg);
	}

	.hamburger-button.open span:nth-child(3) {
		-webkit-transform: rotate(-45deg);
		-moz-transform: rotate(-45deg);
		-o-transform: rotate(-45deg);
		transform: rotate(-45deg);
	}

	.hamburger-button.open span:nth-child(4) {
		top: 6px;
		width: 0%;
	}
</style>