<script lang="ts">
	import type { ProductImageOut } from '$lib/interfaces/ProductOut';
	import Skeleton from '$lib/components/shared/Skeleton.svelte';
	import Button from '$lib/components/shared/Button.svelte';
	import Icon from '@iconify/svelte';
	import { onMount } from 'svelte';
	import type { Action } from 'svelte/action';

	interface Props {
		previews: ProductImageOut[];
		files: File[];
	}

	let { previews, files = $bindable() }: Props = $props();

	let initialFileHashes: string[] = $state([]);
	let fileHashes: string[] = $state([]);
	let filesChanged: boolean = $derived(!areEqual(initialFileHashes, fileHashes));
	let previewError: string | null = $state(null);
	let loadingPreviews: boolean = $state(previews.length > 0);
	let draggedIndex: number | null = $state(null);
	let hoverIndex: number | null = $state(null);

	const thumbnailTitle = 'This image will be used as the product thumbnail';

	async function hashFile(file: File): Promise<string> {
		const arrayBuffer = await file.arrayBuffer();
		const hashBuffer = await crypto.subtle.digest('SHA-256', arrayBuffer);
		const hashArray = Array.from(new Uint8Array(hashBuffer));
		return hashArray.map((b) => b.toString(16).padStart(2, '0')).join('');
	}

	const previewFile: Action<HTMLImageElement, File> = (node, file) => {
		let url = URL.createObjectURL(file);
		node.src = url;

		return {
			update(nextFile) {
				URL.revokeObjectURL(url);
				url = URL.createObjectURL(nextFile);
				node.src = url;
			},
			destroy() {
				URL.revokeObjectURL(url);
			}
		};
	};

	function handleDragStart(index: number) {
		draggedIndex = index;
		hoverIndex = index;
	}

	function handleDragEnter(targetIndex: number) {
		if (draggedIndex === null || targetIndex === hoverIndex) return;

		const reordered = [...files];
		const reorderedHashes = [...fileHashes];
		const [moved] = reordered.splice(draggedIndex, 1);
		const [movedHash] = reorderedHashes.splice(draggedIndex, 1);
		reordered.splice(targetIndex, 0, moved);
		reorderedHashes.splice(targetIndex, 0, movedHash);

		files = reordered;
		fileHashes = reorderedHashes;
		draggedIndex = targetIndex; // update drag position
		hoverIndex = targetIndex;
	}

	function handleDragEnd() {
		draggedIndex = null;
		hoverIndex = null;
	}

	function handleDragover(event: DragEvent) {
		event.preventDefault();
	}

	// Triggered when images are dropped into the dropzone
	async function handleDrop(event: DragEvent) {
		event.preventDefault();

		if (!event.dataTransfer) return;

		const droppedFiles = Array.from(event.dataTransfer.files).filter((file) =>
			file.type.startsWith('image/')
		);

		const uniqueNewFiles: File[] = [];

		for (const file of droppedFiles) {
			const hash = await hashFile(file);
			if (!fileHashes.includes(hash)) {
				fileHashes = [...fileHashes, hash];
				uniqueNewFiles.push(file);
			}
		}

		if (uniqueNewFiles.length > 0) {
			files = [...files, ...uniqueNewFiles];
		}
	}

	function handleKeyDown(event: KeyboardEvent, index: number) {
		if (event.key === 'ArrowLeft' && index > 0) {
			event.preventDefault();
			const reordered = [...files];
			const reorderedHashes = [...fileHashes];
			const [moved] = reordered.splice(index, 1);
			const [movedHash] = reorderedHashes.splice(index, 1);
			reordered.splice(index - 1, 0, moved);
			reorderedHashes.splice(index - 1, 0, movedHash);
			files = reordered;
			fileHashes = reorderedHashes;
			setTimeout(() => focusImage(index - 1), 0);
		} else if (event.key === 'ArrowRight' && index < files.length - 1) {
			event.preventDefault();
			const reordered = [...files];
			const reorderedHashes = [...fileHashes];
			const [moved] = reordered.splice(index, 1);
			const [movedHash] = reorderedHashes.splice(index, 1);
			reordered.splice(index + 1, 0, moved);
			reorderedHashes.splice(index + 1, 0, movedHash);
			files = reordered;
			fileHashes = reorderedHashes;
			setTimeout(() => focusImage(index + 1), 0);
		}
	}

	function focusImage(index: number) {
		const elements = document.querySelectorAll('.image-wrapper');
		(elements[index] as HTMLElement)?.focus();
	}

	// Triggered when images are selected through file input
	async function handleSelect(event: Event) {
		const target = event.target as HTMLInputElement;
		const selectedFiles = target.files ? Array.from(target.files) : [];
		const uniqueNewFiles: File[] = [];
		for (const file of selectedFiles.filter((item) => item.type.startsWith('image/'))) {
			const hash = await hashFile(file);
			if (!fileHashes.includes(hash)) {
				fileHashes = [...fileHashes, hash];
				uniqueNewFiles.push(file);
			}
		}
		files = [...files, ...uniqueNewFiles];
		target.value = '';
	}

	// Removes a selected image from the list
	function removeImage(index: number, event: MouseEvent) {
		event.stopPropagation(); // Prevents triggering the dropzone click event
		files = files.filter((_, i) => i !== index);
		fileHashes = fileHashes.filter((_, i) => i !== index);
	}

	async function createFileFromImage(productImage: ProductImageOut) {
		const imageUrl = new URL(productImage.url);
		const filename = decodeURIComponent(
			imageUrl.pathname.split('/').pop() || `image-${productImage.id}`
		);
		const response = await fetch(productImage.url);
		if (!response.ok) throw new Error(`Unable to load image: ${filename}`);
		const blob = await response.blob();
		return new File([blob], filename, { type: blob.type });
	}

	function areEqual<T>(arrayA: T[], arrayB: T[]): boolean {
		if (arrayA.length !== arrayB.length) {
			return false;
		}

		for (let i = 0; i < arrayA.length; i++) {
			if (arrayA[i] !== arrayB[i]) {
				return false;
			}
		}

		return true;
	}

	let fileInput: HTMLInputElement = $state()!;

	onMount(async () => {
		if (previews.length > 0) {
			try {
				const resolvedFiles = await Promise.all(previews.map(createFileFromImage));
				const resolvedHashes = await Promise.all(resolvedFiles.map(hashFile));
				files = resolvedFiles;
				fileHashes = resolvedHashes;
				initialFileHashes = [...resolvedHashes];
			} catch (error) {
				console.error(error);
				previewError = 'Existing images could not be loaded. Please try again.';
			} finally {
				loadingPreviews = false;
			}
		}
	});
