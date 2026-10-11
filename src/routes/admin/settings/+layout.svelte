<script lang="ts">
	import { page } from '$app/state';
	import Card from '$lib/components/shared/Card.svelte';
	import type { Snippet } from 'svelte';

	let { children }: { children: Snippet } = $props();
</script>

<div class="wrapper">
	<Card width="100%">
		<h1>Settings</h1>
		<nav aria-label="Settings sections">
			<a href="/admin/settings" aria-current={page.url.pathname === '/admin/settings' ? 'page' : undefined}>Site</a>
			<a href="/admin/settings/payments" aria-current={page.url.pathname === '/admin/settings/payments' ? 'page' : undefined}>Payments</a>
		</nav>
		{@render children()}
	</Card>
</div>

<style>
	.wrapper {
		width: 100%;
	}

	nav {
		display: flex;
		gap: 1.5rem;
		border-bottom: 1px solid #ddd;
		margin-bottom: 1.5rem;
	}

	a {
		color: rgba(0, 0, 0, 0.65);
		padding: 0.5rem 0;
		text-decoration: none;
		border-bottom: 2px solid transparent;
	}

	a:hover,
	a[aria-current='page'] {
		color: #000;
	}

	a[aria-current='page'] {
		border-bottom-color: currentColor;
	}
</style>
