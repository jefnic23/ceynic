import { LocalStorage } from "$lib/storage.svelte";
import type { ProductOut } from "$lib/interfaces/ProductOut";

type Cart = {
    products: ProductOut[];
}

export const cart = new LocalStorage<Cart>('cart', {
    products: []
});