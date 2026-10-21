<script lang="ts">
	import type { ProductOut } from '$lib/interfaces/ProductOut';
	import type { Location } from '$lib/interfaces/Location';
	import type { PaymentProcessor } from '$lib/enums/paymentProcessor';
	import Tooltip from '$lib/components/shared/Tooltip.svelte';
	import ProductImages from '$lib/components/ProductImages.svelte';
	import Button from '$lib/components/shared/Button.svelte';
	import { ButtonStyle } from '$lib/enums/buttonStyle';
	import { cart } from '$lib/state/cart.svelte';
	import { currencyFormatter } from '$lib/utils/formatters';
	import { goto } from '$app/navigation';

	let { product, location, paymentProcessor, url }: { product: ProductOut; location: Promise<Location>; paymentProcessor: PaymentProcessor | null; url: URL } = $props();
	const returnsTooltipContent = 'You have 14 days from item delivery to ship this item back. Buyer is responsible for return shipping costs. If the item is not returned in its original condition, the buyer is responsible for any loss in value.';

	function handleInquire() {
		const searchParams = new URLSearchParams({ message: `Hello, I'm interested in purchasing ${product.title}.`, productId: String(product.id) });
		const imageIndex = url.hash.slice(1);
		if (/^\d+$/.test(imageIndex) && Number(imageIndex) < (product.images?.length ?? 0)) searchParams.set('imageIndex', imageIndex);
		void goto(`/contact?${searchParams}`);
	}
</script>

<div class="product-detail">
	<div class="gallery"><ProductImages {product} {url} /></div>
	<div class="details">
		<div><h1>{product.title}</h1><div class="description">{product.description}</div></div>
		<div><div class="price">{currencyFormatter.format(product.price as number)}</div><div class="shipping">+ <i>free shipping</i></div></div>
		{#if product.sold}
			<Button disabled style={ButtonStyle.Neutral}>Sold</Button>
		{:else if paymentProcessor === null}
			<Button onclick={handleInquire} style={ButtonStyle.Info}>Inquire about this work</Button>
		{:else if !cart.current.products.some((item) => item.id === product.id)}
			<Button onclick={() => cart.current.products.push(product)} style={ButtonStyle.Info}>Add to Cart</Button>
		{:else}
			<Button onclick={() => goto('/cart')} style={ButtonStyle.Neutral}>View in Cart</Button>
		{/if}
		{#await location}
			<div>Ships from: <span class="loader" aria-label="Loading shipping location"></span></div>
		{:then value}
			<div>Ships from: <b>{value.city ? `${value.city}, ${value.state}` : value.state}</b></div>
		{/await}
		<Tooltip content={returnsTooltipContent} position="bottom"><div>Returns &amp; exchanges accepted within 14 days</div></Tooltip>
	</div>
</div>

<style>
	.product-detail { display: flex; inline-size: 100%; }
	.gallery { flex: 5; min-inline-size: 0; }
	.details { flex: 3; min-inline-size: 0; padding: 1rem; display: flex; flex-direction: column; gap: 1rem; align-items: center; }
	h1 { font-size: xx-large; font-weight: bolder; text-align: center; margin-block: 0; }
	.description { text-align: justify; hyphens: auto; white-space: pre-line; }
	.price { font-size: x-large; font-weight: bold; text-align: center; }
	.shipping { text-align: center; }
	.loader { display: inline-block; inline-size: 21px; aspect-ratio: 4; background: radial-gradient(circle closest-side, var(--ink) 90%, transparent) 0 / calc(100% / 3) 100% space; clip-path: inset(0 100% 0 0); }
	@media (prefers-reduced-motion: no-preference) { .loader { animation: loading 1s steps(4) infinite; } }
	@keyframes loading { to { clip-path: inset(0 -34% 0 0); } }
	@media (width <= 1144px) { .product-detail { flex-direction: column; } }
</style>
