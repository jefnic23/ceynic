<script lang="ts">
	import type { Snippet } from "svelte";
	import type { LayoutData } from './$types';
	import AdminNavigation from '$lib/components/admin/AdminNavigation.svelte';
	import { invalidateAll, onNavigate } from '$app/navigation';

	onNavigate((navigation) => {
		if (!document?.startViewTransition) return;

		return new Promise((resolve) => {
			document?.startViewTransition(async () => {
				resolve();
				await navigation.complete;
			});
		});
	});
	
	interface Props {
		data: LayoutData;
		children?: Snippet;
	}

	let { data, children }: Props = $props();

	$effect(() => {
		const expiresAt = data.refreshExpiresAt;
		if (expiresAt === null) return;

		let active = true;
		let checking = false;
		let timer: ReturnType<typeof setTimeout>;

		function checkSession() {
			if (expiresAt === null) return;
			clearTimeout(timer);
			if (Date.now() >= expiresAt) {
				if (checking) return;
				checking = true;
				void invalidateAll().catch(() => {
					// The server remains authoritative; retry if the recheck cannot complete.
				}).finally(() => {
					checking = false;
					// Retry if the recheck failed without navigating away or updating the expiry.
					if (active) timer = setTimeout(checkSession, 30_000);
				});
			} else {
				// Browser timers cannot reliably wait longer than 2^31 - 1 ms.
				timer = setTimeout(checkSession, Math.min(expiresAt - Date.now(), 2_147_483_647));
			}
		}

		function onVisibilityChange() {
			if (document.visibilityState === 'visible') checkSession();
		}

		checkSession();
		document.addEventListener('visibilitychange', onVisibilityChange);
		return () => {
			active = false;
			clearTimeout(timer);
			document.removeEventListener('visibilitychange', onVisibilityChange);
		};
	});
</script>

<div class="container">
	<AdminNavigation />

	{#key data.url}
		<main>
			{@render children?.()}
		</main>
	{/key}
</div>

<style>
	.container {
		display: flex;
		flex-direction: row;
	}

	main {
		width: 100%;
		min-width: 0;
		display: flex;
		justify-content: flex-start;
		align-items: flex-start;
		margin-block: 1rem;
		margin-inline: 1rem;
		view-transition-name: main;
	}

	main :global(.card) {
		margin-inline: 0;
	}
</style>
