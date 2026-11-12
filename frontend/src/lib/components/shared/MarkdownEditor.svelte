<script lang="ts">
	import { onMount } from 'svelte';
	import type { CrepeBuilder } from '@milkdown/crepe/builder';

	import '@milkdown/crepe/theme/common/prosemirror.css';
	import '@milkdown/crepe/theme/common/reset.css';
	import '@milkdown/crepe/theme/common/block-edit.css';
	import '@milkdown/crepe/theme/common/code-mirror.css';
	import '@milkdown/crepe/theme/common/cursor.css';
	import '@milkdown/crepe/theme/common/image-block.css';
	import '@milkdown/crepe/theme/common/link-tooltip.css';
	import '@milkdown/crepe/theme/common/list-item.css';
	import '@milkdown/crepe/theme/common/placeholder.css';
	import '@milkdown/crepe/theme/common/table.css';
	import '@milkdown/crepe/theme/common/toolbar.css';
	import '@milkdown/crepe/theme/common/top-bar.css';
	import '@milkdown/crepe/theme/classic.css';

	interface Props {
		id: string;
		name: string;
		label: string;
		placeholder: string;
		value: string;
		maxLength?: number;
	}

	let { id, name, label, placeholder, maxLength, value = $bindable() }: Props = $props();
	let editorRoot: HTMLDivElement;
	let crepe: CrepeBuilder | undefined;
	let ready = $state(false);
	let editorError = $state(false);
	let imageUploadWarning = $state('');

	onMount(() => {
		let active = true;
		let instance: CrepeBuilder | undefined;

		async function initialize() {
			try {
				const [
					{ CrepeBuilder },
					{ blockEdit },
					{ codeMirror },
					{ cursor },
					{ imageBlock },
					{ linkTooltip },
					{ listItem },
					{ placeholder: placeholderFeature },
					{ table },
					{ toolbar },
					{ topBar }
				] = await Promise.all([
					import('@milkdown/crepe/builder'),
					import('@milkdown/crepe/feature/block-edit'),
					import('@milkdown/crepe/feature/code-mirror'),
					import('@milkdown/crepe/feature/cursor'),
					import('@milkdown/crepe/feature/image-block'),
					import('@milkdown/crepe/feature/link-tooltip'),
					import('@milkdown/crepe/feature/list-item'),
					import('@milkdown/crepe/feature/placeholder'),
					import('@milkdown/crepe/feature/table'),
					import('@milkdown/crepe/feature/toolbar'),
					import('@milkdown/crepe/feature/top-bar')
				]);

				if (!active) return;
				instance = new CrepeBuilder({ root: editorRoot, defaultValue: value })
					.addFeature(blockEdit)
					.addFeature(codeMirror)
					.addFeature(cursor)
					.addFeature(imageBlock, {
						blockUploadButton: 'Uploads unavailable',
						blockUploadPlaceholderText: 'or paste an image URL',
						inlineUploadButton: 'Uploads unavailable',
						inlineUploadPlaceholderText: 'or paste an image URL',
						onUpload: async () => {
							imageUploadWarning = 'Image uploads are not supported. Use an image URL instead.';
							throw new Error('Image file uploads are not supported.');
						}
					})
					.addFeature(linkTooltip)
					.addFeature(listItem)
					.addFeature(placeholderFeature, {
						text: placeholder,
						mode: 'block'
					})
					.addFeature(table)
					.addFeature(toolbar)
					.addFeature(topBar);

				instance.on((listener) => {
					listener.markdownUpdated((_ctx, markdown) => {
						if (ready) value = markdown;
					});
				});

				await instance.create();
				if (!active) {
					await instance.destroy();
					return;
				}

				crepe = instance;
				editorRoot.querySelector('[contenteditable="true"]')?.setAttribute('aria-label', label);
				value = instance.getMarkdown();
				ready = true;
			} catch {
				if (active) editorError = true;
				if (instance) await instance.destroy().catch(() => {});
			}
		}

		void initialize();
		return () => {
			active = false;
			if (crepe) void crepe.destroy();
		};
	});
</script>

<div class="markdown-editor">
	<span id="{id}-label" class="editor-label">{label}</span>

	{#if !ready}
		<p class="editor-status" role="status">
			{editorError
				? 'The visual editor could not load. You can still edit and save using the text field below.'
				: 'Loading the visual editor.'}
		</p>
	{/if}

	{#if imageUploadWarning}
		<p class="editor-status" role="status">{imageUploadWarning}</p>
	{/if}

	{#if editorError}
		<textarea {id} aria-labelledby="{id}-label" {placeholder} maxlength={maxLength} bind:value
		></textarea>
	{/if}

	<div
		class="editor-surface"
		class:editor-hidden={!ready}
		bind:this={editorRoot}
		aria-labelledby="{id}-label"
	></div>
	<input type="hidden" {name} {value} />
</div>

<style>
	.markdown-editor {
		inline-size: 100%;
		min-inline-size: 0;
	}

	.editor-status {
		margin-block: 0 0.75rem;
		color: var(--ink-muted);
	}

	.editor-label {
		display: block;
		margin-block-end: 0.5rem;
	}

	textarea {
		inline-size: 100%;
		min-block-size: 22rem;
		max-block-size: 40rem;
		padding: 0.75rem;
		border: 1px solid var(--border);
		border-radius: 0.25rem;
		background: var(--surface);
		color: var(--ink);
		font:
			0.95rem/1.5 ui-monospace,
			'Cascadia Code',
			monospace;
		resize: vertical;
	}

	.editor-surface {
		min-block-size: 22rem;
		border: 1px solid var(--border);
		border-radius: 0.25rem;
		background: var(--surface);
		color: var(--ink);
	}

	.editor-surface.editor-hidden {
		display: none;
	}

	.editor-surface :global(.milkdown) {
		--crepe-color-background: var(--surface);
		--crepe-color-on-background: var(--ink);
		--crepe-color-surface: var(--surface);
		--crepe-color-surface-low: var(--surface-muted);
		--crepe-color-on-surface: var(--ink);
		--crepe-color-on-surface-variant: var(--ink-muted);
		--crepe-color-outline: var(--border);
		--crepe-color-primary: var(--link);
		--crepe-color-secondary: color-mix(in oklch, var(--link), var(--surface) 82%);
		--crepe-color-on-secondary: var(--ink);
		--crepe-color-hover: color-mix(in oklch, var(--link), var(--surface) 92%);
		--crepe-color-selected: color-mix(in oklch, var(--link), var(--surface) 86%);
		--crepe-color-inline-area: var(--surface-muted);
		--crepe-base-font-size: 1rem;
		--crepe-font-default: inherit;
		--crepe-font-title: inherit;
	}
</style>
