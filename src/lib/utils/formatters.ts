import type { Address } from '$lib/interfaces/OrderDetails';

export const currencyFormatter = new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: 'USD',
    minimumFractionDigits: 2
});

export function formatAddress(address: Address): string {
    return [
        address.addressLine1,
        address.addressLine2,
        address.adminArea2,
        address.adminArea1,
        address.postalCode,
        address.countryCode
    ].filter(Boolean).join(', ');
}
