interface Name {
    givenName: string;
    surname: string
}

interface Address {
    addressLine1: string;
    addressLine2: string;
    adminArea1: string;
    adminArea2: string;
    postalCode: string;
    countryCode: string;
}

interface Paypal {
    name: Name;
    emailAddress: string;
    accountId: string;
    accountStatus: string;
    address: Address;
}

interface PaymentSource {
    paypal: Paypal;
}

interface Amount {
    currencyCode: string;
    value: number;
}

interface Payee {
    email_address: string;
    merchant_id: string;
}

interface Shipping {
    address: Address;
}

interface Link {
    href: string;
    ref: string;
    method: string;
}

interface Authorization {
    id: string;
    status: string;
    amount: Amount;
    seller_protection: object;
    expiration_time: Date;
    create_time: Date;
    update_time: Date;
    links: Link[];
}

interface GrossAmount {
    currency_code: string;
    value: number;
}

interface PaypalFee {
    currency_code: string;
    value: number;
}

interface NetAmount {
    currency_code: string;
    value: number;
}

interface SellerReceivableBreakdown {
    gross_amount: GrossAmount;
    paypal_fee: PaypalFee;
    net_amount: NetAmount;
}

interface Capture {
    id: string;
    status: string;
    amount: Amount;
    seller_protection: object;
    final_capture: boolean;
    disbursement_mode: string;
    seller_receivable_breakdown: SellerReceivableBreakdown;
    create_time: Date;
    update_time: Date;
    links: Link[];
}

interface Payments {
    authorizations: Authorization[];
    captures: Capture[];
}

interface PurchaseUnit {
    referenceId: string;
    payee: Payee;
    description: string;
    shipping: Shipping;
    payments: Payments;
    amount: Amount;
}

interface Payer {
    name: Name;
    emailAddress: string;
    payerId: string;
}

export interface OrdersOut {
    id: string;
    createTime: Date;
    status: string;
}

export interface OrderOut {
    id: string;
    status: string;
    intent: string;
    paymentSource: PaymentSource;
    purchaseUnits: PurchaseUnit[];
    payer: Payer;
    createTime: Date;
    links: Link[];
}