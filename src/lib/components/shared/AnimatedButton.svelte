<!-- AnimatedButton.svelte -->
<script lang="ts">
	import { createEventDispatcher } from 'svelte';
	import Button from './Button.svelte';

	interface Props {
		text: string;
		children?: import('svelte').Snippet;
		[key: string]: any
	}

	let { text, children, ...rest }: Props = $props();

    const dispatch = createEventDispatcher();

	function handleClick(event: Event) {
		dispatch('click', event);
	}
</script>

<Button on:click={handleClick} {...rest}>
	<span class="button-content">
        <span class="text">{text}</span>
        <span class="icon">{@render children?.()}</span>
    </span>
</Button>

<style>
	.button-content {
		display: inline-flex;
		align-items: center;
		position: relative;
		transition: transform 0.3s ease;
	}

	.text {
		position: relative;
		transition: transform 0.3s ease;
	}

	.icon {
		position: absolute;
		right: -13px;
		margin-left: 0.25rem;
		opacity: 0;
		transition: transform 0.3s ease, opacity 0.3s ease;
		display: inline-flex;
		align-items: center;
	}

	:global(.base-button:hover .text) {
		transform: translateX(-0.34rem); /* shift text left */
	}

	:global(.base-button:hover .icon) {
		opacity: 1;
		transform: translateX(0.08rem); /* slide icon in from left */
	}
</style>
