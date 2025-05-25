<script lang="ts">
	interface Props {
		duration?: string;
		offset?: number;
		tolerance?: number;
		open?: boolean;
		children?: import('svelte').Snippet;
	}

	let {
		duration = '377ms',
		offset = 0,
		tolerance = 0,
		open = false,
		children
	}: Props = $props();

	let headerClass = $state('pin');
	let lastHeaderClass = $state('pin');
	let y = $state(0);
	let lastY = $state(0);

	function deriveClass(y: number = 0, scrolled: number = 0): string {
		if (y <= offset) return 'pin';
		if (!scrolled || Math.abs(scrolled) < tolerance) return headerClass;
		return scrolled < 0 ? 'unpin' : 'pin';
	}

	function updateClass(y: number = 0): string {
		const scrolledPxs = lastY - y;
		const result = deriveClass(y, scrolledPxs);
		lastY = y;
		return result;
	}

	function action(node: HTMLElement): void {
		node.style.transitionDuration = duration;
	}

	$effect(() => {
		if (!open) {
			headerClass = updateClass(y);
			lastHeaderClass = headerClass;
		} else {
			lastY = y;
		}
	});
</script>

<svelte:window bind:scrollY={y} />

<div use:action class={headerClass}>
	{@render children?.()}
</div>

<style>
	div {
		position: sticky;
		width: 100%;
		top: 0;
		transition: transform 377ms ease-in-out;
		z-index: 9999999;
		will-change: transform;
		view-transition-name: header;
	}

	.pin {
		transform: translateY(0%);
	}

	.unpin {
		transform: translateY(-100%);
	}
</style>
