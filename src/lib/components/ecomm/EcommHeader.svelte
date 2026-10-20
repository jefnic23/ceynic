<script lang="ts">
	import Header from "$lib/components/shared/Header.svelte";
	import { onMount } from "svelte";
	import Hamburger from "../Hamburger.svelte";
	import Icon from "@iconify/svelte";
	import { cart } from "$lib/state/cart.svelte";
	import type { PaymentProcessor } from '$lib/enums/paymentProcessor';

	interface Props {
		url: URL;
		name?: string;
		paymentProcessor: PaymentProcessor | null;
	}

	let { url, name = "", paymentProcessor }: Props = $props();

	let open = $state(false);
	let headerElement: HTMLElement | undefined = $state();

	function toggleMobileHeader() {
		open = false;
	}

	function handleOutsideClick(event: MouseEvent) {
		if (headerElement && !headerElement.contains((event.target as HTMLElement))) {
			open = false;
		}
	}

	onMount(() => {
		document.addEventListener('click', handleOutsideClick);
		return () => document.removeEventListener('click', handleOutsideClick);
	});

	let previousCount: number = $state(cart.current.products.length || 0);
	let displayCount: number = $state(cart.current.products.length || 0);
	let animateBounce: boolean = $state(false);
	let animateShrink: boolean = $state(false);
	let showBadge: boolean = $state(false);

	$effect(() => {
		if (cart.current.products.length > 0) {
			displayCount = cart.current.products.length;
			if (!showBadge) showBadge = true;
			if (cart.current.products.length !== previousCount) {
				animateBounce = false;
				requestAnimationFrame(() => {
					animateBounce = true;
				});
			}
		} else if (previousCount > 0 && cart.current.products.length === 0) {
			// Trigger shrink, then hide
			animateShrink = true;
			setTimeout(() => {
				showBadge = false;
				animateShrink = false;
			}, 200); // match shrink duration
		}
		previousCount = cart.current.products.length || 0;
	});
</script>

