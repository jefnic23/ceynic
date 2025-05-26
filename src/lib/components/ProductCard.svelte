<script lang="ts">
    import Card from "$lib/components/shared/Card.svelte";
	import type { ProductImageOut, ProductOut } from "$lib/interfaces/ProductOut";
	import { onMount } from "svelte";
	import { CldImage } from "svelte-cloudinary";

    interface Props {
        product: ProductOut;
    }

    let { product }: Props = $props();

    let isMobile: boolean = $state(false)

    onMount(() => {
        isMobile = window.innerWidth <= 400;
    });
</script>

<Card>
    <div class="product">
        <a href="/products/{product.id}" data-sveltekit-preload-data>
            <CldImage 
                src={(product.images as ProductImageOut[])[0]?.publicId} 
                alt={product.title} 
                width={!isMobile ? 256 : 225}
                height={!isMobile ? 256 : 225}
                data-pin-nopin="true" 
            />
            <div class="title">{product.title}</div>
            <div class="price">${product.price}</div>
        </a>
    </div>
</Card>

<style>
    a {
        display: grid;
        text-decoration: none;
        color: initial;
    }

    .product{
        
        width: 100%;
        margin: auto;
    }

    .title {
		width: 100%;
		max-width: 256px;
		overflow: hidden;
		text-overflow: ellipsis;
		display: inline-block;
		white-space: nowrap;
		font-style: italic;
		color: rgb(112, 112, 112);
	}

    .price {
        font-weight: 500;
    }

    @media only screen and (max-width: 400px) {
		.title {
			max-width: 225px;
		}
	}
</style>