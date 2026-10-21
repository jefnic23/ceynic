import { getContext, setContext } from 'svelte';

export type ToastMessage = {
	type: 'info' | 'warning' | 'error' | 'success';
	title: string;
	message: string;
	duration?: number;
};

type ShowToast = (toast: ToastMessage) => void;
type ToastContext = { show: ShowToast; dismiss: () => void };

const toastContext = Symbol('toast');

export function provideToast(showToast: ShowToast, dismissToast: () => void) {
	setContext<ToastContext>(toastContext, { show: showToast, dismiss: dismissToast });
}

export function useToast(): ShowToast {
	return getContext<ToastContext>(toastContext).show;
}

export function useDismissToast(): () => void {
	return getContext<ToastContext>(toastContext).dismiss;
}
