<script lang="ts">
	import { ButtonStyle } from '$lib/enums/buttonStyle';
	import { ButtonSize } from '$lib/enums/buttonSize';
	import { createEventDispatcher } from 'svelte';

	interface Props {
		text?: string;
		name?: string;
		value?: string;
		style?: ButtonStyle;
		size?: ButtonSize;
		disabled?: boolean;
		loading?: boolean;
		fullWidth?: boolean;
		tooltip?: string | null;
		children?: import('svelte').Snippet;
	}

	let {
		text = "",
		name = "",
		value = "",
		style = ButtonStyle.Submit,
		size = ButtonSize.Medium,
		disabled = false,
		loading = false,
		fullWidth = false,
		tooltip = null,
		children
	}: Props = $props();

	const dispatch = createEventDispatcher();

	function handleClick(event: Event) {
		if (!disabled && !loading) {
			dispatch('click', event);
		}
	}
</script>

<button
	class="base-button {style} {size} {fullWidth ? 'full-width' : ''} {disabled ? 'disabled' : ''}"
	onclick={handleClick}
	{disabled}
	title={tooltip}
	name={name}
	value={value}
>
	{#if loading}
		<!-- todo: use <Skeleton /> instead -->
		<span class="spinner"></span>
	{:else}
		{text}
		{@render children?.()}
	{/if}
</button>

<style>
	button {
		display: inline-flex;
		align-items: center;
		justify-content: center;
		column-gap: 5px;
		border: none;
		cursor: pointer;
		padding: 0.5rem 1.5rem;
		font-size: 1rem;
		border-radius: 0.25rem;
		overflow: hidden;
		position: relative;
		height: 100%;
		transition:
			background-color 0.3s ease,
			transform 0.2s ease,
			box-shadow 0.2s ease;
	}

	/* Style Variants */
	.submit {
		background-color: #4caf50;
		color: white;
	}
	.cancel {
		background-color: #f44336;
		color: white;
	}
	.info {
		background-color: #2196f3;
		color: white;
	}
	.warning {
		background-color: #ff9800;
		color: white;
	}

	/* Size Variants */
	.small {
		font-size: 0.75rem;
		padding: 0.25rem 0.75rem;
	}
	.medium {
		font-size: 1rem;
		padding: 0.5rem 1.5rem;
	}
	.large {
		font-size: 1.25rem;
		padding: 0.75rem 2rem;
	}

	/* Full Width */
	.full-width {
		width: 100%;
	}

	/* Disabled State */
	button:disabled,
	.disabled {
		background-color: #e0e0e0;
		color: #9e9e9e;
		cursor: not-allowed;
	}

	/* Loading Spinner */
	.spinner {
		border: 2px solid rgba(255, 255, 255, 0.6);
		border-top: 2px solid white;
		border-radius: 50%;
		width: 1em;
		height: 1em;
		animation: spin 0.6s linear infinite;
	}

	@keyframes spin {
		0% {
			transform: rotate(0deg);
		}
		100% {
			transform: rotate(360deg);
		}
	}

	/* Hover Effects */
	button:hover {
		transform: scale(1.03); /* Slight scale-up effect */
		box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2); /* Adds a subtle shadow */
	}
</style>
