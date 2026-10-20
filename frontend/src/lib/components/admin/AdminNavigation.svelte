<script lang="ts">
	import { enhance } from '$app/forms';
	import { page } from '$app/state';
	import Icon from '@iconify/svelte';
	import Sidebar from '$lib/components/shared/Sidebar.svelte';
	import Button from '$lib/components/shared/Button.svelte';

	const links = [
		{ href: '/admin', label: 'Home', icon: 'material-symbols:home-rounded' },
		{ href: '/admin/products', label: 'Products', icon: 'material-symbols:list-alt' },
		{ href: '/admin/orders', label: 'Orders', icon: 'material-symbols:box' },
		{ href: '/admin/settings', label: 'Settings', icon: 'material-symbols:settings-rounded' },
		{ href: '/admin/account', label: 'Account', icon: 'material-symbols:person' }
	];
</script>

<Sidebar>
	<div class="sidebar-content">
		<nav aria-label="Administration">
			{#each links as link (link.href)}
				<a href={link.href} title={link.label} aria-current={page.url.pathname === link.href ? 'page' : undefined} data-sveltekit-preload-data>
					<Icon icon={link.icon} width={32} height={32} />
					<span class="label">{link.label}</span>
				</a>
			{/each}
		</nav>
		<form action="/admin/logout" method="POST" use:enhance>
			<Button type="submit" title="Log Out" appearance="plain" class="sidebar-button">
				<Icon icon="material-symbols:logout-rounded" width={32} height={32} />
				<span class="label">Log Out</span>
			</Button>
		</form>
	</div>
</Sidebar>

<style>
	.sidebar-content { display: flex; flex-direction: column; justify-content: space-between; block-size: 100%; }
	nav { display: flex; flex-direction: column; align-items: flex-start; gap: 1rem; padding: 1rem; }
	nav a,
	form :global(button.sidebar-button) {
		display: flex;
		align-items: center;
		justify-content: flex-start;
		gap: 0.5rem;
		text-transform: uppercase;
		color: color-mix(in oklch, var(--ink) 65%, transparent);
		font-size: 1rem;
		text-decoration: none;
		background: none;
		border: 0;
		padding: 0.5rem;
		border-radius: 4px;
		inline-size: fit-content;
		cursor: pointer;
		line-height: normal;
	}
	nav a:active,
	form :global(button.sidebar-button:active) { background: var(--border); color: var(--ink); }
	@media (hover: hover) and (pointer: fine) {
		nav a:hover,
		form :global(button.sidebar-button:hover) { background: var(--border); color: var(--ink); }
	}
	form { margin: 0; padding: 1rem; }
	.label { white-space: nowrap; }
</style>
