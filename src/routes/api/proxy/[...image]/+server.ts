import type { RequestHandler } from '@sveltejs/kit';
import { VITE_CLOUDINARY_CLOUD_NAME } from '$env/static/private';

export const GET: RequestHandler = async ({ params }) => {
    const imageUrl = `https://res.cloudinary.com/${VITE_CLOUDINARY_CLOUD_NAME}/image/upload/v1/${params.image}`;

    const response = await fetch(imageUrl);

    if (!response.ok) {
        return new Response('Image not found', { status: 404 });
    }

    const blob = await response.blob();
    
    return new Response(blob, {
        headers: {
            'Content-Type': blob.type,
            'Access-Control-Allow-Origin': '*'
        }
    });
};