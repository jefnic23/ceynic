<script lang="ts">
	import type { ProductImageOut, ProductOut } from "$lib/interfaces/ProductOut";
	import ProductImage from '$lib/components/ProductImage.svelte';
	import { quintOut } from "svelte/easing";
	import { crossfade } from "svelte/transition";
	import Modal from "$lib/components/shared/Modal.svelte";
	import { onMount } from "svelte";
	import Icon from "@iconify/svelte";
	import { page } from "$app/state";

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

    let touchStartX: number | null = $state(null);
    let touchEndX: number | null = $state(null);

    function handleTouchStart(event: TouchEvent) {
        touchStartX = event.changedTouches[0].clientX;
    }

    function handleTouchEnd(event: TouchEvent) {
        touchEndX = event.changedTouches[0].clientX;

        if (touchStartX === null || touchEndX === null) return;

        const deltaX = touchEndX - touchStartX;

        if (Math.abs(deltaX) < 50) return;

        if (deltaX > 0) {
            goToPrevious();
        } else {
            goToNext();
        }

        touchStartX = null;
        touchEndX = null;
    }

    function handleThumbnail(index: number) {
        selectedIndex = index;
    }

	onMount(() => {
        const hash = page.url.hash;
        const index = hash ? parseInt(hash.substring(1)) : 0;
        if (!isNaN(index) && index >= 0 && index < (product.images as ProductImageOut[]).length) {
			selectedIndex = index;
		}

		window.addEventListener('keydown', handleKeydown);
		return () => window.removeEventListener('keydown', handleKeydown);
	});
</script>

<div class="images">
    {#if (product.images as ProductImageOut[]).length > 1}
        <ul>
            {#each (product.images as ProductImageOut[]) as image, i}
                <li class:selected={i === selectedIndex}>
                    <a href="#{i}" onclick={() => handleThumbnail(i)}>
                        <ProductImage
							url={image.url}
                            alt={product.title}
                            width={60}
                            height={60}
                            rounded
							crop
                            data-pin-nopin="true"
                        />
                    </a>
                </li>
            {/each}
        </ul>
    {/if}
    <div 
        class="image" 
        onclick={() => (modalIndex = selectedIndex, showModal = true)} 
        onkeydown={(e) => { 
            if (e.key !== "Enter" && e.key !== " ") return; 
            e.preventDefault();
            (e.target as HTMLElement).click();
        }} 
        role="button" 
        tabindex="0" 
        aria-pressed="false"
    >
        {#key selectedImage?.url}
            <div 
				in:receive={{ key: selectedImage?.url }}
				out:send={{ key: selectedImage?.url }}
            >
                <ProductImage
					url={selectedImage?.url}
                    alt={product.title}
                    width={selectedImage?.width}
                    height={selectedImage?.height}
					style="width: 100%; height: 100%; object-fit: contain;"
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
        <div class="modal-image" ontouchstart={handleTouchStart} ontouchend={handleTouchEnd}>
            <button class="arrow left" onclick={goToPrevious} aria-label="Previous image">
                <Icon icon="material-symbols:arrow-back-ios-rounded" width={32} height={32} />
            </button>

            <ProductImage
				url={modalImage.url}
                alt={product.title}
                width={modalImage.width}
                height={modalImage.height}
				style="width: 100%; height: 100%; object-fit: contain;"
                data-pin-nopin="true"
            />

            <button class="arrow right" onclick={goToNext} aria-label="Next image">
                <Icon icon="material-symbols:arrow-forward-ios-rounded" width={32} height={32} />
            </button>
        </div>
    </Modal>
{/if}

<style>
	.images {
		display: flex;
		flex-direction: row;
		flex: 5;
		min-width: 0;
		padding: 1rem;
        column-gap: 1rem;
	}

	ul {
		list-style: none;
		padding: 0;
        margin: 0;
		flex-shrink: 0;
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

	li a {
		display: block;
		width: 100%;
		height: 100%;
	}

    .image  {
        display: grid;
		flex: 1;
		width: 100%;
		min-width: 0;
		aspect-ratio: 1;
		max-height: 75dvh;
        cursor: sw-resize;
    }

    .image > div {
        grid-area: 1 / 1;
		display: flex;
		justify-content: center;
		align-items: center;
		width: 100%;
		height: 100%;
		min-width: 0;
		min-height: 0;
    }

    .modal-image {
		position: relative;
		display: flex;
		align-items: center;
		justify-content: center;
		width: min(calc(100vw - 4rem), calc(100dvh - 8rem), 46em);
		aspect-ratio: 1;
	}

	.arrow {
		position: absolute;
		top: 50%;
		transform: translateY(-50%);
		background: none;
		color: black;
		border: none;
		font-size: 2rem;
		padding: 0.5rem 1rem;
		cursor: pointer;
		border-radius: 6px;
		transition: background 0.2s;
		z-index: 10;
	}

	/* .arrow:hover {
		background: rgba(0, 0, 0, 0.7);
	} */

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
