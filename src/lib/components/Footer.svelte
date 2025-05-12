<script lang="ts">
    import Etsy from '$lib/icons/Etsy.svelte';
	import Facebook from '$lib/icons/Facebook.svelte';
	import Instagram from '$lib/icons/Instagram.svelte';
	import LinkedIn from '$lib/icons/LinkedIn.svelte';
	import Pinterest from '$lib/icons/Pinterest.svelte';
	import TikTok from '$lib/icons/TikTok.svelte';
	import Twitter from '$lib/icons/Twitter.svelte';
	import type { SocialMediaLink } from '$lib/interfaces/socialMediaLink';
	import type { ComponentType } from 'svelte';

	export let copyright: string = "";
	export let socialMediaLinks: SocialMediaLink[] = [];

    let year: number = new Date().getFullYear();

	const iconMap: Record<string, ComponentType> = {
		etsy: Etsy,
		facebook: Facebook,
		instagram: Instagram,
		linkedin: LinkedIn,
		pinterest: Pinterest,
		tiktok: TikTok,
		twitter: Twitter
		// todo: add more
	}
</script>

<div class="footer">
    <div class="icons">
		{#each socialMediaLinks as { name, url }}
			<a href={url} target="_blank">
				<svelte:component this={iconMap[name.toLowerCase()]} size={32} />
			</a>
		{/each}
    </div>
    <div class="copyright">
		<div>
			Copyright © {year}{copyright ? `, ${copyright}` : ""}. All rights reserved.
		</div>
		<div>
			<a href="/admin" style:color="#666666" style:text-decoration="none" target="_blank">Administration</a>
		</div>
		<div>
			Powered by <a href="https://github.com/jefnic23" target="_blank">ceynic.org</a>
		</div>
    </div>
</div>

<style>
    .footer {
		display: flex;
		flex-direction: column;
		align-items: center;
		gap: 1rem;
		padding: 1rem;
		background-color: #f8f8f8;
		border: 1px solid #e7e7e7;
	}

	.icons {
		display: flex;
		flex-direction: row;
		align-items: center;
		gap: 1rem;
	}

	.copyright {
		display: flex;
		flex-direction: row;
		font-size: 12px;
	}

	.copyright > div {
		position: relative;
		padding: 0 0.5rem;
	}

	.copyright > div:not(:last-child)::after {
		content: "|";
		position: absolute;
		right: 0;
	}

	@media (max-width: 768px) {
        .copyright {
            flex-direction: column;
			text-align: center;
        }

		.copyright > div:not(:last-child)::after {
			content: '';
		}
    }
</style>