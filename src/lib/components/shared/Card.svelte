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

<div class="card" style:width={width}>
    {@render children?.()}
</div>

<style>
    .card {
        background: #fff;
        padding: 21px;
        border-radius: 8px;
        box-shadow: rgba(0, 0, 0, 0.13) 0px 3px 13px;
        margin: auto;
    }
</style>
