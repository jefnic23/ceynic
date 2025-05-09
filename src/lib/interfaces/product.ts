interface Product {
    id: number;
    title: string;
    price: number;
    height: number;
    width: number;
    mediumId: number;
    thumbnail: string;
    enabled: boolean;
}

export interface ProductsOut extends Product {
    imageUrl: string;
}

export interface ProductOut extends Product {
    description: string | null;
    images: string[];
}