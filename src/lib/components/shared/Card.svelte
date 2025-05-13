<script>
    /** @type {{children?: import('svelte').Snippet}} */
    let { children } = $props();
</script>

<div class="card">
    {@render children?.()}
</div>

<style>
    .card {
        background: #fff;
        padding: 21px;
        border-radius: 8px;
        box-shadow: rgba(0, 0, 0, 0.13) 0px 3px 13px;
        width: fit-content;
        margin: auto;
    }
</style>