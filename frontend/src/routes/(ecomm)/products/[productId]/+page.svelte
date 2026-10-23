<script lang="ts">
	import type { PageData } from './$types';
	import { page } from '$app/state';
	import Icon from '@iconify/svelte';
	import Skeleton from '$lib/components/shared/Skeleton.svelte';
	import PageContainer from '$lib/components/shared/PageContainer.svelte';
	import ProductDetail from '$lib/components/ecomm/ProductDetail.svelte';

	let { data }: { data: PageData } = $props();
</script>

<PageContainer max="1144px">
	{#await data.product}
		<div class="breadcrumb"><a href="/products">Browse</a><Icon icon="material-symbols:arrow-forward-ios-rounded" width={16} height={16} />...</div>
		<Skeleton />
	{:then product}
		<div class="breadcrumb"><a href="/products">Browse</a><Icon icon="material-symbols:arrow-forward-ios-rounded" width={16} height={16} />{product.title}</div>
		<ProductDetail {product} url={page.url} location={data.location} paymentProcessor={data.paymentProcessor} pinterestEnabled={data.pinterestEnabled} />
	{/await}
</PageContainer>

<style>
	.breadcrumb { display: flex; align-items: center; gap: 5px; font-size: 0.9rem; padding-inline: 1rem; color: var(--ink-muted); }
	.breadcrumb a { text-decoration: none; color: var(--link); }
	.breadcrumb a:active { text-decoration: underline; }
	@media (hover: hover) and (pointer: fine) { .breadcrumb a:hover { text-decoration: underline; } }
</style>
