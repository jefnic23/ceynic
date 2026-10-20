<script lang="ts">
	interface Props {
		className?: string;
		style?: string;
	}

	let { className = '', style = '' }: Props = $props();
</script>

<div class={`skeleton-box ${className}`} style={style}></div>

<style>
	.skeleton-box {
		width: 100%;
		height: 100%;
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
