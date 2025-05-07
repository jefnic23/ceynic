<script lang="ts">
	import { enhance } from "$app/forms";
    import Home from '$lib/icons/Home.svelte';
	import Listing from '$lib/icons/Listing.svelte';
	import Logout from "$lib/icons/Logout.svelte";
	import Settings from "$lib/icons/Settings.svelte";
	import Person from "$lib/icons/Person.svelte";
	import type { LayoutData } from './$types';
	import Sidebar from '$lib/components/shared/Sidebar.svelte';
	import { onNavigate } from '$app/navigation';
	import Box from "$lib/icons/Box.svelte";

	onNavigate((navigation) => {
		if (!document.startViewTransition) return;

		return new Promise((resolve) => {
			document.startViewTransition(async () => {
				resolve();
				await navigation.complete;
			});
		});
	});
	
	export let data: LayoutData;
</script>

<div class="container">
	<Sidebar>
		<nav>
			<div>
				<a href="/admin">
					<Home /> 
					<span class="label">Home</span>
				</a>
				<a href="/admin/products" data-sveltekit-preload-data>
					<Listing /> 
					<span class="label">Products</span>
				</a>
				<a href="/admin/orders" data-sveltekit-preload-data>
					<Box />
					<span class="label">Orders</span>
				</a>
				<a href="/admin/settings">
					<Settings />
					<span class="label">Settings</span>
				</a>
				<a href="/admin/account">
					<Person />
					<span class="label">Account</span>
				</a>
			</div>
			<form action="/admin/logout" method="POST" use:enhance>
				<button type="submit">
					<Logout /> 
					<span class="label">Log Out</span>
				</button>
			</form>
		</nav>
	</Sidebar>

	{#key data.url}
		<main>
			<slot />
		</main>
	{/key}
</div>

<style>
	.container {
		display: flex;
		flex-direction: row;
	}

	main {
		width: 100%;
		display: flex;
		justify-content: center;
		align-items: flex-start;
		margin: 1rem;
		view-transition-name: main;
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
		font-size: 1rem;
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
</style>