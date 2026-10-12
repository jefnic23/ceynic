<script lang="ts">
	import type { Snippet } from 'svelte';
	import Toast from '$lib/components/shared/Toast.svelte';
	import { provideToast, type ToastMessage } from '$lib/state/toast';
	import '../app.css';

	interface Props {
		children?: Snippet;
	}

	let { children }: Props = $props();
	let notification: (ToastMessage & { id: number }) | null = $state(null);
	let visible = $state(false);
	let nextId = 0;

	provideToast(
		(toast) => {
			notification = { ...toast, id: ++nextId };
			visible = true;
		},
		() => (visible = false)
	);
</script>

{@render children?.()}

{#if notification}
	<div class="toast-container">
		{#key notification.id}
			<Toast
				bind:showToast={visible}
				type={notification.type}
				title={notification.title}
				message={notification.message}
				duration={notification.duration}
			/>
		{/key}
	</div>
{/if}

<style>
	.toast-container {
		position: fixed;
		top: 1rem;
		right: 1rem;
		width: min(24rem, calc(100vw - 2rem));
		z-index: 1000;
		view-transition-name: toast;
	}

	:global(::view-transition-old(toast)),
	:global(::view-transition-new(toast)) {
		animation: none;
	}
</style>
