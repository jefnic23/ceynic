<script lang="ts">
	import { type PageData } from './$types';
	import { goto } from '$app/navigation';
	import PayPal from '$lib/components/PayPal.svelte';
	import { PaymentProcessor } from '$lib/enums/paymentProcessor';
	import { usePayPal } from '$lib/state/paypal';
	import Skeleton from '$lib/components/shared/Skeleton.svelte';
	import { cart } from '$lib/state/cart.svelte';
	import { currencyFormatter } from '$lib/utils/formatters';
	import ProductImage from '$lib/components/ProductImage.svelte';
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
	function confirmOrder(orderID: string) {
        cart.current.products = [];
		void goto(`/orders/${encodeURIComponent(orderID)}/confirmation`);
	}

	const paypal = usePayPal();

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
                                <ProductImage
									url={product.images?.[0]?.url}
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
							{#if data.paymentProcessor === PaymentProcessor.PAYPAL}
								{#if paypal.error}
									<p role="alert">PayPal checkout is unavailable right now.</p>
								{:else if paypal.sdk}
									<PayPal paypal={paypal.sdk} productIds={cart.current.products.map(p => p.id) || []} confirmOrder={confirmOrder} />
								{:else}
									<Skeleton />
								{/if}
							{/if}
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
