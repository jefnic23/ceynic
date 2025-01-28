<script lang="ts">
	export let placeholderCount: number = 12;
	export let randomizeHeights: boolean = false;
	export let type: 'image' | 'table-row' | 'paragraph' | 'square' = 'square'; // Add types

	const randomHeights = Array(placeholderCount)
		.fill(0)
		.map(() => Math.floor(Math.random() * (300 - 150 + 1) + 150));

	// Define sizes for different skeleton types
	const typeStyles = {
		image: { width: '100%', height: '200px' },
		'table-row': { width: '100%', height: '40px' },
		square: { width: '150px', height: '150px' },
		paragraph: { width: '100%', height: '24px' } // Default line height
	};

</script>

{#if type === 'paragraph'}
	<div class="skeleton">
		{#each Array(3) as _}
			<div style="margin-bottom: 32px;">
				{#each Array(4) as _}
					<div
						class="skeleton-box"
						style="
							width: {`${Math.random() * (90 - 50) + 50}%`};
							height: {typeStyles.paragraph.height};
							margin-bottom: 8px;
						"
					></div>
				{/each}
			</div>
		{/each}
	</div>
{:else}
	{#each Array(placeholderCount) as _, index}
		<div class="skeleton">
			<div
				class="skeleton-box"
				style="
					width: {typeStyles[type].width};
					height: {randomizeHeights && type === 'image' ? randomHeights[index] : typeStyles[type].height};
				"
			></div>
		</div>
	{/each}
{/if}

<style>
	.skeleton {
		margin-bottom: 34px;
		display: inline-block;
		vertical-align: top;
		animation: shimmer 1.5s infinite;
	}

	.skeleton-box {
		width: 225px;
		background: linear-gradient(to right, #eeeeee 8%, #dddddd 18%, #eeeeee 33%);
		background-size: 800px 104px;
		animation: shimmer 1.5s infinite;
		border-radius: 4px;
	}

	@keyframes shimmer {
		0% {
			background-position: -400px 0;
		}
		100% {
			background-position: 400px 0;
		}
	}
</style>
