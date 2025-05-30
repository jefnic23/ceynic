import { PUBLIC_API_URL } from '$env/static/public';
import type { PaymentProcessor } from "$lib/enums/paymentProcessor";

export const load = async ({ fetch }) => {
    const fetchPaymentProcessor = async (): Promise<PaymentProcessor> => {
        const response = await fetch(`${PUBLIC_API_URL}/settings/paymentProcessor`);

        if (!response.ok) {
            console.log("Error retrieving payment processor.");
        }

        const responseData: PaymentProcessor = await response.json();

        return responseData;
    }

    return {
        paymentProcessor: fetchPaymentProcessor()
    }
}