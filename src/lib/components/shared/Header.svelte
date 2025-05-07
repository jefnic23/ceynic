<script lang="ts">
	import { createEventDispatcher } from 'svelte';

	export let duration = '377ms';
	export let offset = 0;
	export let tolerance = 0;
	export let open: boolean = false;

	let headerClass = 'pin';
	let lastHeaderClass = 'pin';
	let y = 0;
	let lastY = 0;

	const dispatch = createEventDispatcher();

	function deriveClass(y: number = 0, scrolled: number = 0): string {
		// if (y <= 0) {
		// 	headerClass = 'pin';
		// 	lastHeaderClass = 'pin';
		// 	lastY = 0;
		// 	return 'pin';
		// }
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

	$: {
		if (!open) {
			headerClass = updateClass(y);
			if (headerClass !== lastHeaderClass) {
				dispatch(headerClass);
			}
			lastHeaderClass = headerClass;
		} else {
			lastY = y;
		}
	}
</script>

<svelte:window bind:scrollY={y} />

<div use:action class={headerClass}>
	<slot />
</div>

<style>
	div {
		position: sticky;
		width: 100%;
		top: 0;
		transition: transform 377ms ease-in-out;
		z-index: 9999;
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
