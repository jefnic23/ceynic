<script lang="ts">
	import { type PageData } from './$types';
	import { goto } from '$app/navigation';
	import PayPal from '$lib/components/PayPal.svelte';
	import { PaymentProcessor } from '$lib/enums/paymentProcessor';
	import { usePayPal } from '$lib/state/paypal';
	import Skeleton from '$lib/components/shared/Skeleton.svelte';
	import { cart } from '$lib/state/cart.svelte';
	import PageContainer from '$lib/components/shared/PageContainer.svelte';
	import CartItems from '$lib/components/ecomm/CartItems.svelte';
	import CartSummary from '$lib/components/ecomm/CartSummary.svelte';
	import CartLayout from '$lib/components/ecomm/CartLayout.svelte';
	import Button from '$lib/components/shared/Button.svelte';
	import { ButtonStyle } from '$lib/enums/buttonStyle';
	import type { ProductOut } from '$lib/interfaces/ProductOut';
	import { PUBLIC_API_URL } from '$env/static/public';
	import { onMount } from 'svelte';

    interface Props {
		data: PageData;
	}

	let { data }: Props = $props();
	let unavailableIds: number[] = $state([]);
	let checkingAvailability = $state(true);
	let hasUnavailableItems = $derived(cart.current.products.some(product => unavailableIds.includes(product.id)));

	async function refreshAvailability() {
		const ids = [...new Set(cart.current.products.map(product => product.id))];
		const unavailable = await Promise.all(ids.map(async id => {
			try {
				const response = await fetch(`${PUBLIC_API_URL}/products/${id}`);
				if (!response.ok) return id;
				const product: ProductOut = await response.json();
				return product.sold ? id : null;
			} catch {
				return id;
			}
		}));
		unavailableIds = unavailable.filter((id): id is number => id !== null);
		checkingAvailability = false;
	}

	onMount(() => { void refreshAvailability(); });

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

<PageContainer max="1400px">
    {#if cart.current.products.length === 0}
        <p>Cart is empty.</p>
    {:else}
        <CartLayout>
            {#snippet items()}
				<CartItems products={cart.current.products} {unavailableIds} remove={handleRemove} />
            {/snippet}
            {#snippet summary()}
                    <CartSummary count={cart.current.products.length} subtotal={subtotal()}>
							{#if hasUnavailableItems}
								<p role="alert">Remove sold or unavailable items before checking out.</p>
							{:else if checkingAvailability}
								<Skeleton />
							{:else if data.paymentProcessor === PaymentProcessor.PAYPAL}
								{#if paypal.error}
									<p role="alert">PayPal checkout is unavailable right now.</p>
								{:else if paypal.sdk}
									<PayPal paypal={paypal.sdk} productIds={cart.current.products.map(p => p.id) || []} confirmOrder={confirmOrder} onConflict={refreshAvailability} />
								{:else}
									<Skeleton />
								{/if}
							{/if}
                    </CartSummary>
                <div class="form-actions">
                    <Button 
                        onclick={() => cart.current.products = []}
                        style={ButtonStyle.Neutral}
                    >
                        Empty Cart
                    </Button>
                </div>
            {/snippet}
        </CartLayout>
    {/if}
</PageContainer>

