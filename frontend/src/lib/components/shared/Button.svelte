<script lang="ts">
	import { ButtonStyle } from '$lib/enums/buttonStyle';
	import { ButtonSize } from '$lib/enums/buttonSize';
	import type {  Snippet } from 'svelte';
	import type { HTMLButtonAttributes } from 'svelte/elements';

	interface Props extends HTMLButtonAttributes {
		style?: ButtonStyle;
		size?: ButtonSize;
		disabled?: boolean;
		loading?: boolean;
		fullWidth?: boolean;
		tooltip?: string | null;
		appearance?: 'default' | 'plain';
		buttonType?: "submit" | "reset" | "button";
		children?: Snippet;
	}

	let {
		style = ButtonStyle.Submit,
		size = ButtonSize.Medium,
		disabled = false,
		loading = false,
		fullWidth = false,
		tooltip = null,
		appearance = 'default',
		buttonType = "button",
		type,
		class: className = '',
		children,
		...rest
	}: Props = $props();
</script>

<button
	class="base-button {style} {size} {appearance} {fullWidth ? 'full-width' : ''} {disabled ? 'disabled' : ''} {className}"
	type={type ?? buttonType}
	title={tooltip}
	{disabled}
	{...rest}
>
	{#if loading}
		<!-- todo: use <Skeleton /> instead -->
		<span class="spinner"></span>
	{:else}
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
		overflow: clip;
		position: relative;
		transition: background-color 0.3s ease;
	}

	/* Style Variants */
	.submit {
		background-color: var(--success);
		color: var(--surface);
	}
	.cancel {
		background-color: var(--danger);
		color: var(--surface);
	}
	.info {
		background-color: var(--info);
		color: var(--surface);
	}
	.warning {
		background-color: var(--warning);
		color: var(--surface);
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

	.plain {
		padding: 0;
		background: transparent;
		color: inherit;
		border-radius: 0;
	}

	/* Full Width */
	.full-width {
		inline-size: 100%;
	}

	/* Disabled State */
	button:disabled,
	.disabled {
		background-color: var(--border);
		color: var(--ink-muted);
		cursor: not-allowed;
	}

	/* Loading Spinner */
	.spinner {
		border: 2px solid color-mix(in oklch, var(--surface) 60%, transparent);
		border-block-start-color: var(--surface);
		border-radius: 50%;
		inline-size: 1em;
		block-size: 1em;
	}

	@media (prefers-reduced-motion: no-preference) {
		.spinner { animation: spin 0.6s linear infinite; }
	}

	@keyframes spin {
		0% {
			transform: rotate(0deg);
		}
		100% {
			transform: rotate(360deg);
		}
	}

	button:focus-visible { outline-color: var(--info); }
	button:active:not(:disabled) { filter: brightness(0.88); }
	@media (hover: hover) and (pointer: fine) {
		:is(.submit, .cancel, .info, .warning):hover:not(:disabled):not(.plain) {
			filter: brightness(0.95);
		}
		.neutral:hover:not(:disabled):not(.plain) { background-color: color-mix(in oklch, var(--border), var(--surface) 35%); }
	}
</style>
