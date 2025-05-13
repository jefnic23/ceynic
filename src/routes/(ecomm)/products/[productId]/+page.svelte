<script lang="ts">
	import type { PageData } from './$types';
	import PayPal from '$lib/components/PayPal.svelte';
	import Tooltip from '$lib/components/shared/Tooltip.svelte';
	import Skeleton from '$lib/components/shared/Skeleton.svelte';
	import { PaymentProcessor } from '$lib/enums/paymentProcessor';
	import Modal from '$lib/components/shared/Modal.svelte';
	import ArrowRight from '$lib/icons/ArrowRight.svelte';

	// todo: Stripe/Amazon Pay needs to be added here as well

	interface Props {
		data: PageData;
	}

	let { data }: Props = $props();

    const returnsTooltipContent: string = `
        You have 14 days from item delivery to ship this item back. Buyer is responsible for
        return shipping costs. If the item is not returned in its original condition, the buyer
        is responsible for any loss in value.
    `;

	let showModal: boolean = $state(false);
	let orderId: string = $state("");

	function confirmOrder(e: CustomEvent) {
		orderId = e.detail;
		showModal = !showModal;
	}

	// todo: add callback to payment processor 
	// todo: show modal payment confirmation
</script>

<div class="wrapper">
	{#await data.product}
		<div class="breadcrumb">
			<a href="/products">Browse</a>
			<ArrowRight size={16} />
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
			<ArrowRight size={16} />
			{product.title}
		</div>
		<div class="product">
			<div class="image">
				<img src={product.images[0]} alt={product.title} />
			</div>
			<div class="details">
				<div>
					<div class="title">{product.title}</div>
					<div class="description">{product.description}</div>
				</div>
				<div>
					<div class="price">${product.price}</div>
					<div class="shipping">+ <i>free shipping</i></div>
				</div>
				{#await data.paymentProcessor}
					<div>loading</div>
				{:then paymentProcessor} 
					{#if paymentProcessor === PaymentProcessor.PAYPAL}
						<PayPal productIds={[product.id]} on:confirm_order={confirmOrder} />
					{/if}
				{/await}
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
					<div>Returns & exchanges accepted within 14 days</div>
				</Tooltip>
			</div>
		</div>
	{/await}
</div>

{#if showModal}
	<Modal bind:showModal title={"Order Confirmed!"} type={"success"}>
		<div>
			<div>Your order has been confirmed.</div>
			<div>Order ID: {orderId}</div>
		</div>
	</Modal>
{/if}

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
	}

	.image {
		flex: 5;
		padding: 1rem;
	}

	.image img {
		width: 100%;
	}

	.details {
		flex: 3;
		padding: 1rem;
		display: flex;
		flex-direction: column;
		row-gap: 1rem;
	}

	.title {
		font-size: xx-large;
		font-weight: bolder;
		text-align: center;
	}

	.description {
		text-align: justify;
		text-align-last: center;
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

	@media only screen and (max-width: 900px) {
		.wrapper {
			align-items: center;
		}

		.product {
			flex-direction: column;
		}
	}
</style>
