<script lang="ts">
    import Card from "$lib/components/shared/Card.svelte";
	import type { ProductsOut } from "$lib/interfaces/product";

    export let product: ProductsOut
</script>

<Card>
    <div class="product">
        <a href="/products/{product.id}" data-sveltekit-preload-data>
            <img class="image" src={product.imageUrl} alt={product.title} />
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
    }

    .image {
		width: 225px;
		height: 225px;
		object-fit: cover;
	}

    .title {
		width: 100%;
		max-width: 225px;
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

    @media only screen and (max-width: 590px) and (min-width: 491px) {
        .image {
            width: 175px;
            height: 175px;
        }
	}
</style>