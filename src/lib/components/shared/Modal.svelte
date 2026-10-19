<script lang="ts">
	import type { Snippet } from 'svelte';
	import Button from '$lib/components/shared/Button.svelte';

	interface Props {
		showModal: boolean;
		showClose?: boolean;
		dismissible?: boolean;
		busy?: boolean;
		busyLabel?: string;
		type?: 'info' | 'success' | 'warning' | 'error' | 'none';
		title?: string;
		children?: Snippet;
	}

	let {
		showModal = $bindable(),
		showClose = true,
		dismissible = true,
		busy = false,
		busyLabel = 'Loading…',
		type = 'none',
		title = '',
		children
	}: Props = $props();

	let dialog: HTMLDialogElement | undefined = $state();

	$effect(() => {
		if (dialog && showModal) dialog.showModal();
	});

	// todo: clicking outside modal if showClose is true should also close modal
</script>

<dialog
	bind:this={dialog}
	onclose={() => (showModal = false)}
	oncancel={(event) => {
		if (!dismissible || busy) event.preventDefault();
	}}
	class={type}
>
	<div>
		<div inert={busy} aria-busy={busy}>
			<div class="header {showClose ? 'justify-between' : 'justify-center'}">
				<h2>{title}</h2>
				<!-- svelte-ignore a11y_autofocus -->
				{#if showClose && dismissible && !busy}
					<Button type="button" title="Close" class="close-button" appearance="plain" autofocus onclick={() => dialog?.close()}>&times;</Button>
				{/if}
			</div>
			{@render children?.()}
		</div>
		{#if busy}
			<div class="busy-overlay" role="status" aria-live="polite">
				<span class="busy-spinner" aria-hidden="true"></span>
				<span>{busyLabel}</span>
			</div>
		{/if}
	</div>
</dialog>

<style>
	dialog {
		max-inline-size: min(50em, calc(100vw - 2rem));
		max-block-size: 80dvh;
		border-radius: 0.5em;
		border: none;
		padding: 0;
		overflow-y: auto;
		overscroll-behavior: contain;
	}

	dialog::backdrop {
		background: color-mix(in oklch, var(--ink) 30%, transparent);
	}

	dialog > div {
		position: relative;
		padding-block: 1em;
		padding-inline: 1.34em 1em;
	}

	.busy-overlay {
		position: absolute;
		inset: 0;
		display: flex;
		flex-direction: column;
		align-items: center;
		justify-content: center;
		gap: 0.75rem;
		background: color-mix(in oklch, var(--surface) 85%, transparent);
	}

	.busy-spinner {
		width: 2rem;
		height: 2rem;
		border: 3px solid var(--border);
		border-block-start-color: var(--info);
		border-radius: 50%;
	}
	@media (prefers-reduced-motion: no-preference) { .busy-spinner { animation: spin 0.7s linear infinite; } }

	@keyframes spin {
		to {
			transform: rotate(360deg);
		}
	}

	@media (prefers-reduced-motion: no-preference) {
		dialog[open] { animation: zoom 0.3s var(--ease-out); }
		dialog[open]::backdrop { animation: fade 0.2s var(--ease-out); }
	}

	@keyframes zoom {
		from {
			transform: scale(0.95);
		}
		to {
			transform: scale(1);
		}
	}

	@keyframes fade {
		from {
			opacity: 0;
		}
		to {
			opacity: 1;
		}
	}

	.header {
		display: flex;
		flex-direction: row;
		align-items: center;
		text-transform: uppercase;
	}

	.justify-between {
		justify-content: space-between;
	}

	.justify-center {
		justify-content: center;
	}

	/* Close button styling */
	:global(button.close-button) {
		background: none;
		border: none;
		font-size: 1.5em;
		cursor: pointer;
		color: var(--ink-muted);
	}

	:global(button.close-button:active) { color: var(--ink); }
	@media (hover: hover) and (pointer: fine) { :global(button.close-button:hover) { color: var(--ink); } }

	/* Colored bar on the left edge */
	dialog::before {
		content: '';
		position: absolute;
		inset-inline-start: 0;
		inset-block: 0;
		inline-size: 0.5em;
		border-radius: 0.5em 0 0 0.5em;
		background-color: var(--modal-bar-color);
	}

	/* Modal types */
	.info::before {
		--modal-bar-color: var(--info);
	}

	.success::before {
		--modal-bar-color: var(--success);
	}

	.warning::before {
		--modal-bar-color: var(--warning);
	}

	.error::before {
		--modal-bar-color: var(--danger);
	}
</style>
