<script lang="ts">
	import Button from '$lib/components/shared/Button.svelte';

    interface Props {
        open?: boolean;
    }

    let { open = $bindable(false) }: Props = $props();
</script>

<Button type="button" class={open ? 'hamburger-button open' : 'hamburger-button'} appearance="plain" onclick={() => open = !open} aria-label="Main menu">
    <span></span>
    <span></span>
    <span></span>
    <span></span>
</Button>

<style>
    :global(button.hamburger-button) {
        width: 25px;
        height: 25px;
        position: relative;
        -webkit-transform: rotate(0deg);
        -moz-transform: rotate(0deg);
        -o-transform: rotate(0deg);
        transform: rotate(0deg);
        -webkit-transition: .5s ease-in-out;
        -moz-transition: .5s ease-in-out;
        -o-transition: .5s ease-in-out;
        transition: .5s ease-in-out;
        cursor: pointer;
        background: transparent;
        border: none;
	}

	:global(button.hamburger-button) span {
		display: block;
        position: absolute;
        height: 3px;
        width: 100%;
        background: #666;
        border-radius: 5px;
        opacity: 1;
        left: 0;
        -webkit-transform: rotate(0deg);
        -moz-transform: rotate(0deg);
        -o-transform: rotate(0deg);
        transform: rotate(0deg);
        -webkit-transition: .25s ease-in-out;
        -moz-transition: .25s ease-in-out;
        -o-transition: .25s ease-in-out;
        transition: .25s ease-in-out;
	}

    :global(button.hamburger-button) span:nth-child(1) {
        top: 3px;
    }

    :global(button.hamburger-button) span:nth-child(2), :global(button.hamburger-button) span:nth-child(3) {
        top: 11px;
    }

    :global(button.hamburger-button) span:nth-child(4) {
        top: 19px;
    }

    :global(button.hamburger-button.open) span:nth-child(1) {
        top: 11px;
        width: 0%;
        left: 50%;
    }

    :global(button.hamburger-button.open) span:nth-child(2) {
        -webkit-transform: rotate(45deg);
        -moz-transform: rotate(45deg);
        -o-transform: rotate(45deg);
        transform: rotate(45deg);
    }

    :global(button.hamburger-button.open) span:nth-child(3) {
        -webkit-transform: rotate(-45deg);
        -moz-transform: rotate(-45deg);
        -o-transform: rotate(-45deg);
        transform: rotate(-45deg);
    }

    :global(button.hamburger-button.open) span:nth-child(4) {
        top: 11px;
        width: 0%;
        left: 50%;
    }
</style>
