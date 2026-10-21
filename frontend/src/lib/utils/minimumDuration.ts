export async function waitForMinimumDuration(startedAt: number, minimumMs = 500): Promise<void> {
	const remaining = minimumMs - (performance.now() - startedAt);
	if (remaining > 0) {
		await new Promise<void>((resolve) => setTimeout(resolve, remaining));
	}
}
