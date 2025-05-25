<script lang="ts">
    import Card from "$lib/components/shared/Card.svelte";
	import type { ProductsOut } from "$lib/interfaces/ProductsOut";

    interface Props {
        product: ProductsOut;
    }

    let { product }: Props = $props();
</script>

<Card>
    <div class="product">
        <a href="/products/{product.id}" data-sveltekit-preload-data>
            <img class="image" src={product.imageUrl} alt={product.title} data-pin-nopin="true" />
            <div class="title">{product.title}</div>
            <div class="price">${product.price}</div>
        </a>
    </div>
</Card>

<style>
    a {
        text-decoration: none;
        color: initial;
    }

    .product{
        width: min-content;
        margin: auto;
    }

    .image {
		width: 256px;
		height: 256px;
		object-fit: cover;
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
		.image {
			width: 225px;
            height: 225px;
		}
	}
</style>