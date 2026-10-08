<script lang="ts">
	import Button from '$lib/components/shared/Button.svelte';
	import Card from '$lib/components/shared/Card.svelte';
	import Dropzone from '$lib/components/Dropzone.svelte';
	import Modal from '$lib/components/shared/Modal.svelte';
	import type { ProductOut } from '$lib/interfaces/ProductOut';
	import type { PageData } from './$types';
	import { PUBLIC_API_URL } from '$env/static/public';
	import { ButtonStyle } from '$lib/enums/buttonStyle';
	import Skeleton from '$lib/components/shared/Skeleton.svelte';
	import { currencyFormatter } from '$lib/utils/formatters';
	import ProductImage from '$lib/components/ProductImage.svelte';
	import Icon from '@iconify/svelte';
	import ScrollableInput from '$lib/components/shared/ScrollableInput.svelte';
	import Dropdown from '$lib/components/shared/Dropdown.svelte';
	import { enhance } from '$app/forms';
	import Input from '$lib/components/shared/Input.svelte';
	import TextArea from '$lib/components/shared/TextArea.svelte';

	interface Props {
		data: PageData;
	}

	let { data }: Props = $props();

	let showModal: boolean = $state(false);
	let loadingModal: boolean = $state(false);
	let modalMode: 'create' | 'update' = $state('update');
	let selectedProduct: ProductOut = $state(createEmptyProduct());
	let files: File[] = $state([]);

	function createEmptyProduct(): ProductOut {
		return {
			id: 0,
			title: '',
			description: '',
			price: 1.00,
			height: 1,
			width: 1,
			enabled: true,
			dateAdded: '',
			mediumId: 1,
			storefrontId: 0,
			images: [],
			medium: null
		};
	}

	function openCreateModal() {
		modalMode = 'create';
		selectedProduct = createEmptyProduct();
		files = [];
		loadingModal = false;
		showModal = true;
	}

	async function openEditModal(product: ProductOut) {
		modalMode = 'update';
		files = [];
		showModal = true;
		loadingModal = true;
		const response = await fetch(`${PUBLIC_API_URL}/products/${product.id}`);

		if (response.status !== 200) {
			console.log('Error retrieving product.');
			loadingModal = false;
			showModal = false;
			return;
		}

		const responseData: ProductOut = await response.json();

		selectedProduct = responseData;
		loadingModal = false;
	}
</script>

