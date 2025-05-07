<script lang="ts">
	import Cart from "$lib/icons/Cart.svelte";
	import Header from "$lib/components/shared/Header.svelte";
	import { onDestroy, onMount } from "svelte";
	import Hamburger from "../Hamburger.svelte";
	import { slide } from "svelte/transition";

    export let url: URL;
    export let name: string = "";

	let open = false;
	let isMobile = false;
	let headerElement: HTMLElement;

	function updateBodyClass() {
        if (open) {
            document.body.classList.add('menu-open');
        } else {
            document.body.classList.remove('menu-open');
        }
    }

	$: if (typeof window !== 'undefined') {
        updateBodyClass();
    }

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
			document.addEventListener('click', handleOutsideClick);
			checkIsMobile();
		}
    });

	onDestroy(() => {
		if (typeof window !== 'undefined') {
			window.removeEventListener('resize', checkIsMobile);
			document.removeEventListener('click', handleOutsideClick);
			document.body.classList.remove('menu-open');
		}
	});
</script>

<Header open={open}>
	{#if isMobile}
		<div class="header mobile" class:open bind:this={headerElement}>
			<div class="header-left">
				<Hamburger bind:open={open} />
			</div>
			<div class="header-center">
				<a href="/" data-sveltekit-preload-data class="header-text" style:font-size={"x-large"}>{name}</a>
				<nav class={`mobile-menu ${open ? 'open' : ''}`}>
					<a href="/" data-sveltekit-preload-data class:active={url.pathname === '/'} on:click={() => open = !open}>Home</a>
					<a href="/products" data-sveltekit-preload-data class:active={url.pathname.startsWith('/products')} on:click={() => open = !open}>Browse</a>
					<a href="/about" data-sveltekit-preload-data class:active={url.pathname === '/about'} on:click={() => open = !open}>About</a>
					<a href="/contact" class:active={url.pathname === '/contact'} on:click={() => open = !open}>Contact</a>
				</nav>
			</div>
			<div class="header-right">
				<a href="/cart" class:active={url.pathname === '/cart'} on:click={() => open = !open}><Cart size={32} /></a>
			</div>
		</div>
	{:else}
		<div class="header desktop">
			<div class="header-left"></div>
			<div class="header-center">
				<a href="/" data-sveltekit-preload-data class="header-text" style:font-size={"xxx-large"}>{name}</a>
				<nav>
					<a href="/" data-sveltekit-preload-data class:active={url.pathname === '/'}>Home</a>
					<a href="/products" data-sveltekit-preload-data class:active={url.pathname.startsWith('/products')}>Browse</a>
					<a href="/about" data-sveltekit-preload-data class:active={url.pathname === '/about'}>About</a>
					<a href="/contact" class:active={url.pathname === '/contact'}>Contact</a>
				</nav>
			</div>
			<div class="header-right">
				<a href="/cart" class:active={url.pathname === '/cart'}><Cart size={32} /></a>
			</div>
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
		font-size: 13px;
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
		transition: max-height 377ms ease-in-out 210ms;
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
</style>