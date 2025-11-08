<script lang="ts">
	import type { Snippet } from "svelte";
	import { enhance } from "$app/forms";
	import type { LayoutData } from './$types';
	import Sidebar from '$lib/components/shared/Sidebar.svelte';
	import { onNavigate } from '$app/navigation';
	import Icon from "@iconify/svelte";

	onNavigate((navigation) => {
		if (!document?.startViewTransition) return;

		return new Promise((resolve) => {
			document?.startViewTransition(async () => {
				resolve();
				await navigation.complete;
			});
		});
	});
	
	interface Props {
		data: LayoutData;
		children?: Snippet;
	}

	let { data, children }: Props = $props();
</script>

<div class="container">
	<Sidebar>
		<div class="sidebar">
			<nav>
				<a href="/admin" title="Home">
					<Icon icon="material-symbols:home-rounded" width={32} height={32} />
					<span class="label">Home</span>
				</a>
				<a href="/admin/products" title="Products" data-sveltekit-preload-data>
					<Icon icon="material-symbols:list-alt" width={32} height={32}  />
					<span class="label">Products</span>
				</a>
				<a href="/admin/orders" title="Orders" data-sveltekit-preload-data>
					<Icon icon="material-symbols:box" width={32} height={32}  />
					<span class="label">Orders</span>
				</a>
				<a href="/admin/settings" title="Settings">
					<Icon icon="material-symbols:settings-rounded" width={32} height={32}  />
					<span class="label">Settings</span>
				</a>
				<a href="/admin/account" title="Account">
					<Icon icon="material-symbols:person" width={32} height={32}  />
					<span class="label">Account</span>
				</a>
			</nav>
			<form action="/admin/logout" method="POST" use:enhance>
				<button type="submit" title="Log Out">
					<Icon icon="material-symbols:logout-rounded" width={32} height={32}  />
					<span class="label">Log Out</span>
				</button>
			</form>
		</div>
	</Sidebar>

	{#key data.url}
		<main>
			{@render children?.()}
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

	.sidebar {
		display: flex;
		flex-direction: column;
		justify-content: space-between;
		height: 100%;
	}

	nav {
		display: flex;
		flex-direction: column;
		justify-content: space-between;
		align-items: flex-start;
		padding: 1rem;
		gap: 1rem;
	}

	nav a,
	form button {
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
		width: fit-content;
		cursor: pointer;
		line-height: normal;
		justify-content: flex-start;
	}

	nav a:hover,
	form button:hover {
		background-color: #eaeaea;
		color: #000;
	}

	form {
		margin: 0;
		padding: 1rem;
	}

	.label {
		transition: opacity 0.2s ease;
		white-space: nowrap;
	}
</style>