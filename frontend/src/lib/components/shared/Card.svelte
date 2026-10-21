<script lang="ts">
	import type { Snippet } from 'svelte';

    interface Props {
        width?: string;
        children?: Snippet;
    }

    let {
        width = "fit-content",
        children
    }: Props = $props();
</script>

<div class="card" style:--card-width={width}>
    {@render children?.()}
</div>

<style>
    .card {
        background: var(--surface);
        box-sizing: border-box;
        padding: 21px;
        border-radius: 8px;
        box-shadow: 0 3px 13px color-mix(in oklch, var(--ink) 13%, transparent);
        inline-size: var(--card-width);
        max-inline-size: 100%;
        margin-inline: auto;
    }
</style>
