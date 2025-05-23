import type { Medium } from "$lib/interfaces/medium";

interface Product {
    id: number;
    title: string;
    price: number;
    height: number;
    width: number;
    medium: Medium;
    thumbnail: string;
    enabled: boolean;
    date_added: Date;
    mediumId: number;
    storefrontId: number;
}

export interface ProductsOut extends Product {
    imageUrl: string;
}

export interface ProductOut extends Product {
    description: string | null;
    images: string[];
}