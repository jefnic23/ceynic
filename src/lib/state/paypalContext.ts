import type { PayPalNamespace } from '@paypal/paypal-js';

export const paypalContextKey = Symbol('paypal');

export interface PayPalContext {
	paypal: PayPalNamespace | null;
}
