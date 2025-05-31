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
	import { CldImage } from 'svelte-cloudinary';
	import Icon from '@iconify/svelte';

	interface Props {
		data: PageData;
	}

	let { data }: Props = $props();

	let showModal: boolean = $state(false);
	let loadingModal: boolean = $state(false);
	let selectedProduct: ProductOut = $state()!;

	async function openEditModal(product: ProductOut) {
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

	function replaceImageUrl(imageUrl: string) {
		const filename = imageUrl.split('/').at(-1);
		return `/api/proxy/${selectedProduct?.title?.replaceAll(' ', '_')}/${filename}`;
	}
	
	let images: File[] = [];

	function handleImagesChange(event: CustomEvent<{ files: File[] }>) {
		images = event.detail.files;
	}

	function handleThumbnailChange(event: CustomEvent<{ thumbnail: string }>) {
		selectedProduct.thumbnail = event.detail.thumbnail;
	}

	function handleSubmit(event: Event) {
		event.preventDefault();
		console.log(selectedProduct);
		// const formData = new FormData(event.target as HTMLFormElement);
		// images.forEach((image) => formData.append('images', image));
		// Send `formData` to your API endpoint
	}
</script>

<div class="container">
	<Card>
		<div class="header">
			<h1>Products</h1>
			<Button style={ButtonStyle.Info}>
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
						<th></th>
					</tr>
				</thead>
				<tbody>
					{#each products as product}
						<tr>
							<td>
								<CldImage
									src={product.images?.[0]?.publicId || ""}
									alt={product.title}
									width={48}
									height={48}
								/>
							</td>
							<td>{product.title}</td>
							<td>{currencyFormatter.format((product.price as number))}</td>
							<td>{product.height}"</td>
							<td>{product.width}"</td>
							<td>{product.medium}</td>
							<td>
								{#if product.enabled}
									<Icon icon="material-symbols:check-rounded" width={32} height={32} />
								{:else}
									<Icon icon="material-symbols:close-rounded" width={32} height={32} />
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
	<Modal bind:showModal title="Edit Product">
		{#if loadingModal}
			<div>loading product...</div>
		{:else}
			<div class="edit">
				<div class="form-input">
					<label for="title">Title</label>
					<input id="title" type="text" value={selectedProduct.title} />
				</div>
				<div class="form-input">
					<label for="description">Description</label>
					<textarea id="description" value={selectedProduct.description}></textarea>
				</div>

				<div class="form-row">
					<div class="form-input">
						<label for="price">Price</label>
						<div class="price">
							<input
								id="price"
								type="number"
								min="0.01"
								step="0.01"
								value={selectedProduct.price}
							/>
						</div>
					</div>

					<div class="form-input">
						<label for="medium">Medium</label>
						<select id="medium" bind:value={selectedProduct.medium}>
							<option value="Painting">Painting</option>
							<option value="Print">Print</option>
						</select>
					</div>
				</div>

				<div class="form-row">
					<div class="form-input">
						<label for="height">Height</label>
						<div class="inches">
							<input id="height" type="number" min="1" step="1" value={selectedProduct.height} />
						</div>
					</div>

					<div class="form-input">
						<label for="width">Width</label>
						<div class="inches">
							<input id="width" type="number" min="1" step="1" value={selectedProduct.width} />
						</div>
					</div>
				</div>

				<div class="form-row">
					<div class="form-input">
						<label for="enabled">Enabled</label>
						<div class="checkbox">
							<input id="enabled" type="checkbox" value={selectedProduct.enabled} bind:checked={selectedProduct.enabled} />
						</div>
					</div>
				</div>

				<Dropzone
					change={handleImagesChange}
					thumbnailChange={handleThumbnailChange}
					previews={selectedProduct.images || []}
					thumbnail={selectedProduct.thumbnail}
				/>

				<div class="form-buttons">
					<Button onclick={handleSubmit}>
						Submit
					</Button>
					<Button style={ButtonStyle.Cancel} onclick={() => showModal = false}>
						Cancel
					</Button>
				</div>

				<!-- <div class="image-container">
					{#each selectedProduct.images as image}
						<div class="image-wrapper">
							<img src={image} alt={image} />
							{#if image.endsWith(selectedProduct.thumbnail)}
								<div class="thumbnail-overlay">
									<Thumbnail width="3em" height="3em" />
								</div>
							{/if}
						</div>
					{/each}
				</div> -->
			</div>
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
		width: 100vw;
		max-width: 1500px;
		border-collapse: collapse;
		text-align: left;
		font-size: 18px;
		margin: auto;
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

	textarea {
		resize: vertical;
		height: 89px;
	}

	input {
		width: 100%;
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

	.price {
		position: relative;
		display: inline-block;
	}

	.price input {
		padding-left: 1.5em; /* Add space for the dollar sign */
	}

	.price::before {
		content: '$';
		position: absolute;
		left: 0.5em; /* Adjust positioning as needed */
		top: 50%;
		transform: translateY(-50%);
		font-size: 1em;
		font-weight: bold;
		color: #333; /* Adjust color as needed */
	}

	.inches {
		position: relative;
		display: inline-block;
	}

	.inches input {
		padding-right: 2em;
	}

	.inches::after {
		content: 'in.';
		position: absolute;
		right: 0.34em; /* Adjust positioning as needed */
		top: 50%;
		transform: translateY(-50%);
		line-height: normal;
		font-size: 1em;
		font-weight: bold;
		color: #333; /* Adjust color as needed */
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

	/* .thumbnail {
		display: flex;
		justify-content: center;
		align-items: center;
		height: inherit;
	}

	.thumbnail img {
		width: 48px;
		height: 48px;
		margin: 0.5rem 0;
	} */

	:is(tbody > tr):hover {
		outline: 2px solid #666;
		outline-offset: -2px;
	}
</style>
