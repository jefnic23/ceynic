<script lang="ts">
	import type { ProductImageOut, ProductOut } from "$lib/interfaces/ProductOut";
	import { CldImage } from "svelte-cloudinary";
	import { quintOut } from "svelte/easing";
	import { crossfade } from "svelte/transition";
	import Modal from "$lib/components/shared/Modal.svelte";
	import { onMount } from "svelte";
	import ArrowLeft from "$lib/icons/ArrowLeft.svelte";
	import ArrowRight from "$lib/icons/ArrowRight.svelte";

    interface Props {
		product: ProductOut;
        url: URL;
	}

	let { product, url }: Props = $props();

    let selectedIndex: number = $state(0);
    let selectedImage: ProductImageOut | undefined = $derived(product.images?.[selectedIndex]);

    let modalIndex: number | null = $state(null);
    let modalImage: ProductImageOut | null | undefined = $derived(modalIndex !== null ? product.images?.[modalIndex] : null);

    const [send, receive] = crossfade({
		duration: 377,
		easing: quintOut
	});

    let showModal: boolean = $state(false);

    function goToPrevious() {
        if (modalIndex !== null) {
            modalIndex = (modalIndex - 1 + (product.images?.length as number)) % (product.images?.length as number);
        }
    }

    function goToNext() {
        if (modalIndex !== null) {
            modalIndex = (modalIndex + 1) % (product.images?.length as number);
        }
    }

    function handleKeydown(event: KeyboardEvent) {
		if (!showModal || modalIndex === null) return;

		if (event.key === 'ArrowRight') {
			goToNext();
		} else if (event.key === 'ArrowLeft') {
			goToPrevious();
		}
	}

	onMount(() => {
		window.addEventListener('keydown', handleKeydown);
		return () => window.removeEventListener('keydown', handleKeydown);
	});
</script>

<div class="images">
    {#if (product.images as ProductImageOut[]).length > 1}
        <ul>
            {#each (product.images as ProductImageOut[]) as image, i}
                <li 
                    onclick={() => (selectedIndex = i)}
                    class:selected={i === selectedIndex}
                >
                    <CldImage 
                        src={image.publicId} 
                        alt={image.publicId}
                        width={60}
                        height={60}
                        radius={8}
                        data-pin-nopin="true"
                    />
                </li>
            {/each}
        </ul>
    {/if}
    <div class="image" onclick={() => (modalIndex = selectedIndex, showModal = true)}>
        {#key selectedImage?.publicId}
            <div in:receive={{ key: selectedImage?.publicId }} out:send={{ key: selectedImage?.publicId }}>
                <CldImage 
                    src={selectedImage?.publicId || ""} 
                    alt={product.title}
                    width={600}
                    height={600}
                    sizes="(max-width: 768px) 100vw, 50vw"
                    data-pin-do="buttonPin"
                    data-pin-url={url}
                    data-pin-description={product.title}
                />
            </div>
        {/key}
    </div>
</div>

{#if showModal && modalImage}
	<Modal bind:showModal={showModal}>
        <div class="modal-image">
            <button class="arrow left" onclick={goToPrevious} aria-label="Previous image"><ArrowLeft /></button>

            <CldImage
                src={modalImage?.publicId || ""} 
                alt={product.title}
                width={960}
                height={960}
                data-pin-nopin="true"
            />

            <button class="arrow right" onclick={goToNext} aria-label="Next image"><ArrowRight /></button>
        </div>
	</Modal>
{/if}

<style>
    .images {
		display: flex;
		flex-direction: row;
		flex: 5;
		padding: 1rem;
        column-gap: 1rem;
	}

	ul {
		list-style: none;
		padding: 0;
        margin: 0;
	}

	li {
		width: 60px;
		height: 60px;
        margin: 8px 0;
        cursor: pointer;
        transition: outline 0.08s ease-in-out;
	}

    li.selected {
		outline: 2px solid #0070f3; /* or your brand color */
		border-radius: 8px;
	}

    .image {
        position: relative;
        width: 600px;
        height: 600px;
        cursor: sw-resize;
    }

    .image > div {
        position: absolute;
        width: 100%;
        height: 100%;
    }

    .modal-image {
		position: relative;
		display: flex;
		align-items: center;
		justify-content: center;
	}

	.arrow {
		position: absolute;
		top: 50%;
		transform: translateY(-50%);
		background: rgba(0, 0, 0, 0.5);
		color: white;
		border: none;
		font-size: 2rem;
		padding: 0.5rem 1rem;
		cursor: pointer;
		border-radius: 6px;
		transition: background 0.2s;
		z-index: 10;
	}

	.arrow:hover {
		background: rgba(0, 0, 0, 0.7);
	}

	.arrow.left {
		left: 1rem;
	}

	.arrow.right {
		right: 1rem;
	}

    @media only screen and (max-width: 1144px) {
		.images {
            flex-direction: column-reverse;
            row-gap: 1rem;
            align-items: center;
        }

        li {
            float: left;
            margin: 0 8px;
        }
	}
</style>