<div class="container">
	<Card width="-webkit-fill-available">
		<div class="header">
			<h1>Products</h1>
			<Button style={ButtonStyle.Info} onclick={openCreateModal}>
				<div>Add New Product</div>
				<Icon icon="material-symbols:add-rounded" />
			</Button>
		</div>
		{#await data.products}
			<Skeleton />
		{:then products}
			<table>
				<thead>
					<tr>
						<th></th>
						<th>Title</th>
						<th>Price</th>
						<th>Height</th>
						<th>Width</th>
						<th>Medium</th>
						<th>Enabled</th>
						<th>Actions</th>
					</tr>
				</thead>
				<tbody>
					{#each products as product}
						<tr>
							<td>
								<div class="thumbnail">
									<ProductImage
										url={product.images?.[0]?.url}
										alt={product.title}
										width={48}
										height={48}
									/>
								</div>
							</td>
							<td>{product.title}</td>
							<td>{currencyFormatter.format((product.price as number))}</td>
							<td>{product.height}"</td>
							<td>{product.width}"</td>
							<td>{product.medium?.name}</td>
							<td>
								{#if product.enabled}
									<Icon icon="material-symbols:check-rounded" width={32} height={32} color={"green"} />
								{:else}
									<Icon icon="material-symbols:close-rounded" width={32} height={32} color={"red"} />
								{/if}
							</td>
							<td>
								<Button style={ButtonStyle.Info} onclick={async () => await openEditModal(product)}>
									<div>Edit</div>
									<Icon icon="material-symbols:edit-rounded" width={16} height={16} />
								</Button>
								<Button style={ButtonStyle.Cancel}>
									<div>Delete</div>
									<Icon icon="material-symbols:delete-rounded" width={16} height={16} />
								</Button>
							</td>
						</tr>
					{/each}
				</tbody>
			</table>
		{:catch error}
			<div>Something went wrong: {error.message}</div>
		{/await}
	</Card>
</div>

{#if showModal}
	<Modal bind:showModal title={modalMode === 'create' ? 'Add New Product' : 'Edit Product'}>
		{#if loadingModal}
			<div>loading product...</div>
		{:else}
			<form 
				method="POST" 
				action={modalMode === 'create' ? '?/create' : '?/update'}
				enctype="multipart/form-data" 
				class="edit" 
				use:enhance={({ formData }) => {
					// Remove the empty <input type="file"> contents
					formData.delete('medium');
					formData.delete('images');

					// Attach every NEW image in the right order
					files.forEach((item) => {
						if (item instanceof File) {
							formData.append('images', item, item.name);
						}
					});

					return async ({ result, update }) => {
						await update();
						if (result.type === 'success') showModal = false;
					}
				}}
			>
				{#if modalMode === 'update'}
					<input type="hidden" id="id" name="id" value={selectedProduct.id} />
				{/if}
				<div class="form-input">
					<Input id="title" label="Title" bind:value={selectedProduct.title} />
				</div>
				<div class="form-input">
					<TextArea id="description" label="Description" bind:value={selectedProduct.description as string}/>
				</div>

				<div class="form-row">
					<div class="form-input">
						<ScrollableInput 
							bind:value={selectedProduct.price as number} 
							id={"price"} 
							label={"Price"}
							min={1.00}
							step={0.01} 
							className={"price"} 
						/>
					</div>

					<div class="form-input">
						<Dropdown id="medium_id" label="Medium" value={String(selectedProduct.mediumId)}>
							<option value="1">Painting</option>
							<option value="2">Print</option>
						</Dropdown>
					</div>
				</div>

				<div class="form-row">
					<div class="form-input">
						<ScrollableInput 
							bind:value={selectedProduct.height} 
							id={"height"} 
							label={"Height"}
							min={1} 
							className={"size"} 
						/>
					</div>

					<div class="form-input">
						<ScrollableInput 
							bind:value={selectedProduct.width} 
							id={"width"} 
							label={"Width"} 
							min={1} 
							className={"size"} 
						/>
					</div>
				</div>

				<div class="form-row">
					<div class="form-input">
						<label for="enabled">Enabled</label>
						<div class="checkbox">
							<input 
								id="enabled" 
								name="enabled"
								type="checkbox" 
								value={selectedProduct.enabled} 
								bind:checked={selectedProduct.enabled} 
							/>
						</div>
					</div>
				</div>

				<Dropzone previews={selectedProduct.images || []} bind:files={files} />

				<div class="form-buttons">
					<Button buttonType={"submit"}>
						{modalMode === 'create' ? 'Add Product' : 'Update Product'}
					</Button>
					<Button style={ButtonStyle.Cancel} onclick={() => showModal = false}>
						Cancel
					</Button>
				</div>
			</form>
		{/if}
	</Modal>
{/if}

<style>
	.container {
		display: flex;
		flex-direction: column;
		width: 100%;
	}

	.header {
		display: flex;
		flex-direction: row;
		justify-content: space-between;
		align-items: center;
	}

	table {
		width: 100%;
		max-width: 1500px;
		border-collapse: collapse;
		text-align: left;
		font-size: 18px;
		margin: auto;
		overflow: auto;
		white-space: nowrap;
	}

	th {
		background-color: #04AA6D;
		color: white;
	}

	tr {
		height: fit-content;
		vertical-align: middle;
	}

	tbody tr:nth-of-type(odd) {
		background-color: #e9e9e9;
	}

	input {
		width: 100%;
	}

	.thumbnail {
		display: flex;
		padding: 0.5rem;
	}

	.edit {
		display: flex;
		flex-direction: column;
		row-gap: 1rem;
		width: 35em;
	}

	.form-row {
		display: flex;
		flex-direction: row;
		align-items: center;
		justify-content: space-between;
		column-gap: 1rem;
	}

	.form-input {
		display: flex;
		flex-direction: column;
		flex: 1;
	}

	.form-buttons {
		display: flex;
		flex-direction: row;
		align-items: center;
		justify-content: flex-end;
		column-gap: 1rem;
	}

	.checkbox {
		display: flex;
		justify-content: flex-start;
	}

	.checkbox input {
		height: 21px;
		width: 21px;
		margin: 0;
	}

	:is(tbody > tr):hover {
		outline: 2px solid #666;
		outline-offset: -2px;
	}
</style>
