import type { ShippingAddress } from '$lib/interfaces/OrderDetails';

export const currencyFormatter = new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: 'USD',
    minimumFractionDigits: 2
});

export function formatAddress(address: ShippingAddress): string {
    return [
        address.addressLine1,
        address.addressLine2,
        address.city,
        address.region,
        address.postalCode,
        address.countryCode
    ].filter(Boolean).join(', ');
}
