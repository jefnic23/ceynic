<script lang="ts">
    import Card from "$lib/components/shared/Card.svelte";
	import ProductImage from '$lib/components/ProductImage.svelte';
	import type { ProductOut } from "$lib/interfaces/ProductOut";

    interface Props {
        product: ProductOut;
    }

    let { product }: Props = $props();

</script>

<Card>
    <div class="product">
        <a href="/products/{product.id}" data-sveltekit-preload-data>
            <ProductImage
				url={product.images?.[0]?.url}
                alt={product.title} 
                width={256}
                height={256}
                data-pin-nopin="true" 
            />
            <div class="title">{product.title}</div>
            <div class="price">${product.price}{#if product.sold}<span class="sold">Sold</span>{/if}</div>
        </a>
    </div>
</Card>

<style>
    a {
        display: grid;
        text-decoration: none;
		color: var(--ink);
    }
	a:active { opacity: 0.8; }

    .product{
        
		inline-size: clamp(14.0625rem, 12rem + 7vw, 16rem);
		max-inline-size: 100%;
		margin-inline: auto;
    }
	.product :global(img) { inline-size: 100%; aspect-ratio: 1; object-fit: cover; }

    .title {
		inline-size: 100%;
		overflow: clip;
		text-overflow: ellipsis;
		display: inline-block;
		white-space: nowrap;
		font-style: italic;
		color: var(--ink-muted);
	}

    .price {
        font-weight: 500;
    }

	.sold {
		color: var(--ink-muted);
		margin-inline-start: 5px;
	}
</style>
