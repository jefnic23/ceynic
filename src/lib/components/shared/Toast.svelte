<script lang="ts">
	import Button from '$lib/components/shared/Button.svelte';

	interface Props {
		showToast?: boolean;
		type?: 'info' | 'warning' | 'error' | 'success';
		title: string;
		message: string;
		duration?: number;
	}

	let {
		showToast = $bindable(true),
		type = 'info',
		title,
		message,
		duration = 5000
	}: Props = $props();

	$effect(() => {
		if (!showToast) return;

		const timeout = setTimeout(() => (showToast = false), Math.max(0, duration));
		return () => clearTimeout(timeout);
	});
</script>

{#if showToast}
	<div
		class="toast {type}"
		role={type === 'warning' || type === 'error' ? 'alert' : 'status'}
	>
		<div class="content">
			<div class="header">
				<strong>{title}</strong>
				<Button type="button" class="toast-close" appearance="plain" aria-label="Close toast" onclick={() => (showToast = false)}>
					&times;
				</Button>
			</div>
			<p>{message}</p>
		</div>
		<div class="timer" style:animation-duration={`${Math.max(0, duration)}ms`}></div>
	</div>
{/if}

<style>
	.toast {
		--toast-color: var(--info);
		position: relative;
		inline-size: min(100%, 24rem);
		background: var(--surface);
		color: var(--ink-muted);
		border-radius: 0.5rem;
		border-inline-start: 0.5rem solid var(--toast-color);
		box-shadow: 0 3px 13px color-mix(in oklch, var(--ink) 13%, transparent);
		overflow: clip;
	}

	.success {
		--toast-color: var(--success);
	}

	.warning {
		--toast-color: var(--warning);
	}

	.error {
		--toast-color: var(--danger);
	}

	.content {
		padding: 1rem 1rem 1.25rem;
	}

	.header {
		display: flex;
		align-items: flex-start;
		justify-content: space-between;
		gap: 1rem;
	}

	.header strong {
		font-size: 1rem;
	}

	:global(button.toast-close) {
		border: 0;
		background: none;
		color: var(--ink-muted);
		font-size: 1.5rem;
		line-height: 1;
		cursor: pointer;
	}

	p {
		margin-block: 0.5rem 0;
		overflow-wrap: anywhere;
	}

	.timer {
		position: absolute;
		inset-block-end: 0;
		inset-inline: 0;
		block-size: 0.25rem;
		background: var(--toast-color);
		transform-origin: 0% 50%;
		animation-timing-function: linear;
		animation-fill-mode: forwards;
	}
	@media (prefers-reduced-motion: no-preference) {
		.toast { animation: toast-enter 250ms var(--ease-out) backwards; }
		.timer { animation-name: countdown; }
	}

	@keyframes countdown {
		to {
			transform: scaleX(0);
		}
	}

	@keyframes toast-enter {
		from {
			opacity: 0;
			transform: translateX(20px);
		}
		to {
			opacity: 1;
			transform: translateX(0);
		}
	}
</style>
