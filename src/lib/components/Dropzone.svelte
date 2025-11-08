<script lang="ts">
	import type { ProductImageOut } from '$lib/interfaces/ProductOut';
	import Icon from '@iconify/svelte';
	import { onMount } from 'svelte';

	interface Props {
		previews: ProductImageOut[];
		files: File[];
	}

	let { 
		previews,
		files = $bindable()
	}: Props = $props();

	let initialFileHashes: Set<string> = $state(new Set());
	let fileHashes: Set<string> = $state(new Set());
	let filesChanged: boolean = $derived(!areEqual(initialFileHashes, fileHashes));
	let draggedIndex: number | null = $state(null);
	let hoverIndex: number | null = $state(null);

	const thumbnailTitle = "This image will be used as the product thumbnail";

	async function hashFile(file: File): Promise<string> {
		const arrayBuffer = await file.arrayBuffer();
		const hashBuffer = await crypto.subtle.digest('SHA-256', arrayBuffer);
		const hashArray = Array.from(new Uint8Array(hashBuffer));
		return hashArray.map(b => b.toString(16).padStart(2, '0')).join('');
	}

	function handleDragStart(index: number) {
		draggedIndex = index;
		hoverIndex = index;
	}

	function handleDragEnter(targetIndex: number) {
		if (draggedIndex === null || targetIndex === hoverIndex) return;

		const reordered = [...files];
		const [moved] = reordered.splice(draggedIndex, 1);
		reordered.splice(targetIndex, 0, moved);

		files = reordered;
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
			if (!fileHashes.has(hash)) {
				fileHashes = new Set(fileHashes).add(hash);
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
			const [moved] = reordered.splice(index, 1);
			reordered.splice(index - 1, 0, moved);
			files = reordered;
			setTimeout(() => focusImage(index - 1), 0);
		} else if (event.key === 'ArrowRight' && index < files.length - 1) {
			event.preventDefault();
			const reordered = [...files];
			const [moved] = reordered.splice(index, 1);
			reordered.splice(index + 1, 0, moved);
			files = reordered;
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
		const newFiles = selectedFiles.filter((file) => file.type.startsWith('image/'));
		for (const file of newFiles) {
			const hash = await hashFile(file);
			if (!fileHashes.has(hash)) {
				fileHashes = new Set(fileHashes).add(hash);
			}
		}
		files = [...files, ...newFiles];
	}

	// Removes a selected image from the list
	function removeImage(index: number, event: MouseEvent) {
		event.stopPropagation(); // Prevents triggering the dropzone click event
		files = files.filter((_, i) => i !== index);
	}

	async function createFileFromImage(productImage: ProductImageOut) {
		const filename = productImage.publicId;
		const response = await fetch(`../api/proxy/${productImage.publicId}`);
		const blob = await response.blob();
		const file = new File([blob], filename as string, { type: blob.type });
		return file;
	}

	function areEqual<T>(setA: Set<T>, setB: Set<T>): boolean {
		const arrA = Array.from(setA);
        const arrB = Array.from(setB);

        if (arrA.length !== arrB.length) {
            return false;
        }

        for (let i = 0; i < arrA.length; i++) {
            if (arrA[i] !== arrB[i]) {
                return false;
            }
        }

        return true;
	}

	let fileInput: HTMLInputElement = $state()!;

	onMount(async () => {
		if (previews.length > 0) {
			const resolvedFiles = await Promise.all(previews.map(createFileFromImage));
			files = resolvedFiles;
			for (const file of resolvedFiles) {
				const hash = await hashFile(file);
				if (!fileHashes.has(hash)) {
					fileHashes = new Set(fileHashes).add(hash);
					initialFileHashes = new Set(initialFileHashes).add(hash);
				}
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
		<div>
			Drag & drop images here, or click to select
		</div>
		<div>
			Move images to reorder
		</div>
	</div>
	<input type="hidden" id="filesChanged" name="filesChanged" bind:value={filesChanged} />
	<input
		id="images"
		name="images"
		type="file"
		accept="image/*"
		multiple
		bind:this={fileInput}
		onchange={handleSelect}
		style="display: none;"
	/>
	<div class="image-preview">
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
				<img class="image" title={index === 0 ? thumbnailTitle : file.name} src={URL.createObjectURL(file)} alt={file.name} />
				{#if index === 0}
					<span class="thumbnail-indicator" title={thumbnailTitle}>Thumbnail</span>
				{/if}
				<button
					class="remove-btn" 
					aria-label="Remove image" 
					title="Remove image"
					onclick={(e) => removeImage(index, e)}
				>
					&times;
				</button>
			</div>
		{/each}
	</div>
</div>

<style>
	.dropzone {
		border: 2px dashed #ccc;
		padding: 20px;
		display: flex;
		flex-direction: column;
		align-items: center;
		cursor: pointer;
		transition: background-color 0.2s;
	}

	.dropzone:hover {
		background-color: #f0f0f0;
	}

	.instructions {
		display: flex;
		flex-direction: column;
		align-items: center;
	}

	.image-preview {
		display: flex;
		flex-wrap: wrap;
		margin-top: 10px;
		justify-content: center;
	}

	.image-wrapper {
		position: relative;
		width: 150px;
		height: 150px;
		margin: 5px;
		cursor: grab;
		border: 2px solid transparent;
		border-radius: 8px;
		overflow: hidden;
		transition: transform 150ms ease, border-color 150ms ease;
	}

	.image-wrapper.dragged {
		opacity: 0.6;
		transform: scale(0.95);
		cursor: grabbing;
	}

	.image-wrapper.hovered {
		border-color: var(--accent, #0070f3);
		box-shadow: 0 0 0 2px var(--accent, #0070f3);
	}

	.image-wrapper img.image {
		width: 100%;
		height: 100%;
		object-fit: cover;
	}

	.image {
		width: 150px;
		height: 150px;
		object-fit: cover;
	}

	.remove-btn {
		position: absolute;
		top: 5px;
		right: 5px;
		background: rgba(255, 255, 255, 0.7);
		border: none;
		border-radius: 50%;
		cursor: pointer;
		transition:
			transform 0.2s ease,
			background-color 0.2s ease;
	}

	.remove-btn:hover {
		transform: scale(1.2);
		background-color: rgba(255, 0, 0, 0.8);
		color: white;
	}

	.thumbnail-indicator {
		position: absolute;
		bottom: 0;
		left: 0;
		background: rgba(0, 128, 0, 0.6);
		color: white;
		padding: 2px 5px;
		font-size: 0.8em;
	}

	.image-wrapper.thumbnail {
		border: 2px solid green;
	}
</style>