{#snippet header()}
	<div class="header-left">
		<div class="mobile-toggle"><Hamburger bind:open={open} /></div>
	</div>
	<div class="header-center">
		<a href="/" data-sveltekit-preload-data class="header-text" onclick={toggleMobileHeader}>{name}</a>
		<nav class="mobile-menu" class:open>
			<a href="/" data-sveltekit-preload-data class:active={url.pathname === '/'} onclick={toggleMobileHeader}>Home</a>
			<a href="/products" data-sveltekit-preload-data class:active={url.pathname.startsWith('/products')} onclick={toggleMobileHeader}>Browse</a>
			<a href="/about" data-sveltekit-preload-data class:active={url.pathname === '/about'} onclick={toggleMobileHeader}>About</a>
			<a href="/contact" class:active={url.pathname === '/contact'} onclick={toggleMobileHeader}>Contact</a>
		</nav>
	</div>
	<div class="header-right">
		{#if paymentProcessor !== null}
			<a 
				href="/cart" 
				data-sveltekit-preload-data
				class:active={url.pathname === '/cart'} 
				onclick={toggleMobileHeader}
			>
				<Icon icon="material-symbols:shopping-cart-rounded" width={32} height={32} />
				{#if showBadge}
					<span class="cart-badge {animateBounce ? 'bounce' : ''} {animateShrink ? 'shrink' : ''}">
						{displayCount}
					</span>
				{/if}
			</a>
		{/if}
	</div>
{/snippet}

<svelte:head>
	<!-- todo: allow custom font/header image -->
	<link href="https://fonts.googleapis.com/css2?family=Dancing+Script:wght@400..700&display=swap" rel="stylesheet">
</svelte:head>

<Header open={open}>
	<div class="header" class:open bind:this={headerElement}>
		{@render header()}
	</div>
</Header>

<style>
    .header {
		background-color: var(--surface-muted);
		border-block-end: 1px solid var(--border);
		display: grid;
		grid-template-columns: 1fr auto 1fr;
		align-items: center;
		padding: 1rem;
		min-block-size: 150px;
		transition: border-block-end-color 0.3s linear;
	}

	.header.open {
		border-block-end-color: var(--surface-muted);
	}

	nav a {
		position: relative;
		text-transform: uppercase;
		margin-inline: 0.5rem;
		color: color-mix(in oklch, var(--ink) 55%, transparent);
		font-size: 16px;
		font-weight: 400;
		inline-size: fit-content;
		transition:
			color 0.15s ease-in-out,
			background-color 0.15s ease-in-out,
			border-color 0.15s ease-in-out;
	}

	nav a.active {
		color: color-mix(in oklch, var(--ink) 85%, transparent);
	}

	nav a.active::after {
		content: '';
		position: absolute;
		inset-inline-start: 0;
		inset-block-end: 0;
		inline-size: 100%;
		block-size: 2px;
		background: currentColor;
		view-transition-name: active-page;
	}

	a {
		text-decoration: none;
	}
	a:active { color: var(--ink); }

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
		color: color-mix(in oklch, var(--ink) 55%, transparent);
		block-size: 32px;
		inline-size: 32px;
		position: relative;
	}

	.header-text {
		font-family: 'Dancing Script', cursive;
		font-weight: 700;
		font-style: normal;
		color: oklch(0.73 0.08 193);
		text-align: center;
		text-transform: none;
		margin: 0;
		font-size: xxx-large;
	}

	nav.mobile-menu {
		display: flex;
	}
	.mobile-toggle { display: none; }

	.cart-badge {
		position: absolute;
		inset-block-end: 0;
		inset-inline-start: 0;
		background: var(--danger);
		color: var(--surface);
		font-size: 0.75rem;
		font-weight: bold;
		border-radius: 9999px;
		padding: 0.15em 0.5em;
		line-height: normal;
		transform: translate(-34%, 34%);
		pointer-events: none;
	}

	@media (width <= 768px) {
		.header { min-block-size: 58px; padding-block: 0; padding-inline: 1rem; }
		.mobile-toggle { display: flex; }
		.header-text { font-size: xx-large; }
		nav.mobile-menu {
			position: absolute;
			inset-block-start: 100%;
			inset-inline: 0;
			display: flex;
			flex-direction: column;
			background: var(--surface-muted);
			border-block-end: 1px solid var(--border);
			box-shadow: 0 5px 5px -5px color-mix(in oklch, var(--ink) 15%, transparent);
			padding-inline: 1rem;
			clip-path: inset(0 -3rem 100%);
			visibility: hidden;
		}
		nav.mobile-menu.open { clip-path: inset(0 -3rem -3rem); visibility: visible; }
		nav.mobile-menu a { margin-block: 0.5rem; }
	}
	@media (width <= 768px) and (prefers-reduced-motion: no-preference) {
		nav.mobile-menu { transition: clip-path 250ms var(--ease-out), visibility 250ms; }
	}
	@media (prefers-reduced-motion: no-preference) {
		.cart-badge { transition: transform 0.2s var(--ease-out); }
		.bounce { animation: bounce 0.4s var(--ease-out); }
		.shrink { animation: shrink 0.2s var(--ease-out) forwards; }
	}

	@keyframes bounce {
		0%   { transform: translate(-34%, 34%) scale(1); }
		25%  { transform: translate(-34%, 34%) scale(1.2); }
		50%  { transform: translate(-34%, 34%) scale(0.95); }
		75%  { transform: translate(-34%, 34%) scale(1.05); }
		100% { transform: translate(-34%, 34%) scale(1); }
	}

	@keyframes shrink {
		from { transform: translate(-34%, 34%) scale(1); opacity: 1; }
		to   { transform: translate(-34%, 34%) scale(0); opacity: 0; }
	}
</style>
