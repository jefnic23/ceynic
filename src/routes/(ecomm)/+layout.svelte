<script lang="ts">
	import { page } from '$app/stores';
	import type { PageData } from './$types';
	import Header from '$lib/components/Header.svelte';
	import Footer from '$lib/components/Footer.svelte';
	import { onNavigate } from '$app/navigation';
	import Cart from '$lib/icons/Cart.svelte';

	onNavigate((navigation) => {
		if (!document.startViewTransition) return;

		return new Promise((resolve) => {
			document.startViewTransition(async () => {
				resolve();
				await navigation.complete;
			});
		});
	});

	export let data: PageData;

	let namePromise: Promise<string> = data.name;
	let name: string = "";

	$: if (namePromise) {
		namePromise.then((value) => {
			name = value;
		});
	}
</script>

<svelte:head>
	<link href="https://fonts.googleapis.com/css2?family=Dancing+Script:wght@400..700&display=swap" rel="stylesheet">
</svelte:head>

<div class="wrapper">
	<Header>
		<div class="header">
			<div class="header-left"></div>
			<div class="header-center">
				<a href="/" data-sveltekit-preload-data class="header-text">{name}</a>
				<nav>
					<a href="/" data-sveltekit-preload-data class:active={$page.url.pathname === '/'}>Home</a>
					<a href="/products" data-sveltekit-preload-data class:active={$page.url.pathname.startsWith('/products')}>Browse</a>
					<a href="/about" data-sveltekit-preload-data class:active={$page.url.pathname === '/about'}>About</a>
					<a href="/contact" class:active={$page.url.pathname === '/contact'}>Contact</a>
				</nav>
			</div>
			<div class="header-right">
				<a href="/cart" class:active={$page.url.pathname === '/cart'}><Cart size={32} /></a>
			</div>
		</div>
	</Header>
	
	{#key data.url}
		<main>
			<slot />
		</main>
	{/key}

	<Footer copyright={name} />
</div>

<style>
	.header {
		min-height: 150px;
		background-color: #f8f8f8;
		border: 1px solid #e7e7e7;
		padding: 1rem;
		display: grid;
		grid-template-columns: 1fr auto 1fr;
		align-items: center;
	}

	nav a {
		text-transform: uppercase;
		margin: 0 0.5rem;
		color: rgba(0, 0, 0, 0.55);
		font-size: 13px;
		transition:
			color 0.15s ease-in-out,
			background-color 0.15s ease-in-out,
			border-color 0.15s ease-in-out;
	}

	nav a.active {
		border-bottom: 2px solid currentColor;
		font-weight: bold;
	}

	a {
		text-decoration: none;
	}

	.header-left {
		display: flex;
		justify-content: flex-end;
		align-items: center;
	}

	.header-center {
		display: flex;
		flex-direction: column;
		align-items: center;
		gap: 0.75rem;
	}

	.header-right {
		display: flex;
		justify-content: flex-end;
		align-items: center;
	}

	.header-right a {
		color: rgba(0, 0, 0, 0.55);
	}

	.header-text {
		font-family: 'Dancing Script', cursive;
		font-weight: 700;
		font-style: normal;
		font-size: xxx-large;
		color: #62b2b2;
		text-align: center;
		text-transform: none;
		margin: 0;
	}

	main {
		position: relative;
		display: flex;
		justify-content: center;
		flex: 1;
		padding: 2rem;
	}

	.wrapper {
		min-height: 100svh;
		display: flex;
		flex-direction: column;
		justify-content: space-between;
	}
</style>
