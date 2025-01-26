<script lang="ts">
	import type { PageData } from './$types';
	import PayPal from '$lib/components/PayPal.svelte';
	import Tooltip from '$lib/components/Tooltip.svelte';

	export let data: PageData;

    const returnsTooltipContent = `
        You have 14 days from item delivery to ship this item back. Buyer is responsible for
        return shipping costs. If the item is not returned in its original condition, the buyer
        is responsible for any loss in value.
    `;
</script>

<div class="wrapper">
	{#await data.product}
		<p>Loading product...</p>
	{:then product}
		<div class="row">
			<div class="column flex-5 center">
				<img src={product.images[0]} alt={product.title} />
			</div>
			<div class="column flex-3 left">
				<div>
					<div class="title">{product.title}</div>
					<div class="description">{product.description}</div>
				</div>
				<div>
					<div class="price">${product.price}</div>
					<div class="shipping">+ <i>free shipping</i></div>
				</div>
				<PayPal productId={product.id} />
				<div>
					{#await data.location}
						<div>Ships from: <div class="loader"></div></div>
					{:then location}
						<div>
							Ships from: <b>{location.city ? `${location.city}, ${location.state}` : `${location.state}`}</b>
						</div>
					{/await}
				</div>
                <Tooltip content={returnsTooltipContent.trim()} position={'bottom'}>
                    <div class="returns">Returns & exchanges accepted within 14 days</div>
                </Tooltip>
			</div>
		</div>
	{/await}
</div>

<style>
	.wrapper {
		display: flex;
		flex-direction: column;
		align-items: center;
		width: 100%;
		padding: 1rem 0;
	}

	.row {
		display: flex;
		flex-direction: row;
		column-gap: 1rem;
	}

	.column {
		display: flex;
		flex-direction: column;
		align-items: left;
		row-gap: 1rem;
	}

    .left {
        align-items: left;
    }

    .center {
        align-items: center;
    }

	.flex-5 {
		flex: 5;
	}

	.flex-3 {
		flex: 3;
	}

	img {
		width: 89%;
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

    .returns {
        text-decoration: underline dashed;
        text-underline-position: under;
    }

    .returns:hover {
        cursor: help;
    }
</style>
