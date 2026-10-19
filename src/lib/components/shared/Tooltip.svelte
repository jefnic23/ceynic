<script lang="ts">
	import Icon from '@iconify/svelte';

	interface Props {
		content?: string;
		position?: string;
		infoLabel?: string;
		children?: import('svelte').Snippet;
	}

	let { content = '', position = 'top', infoLabel, children }: Props = $props();
	let container: HTMLDivElement | undefined = $state();
	let button: HTMLButtonElement | undefined = $state();
	let hovered = $state(false);
	let focused = $state(false);
	let clicked = $state(false);
	let visible = $derived(hovered || focused || clicked);
	const tooltipId = $props.id();
</script>

<svelte:window
	onclick={(event) => {
		if (infoLabel && !container?.contains(event.target as Node)) clicked = false;
	}}
	onkeydown={(event) => {
		if (infoLabel && event.key === 'Escape') {
			clicked = false;
			hovered = false;
			button?.blur();
		}
	}}
/>

<div
	class="tooltip-container"
	class:info={!!infoLabel}
	bind:this={container}
	onpointerenter={() => {
		if (infoLabel) hovered = true;
	}}
	onpointerleave={() => {
		if (infoLabel) hovered = false;
	}}
>
	{#if infoLabel}
		<button
			bind:this={button}
			type="button"
			class="trigger"
			aria-label={`More information about ${infoLabel}`}
			aria-expanded={visible}
			aria-describedby={visible ? tooltipId : undefined}
			onfocus={() => (focused = true)}
			onblur={() => {
				focused = false;
				clicked = false;
			}}
			onclick={() => (clicked = !clicked)}
		>
			<Icon icon="material-symbols:info-outline-rounded" width={18} height={18} aria-hidden="true" />
		</button>
	{:else}
		{@render children?.()}
	{/if}
	{#if !infoLabel || visible}
		<div
			class="tooltip"
			data-position={position}
			id={infoLabel ? tooltipId : undefined}
			role={infoLabel ? 'tooltip' : undefined}
		>
			{content}
		</div>
	{/if}
</div>

<style>
	.tooltip-container {
		position: relative;
		display: inline-block;
	}

	.tooltip-container:not(.info) :global(> :first-child) {
		text-decoration: underline dashed;
        text-underline-position: under;
	}

	@media (hover: hover) and (pointer: fine) {
		.tooltip-container:not(.info) :global(> :first-child):hover { cursor: help; }
		.tooltip-container:not(.info):hover .tooltip { opacity: 1; transform: scale(1); pointer-events: none; }
		.trigger:hover { color: var(--info); }
	}
	
	.tooltip {
		position: absolute;
		background-color: var(--ink-muted);
		color: var(--surface);
		padding: 0.5rem;
		border-radius: 4px;
		font-size: 0.875rem;
		z-index: 100;
		opacity: 0;
		transform: scale(0.95);
		transition: opacity 0.2s var(--ease-out);
		pointer-events: none;
        width: 100%;
		max-width: 377px; /* Limit the width of the tooltip */
		word-wrap: break-word; /* Break long words */
		white-space: normal; /* Allow text to wrap */
	}

	@media (prefers-reduced-motion: no-preference) { .tooltip { transition: opacity 0.2s var(--ease-out), transform 0.2s var(--ease-out); } }

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

	.tooltip-container.info {
		display: inline-flex;
		align-items: center;
	}

	.trigger {
		display: inline-flex;
		align-items: center;
		justify-content: center;
		width: 1.75rem;
		height: 1.75rem;
		padding: 0;
		border: 0;
		border-radius: 50%;
		background: transparent;
		color: var(--ink-muted);
		cursor: help;
	}

	.trigger:active { color: var(--info); }

	.trigger:focus-visible {
		outline: 2px solid var(--info);
		outline-offset: 2px;
	}

	.tooltip-container.info .tooltip {
		left: 0;
		width: 16rem;
		max-width: calc(100vw - 3rem);
		opacity: 1;
		transform: none;
		line-height: 1.4;
	}
</style>
