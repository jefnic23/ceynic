<script lang="ts">
	import Card from '$lib/components/shared/Card.svelte';
	import Input from '$lib/components/shared/Input.svelte';
	import MarkdownEditor from '$lib/components/shared/MarkdownEditor.svelte';
	import Button from '$lib/components/shared/Button.svelte';
	import { useToast } from '$lib/state/toast';
	import type { ActionData, PageData } from './$types';
	import PageContainer from '$lib/components/shared/PageContainer.svelte';

	let { data, form }: { data: PageData; form: ActionData } = $props();
	let about = $state(data.about);
	const showToast = useToast();

	$effect(() => {
		about = form?.about ?? data.about;
		if (form?.message) {
			showToast({ type: 'error', title: 'About page not saved', message: form.message });
		} else if (form?.success) {
			showToast({
				type: 'success',
				title: 'About page saved',
				message: 'Your About page content has been updated.'
			});
		}
	});
</script>

<PageContainer max="1200px">
	<div class="account-sections">
		<Card width="100%">
			<h1>Account</h1>
			<div class="form-stack fields">
				<Input
					id="contact-email"
					label="Contact email"
					type="email"
					value={data.user.email}
					readonly
				/>
				<Input id="first-name" label="First name" value={data.user.firstName ?? ''} readonly />
				<Input id="last-name" label="Last name" value={data.user.lastName ?? ''} readonly />
			</div>
		</Card>

		<Card width="100%">
			<h2>About page</h2>
			<form class="form-stack" method="POST">
				<p>Edit the text shown on your public About page. Markdown formatting is supported.</p>
				<MarkdownEditor
					id="about-content"
					name="about"
					label="About page content"
					placeholder="Write your About page. Type / for block options."
					maxLength={50_000}
					bind:value={about}
				/>
				<Button type="submit">Save About page</Button>
			</form>
		</Card>
	</div>
</PageContainer>

<style>
	.account-sections {
		display: grid;
		gap: 1.5rem;
	}

	h1,
	h2 {
		margin-block: 0 1.5rem;
	}

	.fields {
		gap: 1.5rem;
	}
</style>
