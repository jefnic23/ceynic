<script lang="ts">
	import Button from '$lib/components/shared/Button.svelte';
	import Card from '$lib/components/shared/Card.svelte';
	import Table from '$lib/components/shared/Table.svelte';
	import Modal from '$lib/components/shared/Modal.svelte';
	import type { ProductOut } from '$lib/interfaces/ProductOut';
	import type { PageData } from './$types';
	import { PUBLIC_API_URL } from '$env/static/public';
	import { ButtonStyle } from '$lib/enums/buttonStyle';
	import Skeleton from '$lib/components/shared/Skeleton.svelte';
	import { currencyFormatter } from '$lib/utils/formatters';
	import ProductImage from '$lib/components/ProductImage.svelte';
	import Icon from '@iconify/svelte';
	import { enhance } from '$app/forms';
	import ProductEditorFields from '$lib/components/admin/ProductEditorFields.svelte';
	import PageContainer from '$lib/components/shared/PageContainer.svelte';
	import StatusBadge from '$lib/components/shared/StatusBadge.svelte';
	import Toast from '$lib/components/shared/Toast.svelte';
	import { waitForMinimumDuration } from '$lib/utils/minimumDuration';
	import { useDismissToast, useToast } from '$lib/state/toast';

	interface Props {
		data: PageData;
	}

	let { data }: Props = $props();
	const productColumns = [
		{ label: '' },
		{ label: 'Title', sortValue: (product: ProductOut) => product.title },
		{ label: 'Price', sortValue: (product: ProductOut) => Number(product.price) },
		{ label: 'Height', sortValue: (product: ProductOut) => product.height },
		{ label: 'Width', sortValue: (product: ProductOut) => product.width },
		{ label: 'Medium', sortValue: (product: ProductOut) => product.medium?.name },
		{ label: 'Enabled', sortValue: (product: ProductOut) => product.enabled },
		{ label: 'Actions' }
	];

	let showModal: boolean = $state(false);
	let loadingModal: boolean = $state(false);
	let isUpdating: boolean = $state(false);
	let modalMode: 'create' | 'update' = $state('update');
	let selectedProduct: ProductOut = $state(createEmptyProduct());
	let files: File[] = $state([]);
	let formToast: { id: number; title: string; message: string } | null = $state(null);
	let formToastVisible = $state(false);
	let nextFormToastId = 0;
	const showToast = useToast();
	const dismissToast = useDismissToast();

	function showFormError(title: string, message: string) {
		formToast = { id: ++nextFormToastId, title, message };
		formToastVisible = true;
		showToast({ type: 'error', title, message });
	}

	$effect(() => {
		if (formToast && !formToastVisible) dismissToast();
	});

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
			sold: false,
			images: [],
			medium: null
		};
	}

	function openCreateModal() {
		modalMode = 'create';
		selectedProduct = createEmptyProduct();
		files = [];
		loadingModal = false;
		formToast = null;
		showModal = true;
	}

	async function openEditModal(product: ProductOut) {
		modalMode = 'update';
		files = [];
		formToast = null;
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

<PageContainer max="100%">
	<Card width="100%">
		<div class="section-header">
			<h1>Products</h1>
			<Button style={ButtonStyle.Info} onclick={openCreateModal}>
				<div>Add New Product</div>
				<Icon icon="material-symbols:add-rounded" />
			</Button>
		</div>
		{#await data.products}
			<Skeleton />
		{:then products}
			<Table label="Products" minWidth="64rem" rows={products} columns={productColumns} emptyMessage="No products found.">
				{#snippet row(product)}
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
							<StatusBadge tone={product.enabled ? 'success' : 'error'}>
								<Icon icon={product.enabled ? 'material-symbols:check-rounded' : 'material-symbols:close-rounded'} width={16} height={16} />
								{product.enabled ? 'Enabled' : 'Disabled'}
							</StatusBadge>
						</td>
						<td>
							<div class="actions">
								<Button style={ButtonStyle.Info} onclick={async () => await openEditModal(product)}>
									<div>Edit</div>
									<Icon icon="material-symbols:edit-rounded" width={16} height={16} />
								</Button>
								<form
									method="POST"
									action="?/delete"
									class="delete-form"
									use:enhance={() => {
										const title = product.title;
										return async ({ result, update }) => {
											if (result.type === 'success') {
												try {
													await update();
													showToast({ type: 'success', title: 'Product deleted', message: `"${title}" was deleted.` });
												} catch (error) {
													console.error('Product list refresh failed:', error);
													showToast({ type: 'warning', title: 'Product deleted', message: 'The product list could not be refreshed.' });
												}
											} else {
												showToast({ type: 'error', title: 'Product not deleted', message: 'Unable to delete product. Please try again.' });
											}
										};
									}}
								>
									<input type="hidden" name="id" value={product.id} />
									<Button type="submit" style={ButtonStyle.Cancel}>
										<div>Delete</div>
										<Icon icon="material-symbols:delete-rounded" width={16} height={16} />
									</Button>
								</form>
							</div>
						</td>
					</tr>
				{/snippet}
			</Table>
		{:catch error}
			<div>Something went wrong: {error.message}</div>
		{/await}
	</Card>
</PageContainer>

{#if showModal}
	<Modal
		bind:showModal
		busy={isUpdating}
		busyLabel="Updating product…"
		placement="top"
		title={modalMode === 'create' ? 'Add New Product' : 'Edit Product'}
	>
		{#if loadingModal}
			<div>loading product...</div>
		{:else}
			{#if formToast}
				<div class="form-toast">
					{#key formToast.id}
						<Toast bind:showToast={formToastVisible} type="error" title={formToast.title} message={formToast.message} />
					{/key}
				</div>
			{/if}
			<form 
				method="POST" 
				action={modalMode === 'create' ? '?/create' : '?/update'}
				enctype="multipart/form-data" 
				class="form-stack edit" 
				use:enhance={({ formData, cancel }) => {
					const updating = modalMode === 'update';
					if (updating && isUpdating) {
						cancel();
						return;
					}

					// Remove the empty <input type="file"> contents
					formData.delete('medium');
					formData.delete('images');

					// Attach every NEW image in the right order
					files.forEach((item) => {
						if (item instanceof File) {
							formData.append('images', item, item.name);
						}
					});

					const busyStartedAt = updating ? performance.now() : 0;
					if (updating) {
						isUpdating = true;
					}

					return async ({ result, update }) => {
						if (!updating) {
							if (result.type === 'success') {
								try {
									await update();
									showModal = false;
									showToast({ type: 'success', title: 'Product added', message: 'The product was added.' });
								} catch (error) {
									console.error('Product list refresh failed:', error);
									showModal = false;
									showToast({ type: 'warning', title: 'Product added', message: 'The product list could not be refreshed.' });
								}
							} else {
								showFormError('Product not added', result.type === 'failure'
									? 'Please review the product details and try again.'
									: 'Unable to add product. Please try again.');
							}
							return;
						}

						let updateSucceeded = false;
						let refreshFailed = false;
						let failureMessage = 'Unable to update product. Please try again.';
						try {
							if (result.type === 'success') {
								await update();
								updateSucceeded = true;
							} else if (result.type === 'failure') {
								failureMessage = 'Please review the product details and try again.';
							}
						} catch (error) {
							console.error('Product update failed:', error);
							if (result.type === 'success') {
								updateSucceeded = true;
								refreshFailed = true;
							}
						} finally {
							await waitForMinimumDuration(busyStartedAt);
							isUpdating = false;
							if (updateSucceeded) {
								showModal = false;
								showToast(refreshFailed
									? { type: 'warning', title: 'Product updated', message: 'The product list could not be refreshed.' }
									: { type: 'success', title: 'Product updated', message: 'The product was updated.' });
							} else {
								showFormError('Product not updated', failureMessage);
							}
						}
					}
				}}
			>
				{#if modalMode === 'update'}
					<input type="hidden" id="id" name="id" value={selectedProduct.id} />
				{/if}
				<ProductEditorFields bind:product={selectedProduct} bind:files />

				<div class="form-actions">
					<Button type="submit">
						{modalMode === 'create' ? 'Add Product' : 'Update Product'}
					</Button>
					<Button type="button" style={ButtonStyle.Cancel} onclick={() => showModal = false}>
						Cancel
					</Button>
				</div>
			</form>
		{/if}
	</Modal>
{/if}

<style>
	.thumbnail {
		display: flex;
	}

	.actions {
		display: flex;
		align-items: center;
		gap: 0.5rem;
	}

	.delete-form {
		display: inline-block;
	}

	.edit {
		max-inline-size: 35em;
	}

	.form-toast {
		inline-size: min(100%, 35em);
		margin-block-end: 1rem;
	}

</style>
