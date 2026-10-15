import type { PayPalNamespace } from '@paypal/paypal-js';
import { getContext, setContext } from 'svelte';

export type PayPalState = {
	sdk: PayPalNamespace | null;
	error: boolean;
};

const paypalContext = Symbol('paypal');

export function providePayPal(state: PayPalState) {
	setContext(paypalContext, state);
}

export function usePayPal(): PayPalState {
	return getContext<PayPalState>(paypalContext);
}
