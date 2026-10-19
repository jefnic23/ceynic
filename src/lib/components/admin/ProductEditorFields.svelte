<script lang="ts">
	import type { ProductOut } from '$lib/interfaces/ProductOut';
	import Input from '$lib/components/shared/Input.svelte';
	import TextArea from '$lib/components/shared/TextArea.svelte';
	import ScrollableInput from '$lib/components/shared/ScrollableInput.svelte';
	import Dropdown from '$lib/components/shared/Dropdown.svelte';
	import Checkbox from '$lib/components/shared/Checkbox.svelte';
	import Tooltip from '$lib/components/shared/Tooltip.svelte';
	import Dropzone from '$lib/components/Dropzone.svelte';

	let { product = $bindable(), files = $bindable() }: { product: ProductOut; files: File[] } = $props();
</script>

<Input id="title" label="Title" bind:value={product.title} />
<TextArea id="description" label="Description" bind:value={product.description as string} />

<div class="form-grid">
	<ScrollableInput bind:value={product.price as number} id="price" label="Price" min={1} step={0.01} className="price" />
	<Dropdown id="medium_id" label="Medium" value={String(product.mediumId)}>
		<option value="1">Painting</option>
		<option value="2">Print</option>
	</Dropdown>
</div>
<div class="form-grid">
	<ScrollableInput bind:value={product.height} id="height" label="Height" min={1} className="size" />
	<ScrollableInput bind:value={product.width} id="width" label="Width" min={1} className="size" />
</div>
<div class="checkbox-help">
	<Checkbox name="enabled" label="Enabled" bind:checked={product.enabled} />
	<Tooltip infoLabel="Enabled" content="Controls whether the product is available for display on the site." />
</div>
<Dropzone previews={product.images || []} bind:files />

<style>
	.checkbox-help { display: inline-flex; align-items: center; gap: 0.25rem; }
</style>
