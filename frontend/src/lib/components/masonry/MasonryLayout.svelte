<script lang="ts">
	import Skeleton from '$lib/components/shared/Skeleton.svelte';
	import MasonryItem from '$lib/components/masonry/MasonryItem.svelte';
	import type { ProductOut } from '$lib/interfaces/ProductOut';
	import { onMount, tick } from 'svelte';

	interface Props {
		products?: ProductOut[];
	}

	let { products = [] }: Props = $props();
	let layout: HTMLDivElement;
	let columnCount = $state(3);
	let productColumns = $derived(
		Array.from({ length: columnCount }, (_, column) =>
			products.filter((_, index) => index % columnCount === column)
		)
	);
	const skeletonIndexes = Array.from({ length: 12 }, (_, index) => index);

	onMount(() => {
		if (products.length > 0) tick().then(() => window.PinUtils?.build());

		const observer = new ResizeObserver(([entry]) => {
			if (!entry) return;
			const gap = 13;
			const minColumnWidth = 384;
			columnCount = Math.min(3, Math.max(1, Math.floor((entry.contentRect.width + gap) / (minColumnWidth + gap))));
		});
		observer.observe(layout);
		return () => observer.disconnect();
	});

	let loadedImages = $state(new Set<number>());

	function handleImageLoad (id: number) {
		loadedImages.add(id);
		loadedImages = new Set(loadedImages);
	};

	function randomAspectRatio() {
		// Choose ratios between 3:4 (0.75) and 9:16 (0.5625)
		const min = 0.5625;
		const max = 0.75;
		const ratio = Math.random() * (max - min) + min;
		return ratio.toFixed(2);
	}
</script>

<div class="masonry-layout" bind:this={layout} style:--column-count={columnCount}>
	{#each productColumns as columnProducts, column}
		<div class="masonry-column">
			{#if products.length === 0}
				{#each skeletonIndexes.filter((index) => index % columnCount === column) as _}
					<div class="masonry-skeleton-item" style="aspect-ratio: 1 / {randomAspectRatio()};">
						<Skeleton />
					</div>
				{/each}
			{:else}
				{#each columnProducts as product (product.id)}
					<MasonryItem
						{product}
						loaded={loadedImages.has(product.id)}
						load={handleImageLoad}
					/>
				{/each}
			{/if}
		</div>
	{/each}
</div>

<style>
	.masonry-layout {
		display: grid;
		grid-template-columns: repeat(var(--column-count), minmax(0, 1fr));
		gap: 13px;
		inline-size: 100%;
	}

	.masonry-column {
		display: flex;
		flex-direction: column;
		gap: 13px;
		min-inline-size: 0;
	}

	.masonry-skeleton-item {
		inline-size: 100%;
	}

</style>
