<script lang="ts">
	import type { Snippet } from 'svelte';

	interface Props {
		showModal: boolean;
		showClose?: boolean;
		type?: 'info' | 'success' | 'warning' | 'error' | 'none';
		title?: string;
		children?: Snippet;
	}

	let {
		showModal = $bindable(),
		showClose = true,
		type = 'none',
		title = '',
		children
	}: Props = $props();

	let dialog: HTMLDialogElement | undefined = $state();

	$effect(() => {
		if (dialog && showModal) dialog.showModal();
	});

	function handleClick(event: Event) {
		event.stopPropagation();
	}

	// todo: clicking outside modal if showClose is true should also close modal
</script>

<dialog bind:this={dialog} onclose={() => (showModal = false)} class={type}>
	<div 
		onclick={handleClick}
		onkeydown={(e) => { 
            if (e.key !== "Enter" && e.key !== " ") return; 
            e.preventDefault();
            (e.target as HTMLElement).click();
        }} 
		role="button" 
        tabindex="0" 
        aria-pressed="false"
	>
		<div class="header {showClose ? 'justify-between' : 'justify-center'}">
			<h2>{title}</h2>
			<!-- svelte-ignore a11y_autofocus -->
			{#if showClose}
				<button class="close-button" autofocus onclick={() => dialog?.close()}>&times;</button>
			{/if}
		</div>
		{@render children?.()}
	</div>
</dialog>

<style>
	dialog {
		max-width: 50em;
		border-radius: 0.5em;
		border: none;
		padding: 0;
		overflow: hidden;
	}

	dialog::backdrop {
		background: rgba(0, 0, 0, 0.3);
	}

	dialog > div {
		padding: 1em 1em 1em 1.34em;
		transition:
			max-height 0.3s ease,
			height 0.3s ease;
	}

	dialog[open] {
		animation: zoom 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
	}

	@keyframes zoom {
		from {
			transform: scale(0.95);
		}
		to {
			transform: scale(1);
		}
	}

	dialog[open]::backdrop {
		animation: fade 0.2s ease-out;
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
	.close-button {
		background: none;
		border: none;
		font-size: 1.5em;
		cursor: pointer;
		color: #333;
		transition:
			transform 0.2s ease,
			color 0.2s ease;
	}

	.close-button:hover {
		transform: scale(1.2);
		color: #000;
	}

	/* Colored bar on the left edge */
	dialog::before {
		content: '';
		position: absolute;
		left: 0;
		top: 0;
		bottom: 0;
		width: 0.5em;
		border-radius: 0.5em 0 0 0.5em;
		background-color: var(--modal-bar-color);
	}

	/* Modal types */
	.info::before {
		--modal-bar-color: #1e90ff; /* Blue for info */
	}

	.success::before {
		--modal-bar-color: #28a745; /* Green for success */
	}

	.warning::before {
		--modal-bar-color: #ffcc00; /* Yellow for warning */
	}

	.error::before {
		--modal-bar-color: #ff6347; /* Red for error */
	}
</style>
