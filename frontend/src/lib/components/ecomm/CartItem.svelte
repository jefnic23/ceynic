<script lang="ts">
	import type { ProductOut } from '$lib/interfaces/ProductOut';
	import ProductImage from '$lib/components/ProductImage.svelte';
	import Button from '$lib/components/shared/Button.svelte';
	import { ButtonStyle } from '$lib/enums/buttonStyle';
	import { currencyFormatter } from '$lib/utils/formatters';

	let { product, unavailable, remove }: { product: ProductOut; unavailable: boolean; remove: (product: ProductOut) => void } = $props();
</script>

<div class="cart-item">
	<ProductImage url={product.images?.[0]?.url} alt={product.title} width={128} height={128} data-pin-nopin="true" />
	<div class="content">
		<div>
			<h3><a href="/products/{product.id}">{product.title}</a></h3>
			<div class="description">{product.description}</div>
			<div class="price">{currencyFormatter.format(product.price as number)}</div>
			{#if unavailable}<div role="status">Sold or unavailable — remove this item to continue.</div>{/if}
		</div>
		<div class="remove"><Button onclick={() => remove(product)} style={ButtonStyle.Neutral}>Remove</Button></div>
	</div>
</div>

<style>
	.cart-item { display: flex; flex-wrap: wrap; gap: 1rem; }
	.cart-item :global(img) { flex: none; }
	.content { display: flex; flex: 1 1 16rem; flex-direction: column; min-inline-size: 0; }
	h3 { margin-block: 0; font-size: 1.17em; }
	a { text-decoration: none; color: var(--ink); }
	a:active { color: var(--link); }
	@media (hover: hover) and (pointer: fine) { a:hover { text-decoration: underline; } }
	.description { max-inline-size: 600px; overflow: clip; text-overflow: ellipsis; white-space: nowrap; font-style: italic; padding-inline-end: 3px; color: var(--ink-muted); }
	.remove { display: flex; justify-content: flex-end; margin-block-start: 1rem; }
</style>
