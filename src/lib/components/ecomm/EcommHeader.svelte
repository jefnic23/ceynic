<script lang="ts">
	import Header from "$lib/components/shared/Header.svelte";
	import { onDestroy, onMount } from "svelte";
	import Hamburger from "../Hamburger.svelte";
	import Icon from "@iconify/svelte";
	import { cart } from "$lib/state/cart.svelte";

	interface Props {
		url: URL;
		name?: string;
	}

	let { url, name = "" }: Props = $props();

	let open = $state(false);
	let isMobile = $state(false);
	let headerElement: HTMLElement | undefined = $state();

	function toggleMobileHeader() {
		if (isMobile && open) open = !open
	}

	function updateBodyClass() {
        if (open) {
            document?.body?.classList?.add('menu-open');
        } else {
            document?.body?.classList?.remove('menu-open');
        }
    }

	$effect(() => {
		if (typeof window !== 'undefined') {
			updateBodyClass();
		}
	});

	function checkIsMobile() {
        isMobile = window.innerWidth <= 768;
    }

	function handleOutsideClick(event: MouseEvent) {
		if (headerElement && !headerElement.contains((event.target as HTMLElement))) {
			open = false;
			updateBodyClass();
		}
	}

	onMount(() => {
		if (typeof window !== 'undefined') {
			window.addEventListener('resize', checkIsMobile);
			document?.addEventListener('click', handleOutsideClick);
			checkIsMobile();
		}
    });

	onDestroy(() => {
		if (typeof window !== 'undefined') {
			window.removeEventListener('resize', checkIsMobile);
			document?.removeEventListener('click', handleOutsideClick);
			document?.body?.classList?.remove('menu-open');
		}
	});

	let previousCount: number = $derived(cart.current.products.length || 0);
	let animate: boolean = $state(false);

	$effect(() => {
		if (previousCount !== 0) {
			animate = false;
			requestAnimationFrame(() => {
				animate = true;
			});
		}
		previousCount = cart.current.products.length || 0;
	});
</script>

{#snippet header()}
	<div class="header-left">
		{#if isMobile}
			<Hamburger bind:open={open} />
		{/if}
	</div>
	<div class="header-center">
		<a href="/" data-sveltekit-preload-data class="header-text" style:font-size={isMobile ? "xx-large" : "xxx-large"} onclick={toggleMobileHeader}>{name}</a>
		<nav class={isMobile ? `mobile-menu ${open ? 'open' : ''}` : ''}>
			<a href="/" data-sveltekit-preload-data class:active={url.pathname === '/'} onclick={toggleMobileHeader}>Home</a>
			<a href="/products" data-sveltekit-preload-data class:active={url.pathname.startsWith('/products')} onclick={toggleMobileHeader}>Browse</a>
			<a href="/about" data-sveltekit-preload-data class:active={url.pathname === '/about'} onclick={toggleMobileHeader}>About</a>
			<a href="/contact" class:active={url.pathname === '/contact'} onclick={toggleMobileHeader}>Contact</a>
		</nav>
	</div>
	<div class="header-right">
		<!-- todo: don't show cart if no payment processor is found -->
		<a 
			href="/cart" 
			class:active={url.pathname === '/cart'} 
			style:position="relative"
			onclick={toggleMobileHeader}
		>
			<Icon icon="material-symbols:shopping-cart-rounded" width={32} height={32} />
			{#if cart.current.products.length > 0}
				<span class="cart-badge {animate ? 'bounce' : ''}">{cart.current.products.length}</span>
				
			{/if}
		</a>
	</div>
{/snippet}

<svelte:head>
	<!-- todo: allow custom font/header image -->
	<link href="https://fonts.googleapis.com/css2?family=Dancing+Script:wght@400..700&display=swap" rel="stylesheet">
</svelte:head>

<Header open={open}>
	{#if isMobile}
		<div class="header mobile" class:open bind:this={headerElement}>
			{@render header()}
		</div>
	{:else}
		<div class="header desktop">
			{@render header()}
		</div>
	{/if}
</Header>

<style>
    .header {
		background-color: #f8f8f8;
		border-bottom: 1px solid #e7e7e7;
		display: grid;
		grid-template-columns: 1fr auto 1fr;
		align-items: center;
		padding: 0 1rem;
		transition: border-bottom 0.3s linear;
	}

	.header.open {
		border-bottom: 1px solid #f8f8f8;
	}

	.mobile {
		min-height: 58px;
	}

	.desktop {
		min-height: 150px;
		padding: 1rem;
	}

	nav a {
		position: relative;
		text-transform: uppercase;
		margin: 0 0.5rem;
		color: rgba(0, 0, 0, 0.55);
		font-size: 16px;
		width: fit-content;
		transition:
			color 0.15s ease-in-out,
			background-color 0.15s ease-in-out,
			border-color 0.15s ease-in-out;
	}

	nav a.active {
		font-weight: bold;
	}

	nav a.active::after {
		content: '';
		position: absolute;
		left: 0;
		bottom: 0;
		width: 100%;
		height: 2px;
		background: currentColor;
		view-transition-name: active-page;
	}

	a {
		text-decoration: none;
	}

	.header-left {
		display: flex;
		justify-content: flex-start;
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
		height: 32px;
		width: 32px;
	}

	.header-text {
		font-family: 'Dancing Script', cursive;
		font-weight: 700;
		font-style: normal;
		color: #62b2b2;
		text-align: center;
		text-transform: none;
		margin: 0;
	}

	nav.mobile-menu {
		display: flex;
		flex-direction: column;
		overflow: hidden;
		max-height: 0;
		transition: max-height 377ms ease-in-out 199ms;
		background-color: #f8f8f8;
		border-bottom: 1px solid #e7e7e7;
		position: absolute;
		top: 100%;
		left: 0;
		width: 100%;
		box-shadow: 0 5px 5px -5px rgba(0, 0, 0, 0.15);
		padding: 0 1rem;
	}

	nav.mobile-menu a {
		margin: 0.5rem 0;
	}

	/* When the menu is open */
	nav.mobile-menu.open {
		max-height: 500px; /* large enough to fit all items */
		opacity: 1;
		transition: max-height 377ms ease-in-out;
	}

	.cart-badge {
		position: absolute;
		bottom: 0;
		left: 0;
		background: red;
		color: white;
		font-size: 0.75rem;
		font-weight: bold;
		border-radius: 9999px;
		padding: 0.15em 0.5em;
		line-height: normal;
		transform: translate(-34%, 34%);
		pointer-events: none;
		transition: transform 0.2s ease;
	}

	.bounce {
		animation: bounce 0.4s ease;
	}

	@keyframes bounce {
		0%   { transform: translate(-34%, 34%) scale(1); }
		25%  { transform: translate(-34%, 34%) scale(1.2); }
		50%  { transform: translate(-34%, 34%) scale(0.95); }
		75%  { transform: translate(-34%, 34%) scale(1.05); }
		100% { transform: translate(-34%, 34%) scale(1); }
	}
</style>