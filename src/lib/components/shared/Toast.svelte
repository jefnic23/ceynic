<script lang="ts">
	import { cubicIn } from 'svelte/easing';
	import { fly } from 'svelte/transition';

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
		out:fly={{ x: 20, duration: 200, easing: cubicIn }}
	>
		<div class="content">
			<div class="header">
				<strong>{title}</strong>
				<button type="button" aria-label="Close toast" onclick={() => (showToast = false)}>
					&times;
				</button>
			</div>
			<p>{message}</p>
		</div>
		<div class="timer" style:animation-duration={`${Math.max(0, duration)}ms`}></div>
	</div>
{/if}

<style>
	.toast {
		--toast-color: #1e90ff;
		position: relative;
		width: min(100%, 24rem);
		background: white;
		color: #333;
		border-radius: 0.5rem;
		border-left: 0.5rem solid var(--toast-color);
		box-shadow: 0 3px 13px rgba(0, 0, 0, 0.13);
		overflow: hidden;
		animation: toast-enter 250ms cubic-bezier(0.22, 1, 0.36, 1) backwards;
	}

	.success {
		--toast-color: #28a745;
	}

	.warning {
		--toast-color: #ffcc00;
	}

	.error {
		--toast-color: #ff6347;
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

	button {
		border: 0;
		background: none;
		color: #333;
		font-size: 1.5rem;
		line-height: 1;
		cursor: pointer;
	}

	p {
		margin: 0.5rem 0 0;
		overflow-wrap: anywhere;
	}

	.timer {
		position: absolute;
		bottom: 0;
		left: 0;
		right: 0;
		height: 0.25rem;
		background: var(--toast-color);
		transform-origin: left;
		animation-name: countdown;
		animation-timing-function: linear;
		animation-fill-mode: forwards;
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
