<script lang="ts">
    import { PUBLIC_PAYPAL_CLIENT_ID } from '$env/static/public';
	import { loadScript, type PayPalNamespace } from '@paypal/paypal-js';
	import { onMount } from 'svelte';
	import { type PageData } from './$types';
	import PayPal from '$lib/components/PayPal.svelte';
	import { PaymentProcessor } from '$lib/enums/paymentProcessor';
	import Modal from '$lib/components/shared/Modal.svelte';
	import Skeleton from '$lib/components/shared/Skeleton.svelte';
	import { cart } from '$lib/state/cart.svelte';
	import { currencyFormatter } from '$lib/utils/formatters';
	import { CldImage } from 'svelte-cloudinary';
	import Card from '$lib/components/shared/Card.svelte';
	import Button from '$lib/components/shared/Button.svelte';
	import { ButtonStyle } from '$lib/enums/buttonStyle';
	import type { ProductOut } from '$lib/interfaces/ProductOut';

    interface Props {
		data: PageData;
	}

	let { data }: Props = $props();

    let subtotal: () => number = $derived(() => {
        const prices = cart.current.products.map(p => parseFloat(p.price as string));
		return prices.reduce((a, b) => a + b, 0.0)
    });
    let showModal: boolean = $state(false);
	let orderId: string = $state("");

	function confirmOrder(e: CustomEvent) {
		orderId = e.detail;
		showModal = !showModal;
	}

    // todo: Stripe/Amazon Pay needs to be added here as well
    let paypal: PayPalNamespace | null = $state(null);

	onMount(async () => {
		try {
			paypal = await loadScript({
				clientId: PUBLIC_PAYPAL_CLIENT_ID,
				currency: 'USD',
				dataPageType: 'checkout',
				intent: 'authorize',
				// debug: true
				// todo: add merchantId
			});
		} catch (error) {
			// todo: log error and show something in the UI
		}
	});

    function handleRemove(product: ProductOut) {
        cart.current.products = cart.current.products.filter(p => p.id !== product.id);
    }
</script>

<div class="container column gap">
    {#if cart.current.products.length === 0}
        <div class="row">Cart is empty.</div>
    {:else}
        <div class="cart gap">
            <div>
                <Card>
                    <div class="column gap">
                        {#each cart.current.products as product}
                            <div class="product" style:row-gap="1rem" style:column-gap="1rem">
                                <CldImage
                                    src={product.images?.[0]?.publicId || ""}
                                    alt={product.title}
                                    width={128}
                                    height={128}
                                    data-pin-nopin="true"
                                />
                                <div class="column">
                                    <div>
                                        <div class="title">
                                            <a href="/products/{product.id}">
                                                <h3 style:margin="0">{product.title}</h3>
                                            </a>
                                        </div>
                                        <div class="description">{product.description}</div>
                                        <div>{currencyFormatter.format(product.price as number)}</div>
                                    </div>
                                    <div class="remove">
                                        <Button onclick={() => handleRemove(product)} style={ButtonStyle.Neutral}>Remove</Button>
                                    </div>
                                </div>
                            </div>
                        {/each}
                    </div>
                </Card>
            </div>
            <div class="summary gap end">
                <div>
                    <Card>
                        <div class="column center" style:row-gap="1rem">
                            <h2 style:margin="0">Order Summary</h2>
                            <div class="row apart">
                                <div>
                                    Subtotal ({cart.current.products.length}): 
                                </div>
                                <div>
                                    {currencyFormatter.format(subtotal())}
                                </div>
                            </div>
                            {#await data.paymentProcessor}
                                <Skeleton />
                            {:then paymentProcessor} 
                                {#if paymentProcessor === PaymentProcessor.PAYPAL}
                                    <PayPal paypal={paypal} productIds={cart.current.products.map(p => p.id) || []} confirmOrder={confirmOrder} />
                                {/if}
                            {/await}
                        </div>
                    </Card> 
                </div>
                <div class="row" style:justify-content="flex-end">
                    <Button 
                        onclick={() => cart.current.products = []}
                        style={ButtonStyle.Neutral}
                    >
                        Empty Cart
                    </Button>
                </div>
            </div>
        </div>
    {/if}
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
    .container {
        width: 100%;
        max-width: 1400px;
        align-items: center;
    }

    .column {
        display: flex;
        flex-direction: column;
        width: 100%;
    }

    .row {
        display: flex;
        flex-direction: row;
        justify-content: center;
        width: 100%;
    }

    .gap {
        column-gap: 2rem;
        row-gap: 2rem;
    }

    .center {
        align-items: center;
    }

    .end {
        align-items: flex-end;
    }

    .apart {
        width: 100%;
        justify-content: space-between;
    }

    a {
        text-decoration: none;
        color: black;
    }

    .title {
        width: fit-content;
    }

    .title > a:hover {
        text-decoration: underline;
        cursor: pointer;
    }

    .cart {
        display: flex;
        flex-direction: row;
    }

    .product {
        display: flex;
        flex-direction: row;
    }

    .description {
        width: 100%;
        max-width: 600px;
        overflow: hidden;
        text-overflow: ellipsis;
        white-space: nowrap;
        font-style: italic;
        padding-right: 3px;
        color: rgb(112, 112, 112);
    }

    .remove {
        margin-top: 1rem;
        display: flex;
        justify-content: end;
    }

    .summary {
        display: flex;
        flex-direction: column;
    }

    @media only screen and (max-width: 992px) and (min-width: 769px) {
        .cart {
            flex-direction: column;
        }

        .product {
            flex-direction: column;
            align-items: center;
        }

        .summary {
            align-items: center;
        }
    }

    @media only screen and (max-width: 768px) and (min-width: 481px) {
        .cart {
            flex-direction: column;
        }

        .product {
            flex-direction: column;
            align-items: center;
        }

        .description {
            max-width: 360px;
        }

        .summary {
            align-items: center;
        }
    }

    @media only screen and (max-width: 480px) {
        .cart {
            flex-direction: column;
        }

        .product {
            flex-direction: column;
            align-items: center;
        }

        .description {
            max-width: 280px;
        }

        .summary {
            align-items: center;
        }
    }
</style>