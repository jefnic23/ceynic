<script lang="ts">
	import type { SocialMediaLinkOut } from '$lib/interfaces/SocialMediaLinkOut';
	import Icon, { type IconProps } from '@iconify/svelte';

	interface Props {
		copyright?: string;
		socialMediaLinks?: SocialMediaLinkOut[];
	}

	let { copyright = "", socialMediaLinks = [] }: Props = $props();

    let year: number = new Date().getFullYear();

	const iconMap: Record<string, IconProps> = {
		etsy: { icon: "mdi:etsy", color: "#eb6d20" },
		facebook: { icon: "mdi:facebook", color: "#1877F2" },
		instagram: { icon: "mdi:instagram", color: "#000000" },
		linkedin: { icon: "mdi:linkedin", color: "#0077B5" },
		pinterest: { icon: "mdi:pinterest", color: "#E60023" },
		tiktok: { icon: "ic:baseline-tiktok", color: "#000000" },
		twitter: { icon: "bi:twitter-x", color: "#000000" }
		// todo: add more
	}
</script>

<div class="footer">
    <div class="icons">
		<!-- todo: move social links to sidebar in mobile -->
		{#each socialMediaLinks as { name, url }}
			{@const iconProps = iconMap[name.toLowerCase()]}
			<a href={url} target="_blank">
				<Icon 
					icon={iconProps.icon} 
					color={iconProps.color || ""} 
					width={32} 
					height={32}
				/>
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