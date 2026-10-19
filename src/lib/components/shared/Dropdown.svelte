<script lang="ts">
	import type { Snippet } from "svelte";

	interface Props {
		id: string;
		label: string;
		value: string;
        children?: Snippet;
	}

	let {
		id,
		label,
		value = $bindable(),
        children
	}: Props = $props();
</script>

<div class="floating-field">
	<label for={id}>{label}</label>
	<select {id} name={id} bind:value>
        {@render children?.()}
    </select>
</div>

<style>
	select { padding: 13px; }
</style>
