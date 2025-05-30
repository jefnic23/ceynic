<script lang="ts">
	import type { PageData } from './$types';
	import Tooltip from '$lib/components/shared/Tooltip.svelte';
	import Skeleton from '$lib/components/shared/Skeleton.svelte';
	import { page } from '$app/state';
	import ProductImages from '$lib/components/ProductImages.svelte';
	import Button from '$lib/components/shared/Button.svelte';
	import type { ProductOut } from '$lib/interfaces/ProductOut';
	import { ButtonStyle } from '$lib/enums/buttonStyle';
	import { cart } from '$lib/state/cart.svelte';
	import Icon from '@iconify/svelte';
	import { currencyFormatter } from '$lib/utils/formatters';
	import { goto } from '$app/navigation';

	interface Props {
		data: PageData;
	}

	let { data }: Props = $props();

    const returnsTooltipContent: string = `
        You have 14 days from item delivery to ship this item back. Buyer is responsible for
        return shipping costs. If the item is not returned in its original condition, the buyer
        is responsible for any loss in value.
    `;

	function handleAddToCart(product: ProductOut) {
		cart.current.products.push(product);
		// todo: add toast message with redirect to cart
		// console.log($state.snapshot(cart));
	}

	function handleViewInCart() {
		goto('/cart');
	}
</script>

<div class="wrapper">
	{#await data.product}
		<div class="breadcrumb">
			<a href="/products">Browse</a>
			<Icon icon="material-symbols:arrow-forward-ios-rounded" width={16} height={16} />
			...
		</div>
		<div class="product">
			<div class="image">
				<Skeleton />
			</div>
			<div class="details">
				<Skeleton />
			</div>
		</div>
	{:then product}
		<div class="breadcrumb">
			<a href="/products">Browse</a>
			<Icon icon="material-symbols:arrow-forward-ios-rounded" width={16} height={16} />
			{product.title}
		</div>
		<div class="product">
			<ProductImages product={product} url={page.url} />
			<div class="details">
				<div>
					<div class="title">{product.title}</div>
					<div class="description">{product.description}</div>
				</div>
				<div>
					<div class="price">{currencyFormatter.format(product.price as number)}</div>
					<div class="shipping">+ <i>free shipping</i></div>
				</div>
				{#if cart.current.products.find(p => p.id === product.id) === undefined}
					<Button onclick={() => handleAddToCart(product)} style={ButtonStyle.Info}>
						Add to Cart
					</Button>
				{:else}
					<Button onclick={handleViewInCart} style={ButtonStyle.Neutral}>
						View in Cart
					</Button>
				{/if}
				{#await data.location}
					<div>Ships from: <div class="loader"></div></div>
				{:then location}
					<div>
						Ships from: <b>{location.city ? `${location.city}, ${location.state}` : `${location.state}`}</b>
					</div>
				{/await}
				<Tooltip content={returnsTooltipContent.trim()} position={'bottom'}>
					<div>Returns & exchanges accepted within 14 days</div>
				</Tooltip>
			</div>
		</div>
	{/await}
</div>



<style>
	.wrapper {
		display: flex;
		flex-direction: column;
		align-items: flex-start;
		width: 100%;
		column-gap: 1rem;
		max-width: 1144px;
	}

	.breadcrumb {
		display: flex;
		flex-direction: row;
		align-items: center;
		column-gap: 5px;
		font-size: 0.9rem;
		padding: 0 1rem;
		color: #666;
	}

	.breadcrumb a {
		text-decoration: none;
		color: #0070f3; /* example link color */
	}

	.product {
		display: flex;
		flex-direction: row;
		width: 100%;
	}

	.details {
		flex: 3;
		padding: 1rem;
		display: flex;
		flex-direction: column;
		row-gap: 1rem;
		align-items: center;
	}

	.title {
		font-size: xx-large;
		font-weight: bolder;
		text-align: center;
	}

	.description {
		text-align: justify;
		hyphens: auto;
	}

	.price {
		font-size: x-large;
		font-weight: bold;
		text-align: center;
	}

    .shipping {
        text-align: center;
    }

    .loader {
        display: inline-block;
        width: 21px;
        aspect-ratio: 4;
        background: radial-gradient(circle closest-side,#000 90%,#0000) 0/calc(100%/3) 100% space;
        clip-path: inset(0 100% 0 0);
        animation: l1 1s steps(4) infinite;
    }

    @keyframes l1 {to{clip-path: inset(0 -34% 0 0)}}

	@media only screen and (max-width: 1144px) {
		.wrapper {
			align-items: center;
		}

		.product {
			flex-direction: column;
		}
	}
</style>
