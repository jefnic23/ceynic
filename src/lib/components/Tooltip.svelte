<script lang="ts">
	export let content = '';
	export let position = 'top'; // 'top', 'bottom', 'left', or 'right'
</script>

<div class="tooltip-container">
	<slot></slot>
	<div class="tooltip" data-position={position}>
		{content}
	</div>
</div>

<style>
	.tooltip-container {
		position: relative;
		display: inline-block;
	}

	.tooltip {
		position: absolute;
		background-color: #333;
		color: white;
		padding: 0.5rem;
		border-radius: 4px;
		font-size: 0.875rem;
		z-index: 100;
		opacity: 0;
		transform: scale(0.95);
		transition:
			opacity 0.2s,
			transform 0.2s;
		pointer-events: none;
        width: 100%;
		max-width: 377px; /* Limit the width of the tooltip */
		word-wrap: break-word; /* Break long words */
		white-space: normal; /* Allow text to wrap */
	}

	.tooltip-container:hover .tooltip {
		opacity: 1;
		transform: scale(1);
        pointer-events: none;
	}

	.tooltip[data-position='top'] {
		bottom: 100%;
		/* left: 50%; */
		transform: translateX(-50%);
		margin-bottom: 0.5rem;
	}

	.tooltip[data-position='bottom'] {
		top: 100%;
		/* left: 50%; */
		transform: translateX(-50%);
		margin-top: 0.5rem;
	}

	.tooltip[data-position='left'] {
		right: 100%;
		/* top: 50%; */
		transform: translateY(-50%);
		margin-right: 0.5rem;
	}

	.tooltip[data-position='right'] {
		left: 100%;
		/* top: 50%; */
		transform: translateY(-50%);
		margin-left: 0.5rem;
	}
</style>
