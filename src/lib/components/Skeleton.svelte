<script lang="ts">
	export let placeholderCount: number = 12;

	const randomHeights = Array(placeholderCount)
		.fill(0)
		.map(() => Math.floor(Math.random() * (300 - 150 + 1) + 150));
</script>

{#each Array(placeholderCount) as _, index}
    <div class="masonry-item skeleton">
        <div
            class="skeleton-box"
            style="height: {randomHeights[index]}px;"
        ></div>
    </div>
{/each}

<style>
	.masonry-item {
		margin-bottom: 34px;
		display: inline-block;
		vertical-align: top;
		opacity: 0;
		transition: opacity 0.5s ease-in-out;
	}

	.masonry-item.skeleton {
		opacity: 1;
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