</script>

<div
	class="dropzone"
	role="button"
	aria-label="Image upload dropzone. Click or press Enter to upload images."
	tabindex="0"
	ondragover={handleDragover}
	ondrop={handleDrop}
	onclick={() => fileInput.click()}
	onkeydown={(e) => e.key === 'Enter' && fileInput.click()}
>
	<div class="instructions">
		<Icon icon="material-symbols:upload-rounded" />
		<div>Drag & drop images here, or click to select</div>
		<div>Move images to reorder</div>
	</div>
	{#if previewError}
		<p class="preview-error" role="alert">{previewError}</p>
	{/if}
	<input type="hidden" id="filesChanged" name="filesChanged" bind:value={filesChanged} />
	<input
		id="images"
		class="file-input"
		name="images"
		type="file"
		accept="image/*"
		multiple
		bind:this={fileInput}
		onchange={handleSelect}
	/>
	<div class="image-preview">
		{#if loadingPreviews}
			<span class="sr-only" role="status">Loading existing images…</span>
			{#each previews as preview (preview.id)}
				<div class="image-wrapper placeholder" aria-hidden="true">
					<Skeleton />
				</div>
			{/each}
		{/if}
		{#each files as file, index}
			<div
				class="image-wrapper
					{index === 0 ? 'thumbnail' : ''} 
					{index === draggedIndex ? 'dragged' : ''} 
					{index === hoverIndex ? 'hovered' : ''}"
				role="button"
				aria-label="Use arrow keys to reorder."
				aria-pressed={index === 0}
				tabindex="0"
				draggable="true"
				ondragstart={() => handleDragStart(index)}
				ondragenter={() => handleDragEnter(index)}
				ondragend={handleDragEnd}
				onkeydown={(e) => handleKeyDown(e, index)}
			>
				<img
					use:previewFile={file}
					class="image"
					title={index === 0 ? thumbnailTitle : file.name}
					alt={file.name}
				/>
				{#if index === 0}
					<span class="thumbnail-indicator" title={thumbnailTitle}>Thumbnail</span>
				{/if}
				<Button
					type="button"
					class="remove-btn"
					appearance="plain"
					aria-label="Remove image"
					title="Remove image"
					onclick={(e) => removeImage(index, e)}
				>
					&times;
				</Button>
			</div>
		{/each}
	</div>
</div>

<style>
	.file-input { display: none; }
	.dropzone {
		border: 2px dashed var(--border);
		padding: 20px;
		display: flex;
		flex-direction: column;
		align-items: center;
		cursor: pointer;
		transition: background-color 0.2s var(--ease-out);
	}

	.dropzone:active { background-color: var(--surface-muted); }
	@media (hover: hover) and (pointer: fine) { .dropzone:hover { background-color: var(--surface-muted); } }

	.instructions {
		display: flex;
		flex-direction: column;
		align-items: center;
	}

	.preview-error {
		color: var(--danger);
	}

	.image-preview {
		display: flex;
		flex-wrap: wrap;
		margin-block-start: 10px;
		justify-content: center;
	}

	.image-wrapper {
		position: relative;
		inline-size: 150px;
		block-size: 150px;
		margin: 5px;
		cursor: grab;
		border: 2px solid transparent;
		border-radius: 8px;
		overflow: clip;
		transition: border-color 150ms var(--ease-out);
	}

	.sr-only {
		position: absolute;
		width: 1px;
		height: 1px;
		padding: 0;
		margin: -1px;
		overflow: hidden;
		clip: rect(0, 0, 0, 0);
		white-space: nowrap;
		border: 0;
	}

	.placeholder {
		cursor: default;
	}

	.image-wrapper.dragged {
		opacity: 0.6;
		transform: scale(0.95);
		cursor: grabbing;
	}
	.image-wrapper:active { border-color: var(--link); }

	.image-wrapper.hovered {
		border-color: var(--link);
		box-shadow: 0 0 0 2px var(--link);
	}

	.image-wrapper img.image {
		inline-size: 100%;
		block-size: 100%;
		object-fit: cover;
	}

	.image {
		inline-size: 150px;
		block-size: 150px;
		object-fit: cover;
	}

	:global(button.remove-btn) {
		position: absolute;
		inset-block-start: 5px;
		inset-inline-end: 5px;
		background: color-mix(in oklch, var(--surface) 70%, transparent);
		border: none;
		border-radius: 50%;
		cursor: pointer;
		transition: background-color 0.2s var(--ease-out);
	}

	:global(button.remove-btn:active) { background: var(--danger); color: var(--surface); }
	@media (hover: hover) and (pointer: fine) {
		:global(button.remove-btn:hover) { background: color-mix(in oklch, var(--danger) 80%, transparent); color: var(--surface); }
	}
	@media (prefers-reduced-motion: no-preference) {
		.image-wrapper { transition: transform 150ms var(--ease-out), border-color 150ms var(--ease-out); }
		:global(button.remove-btn) { transition: transform 150ms var(--ease-out), background-color 150ms var(--ease-out); }
	}

	.thumbnail-indicator {
		position: absolute;
		inset-block-end: 0;
		inset-inline-start: 0;
		background: color-mix(in oklch, var(--success) 60%, transparent);
		color: var(--surface);
		padding: 2px 5px;
		font-size: 0.8em;
	}

	.image-wrapper.thumbnail {
		border: 2px solid var(--success);
	}
</style>
