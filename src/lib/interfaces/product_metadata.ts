export interface PriceRange {
    minimum: number;
    maximum: number
}

export interface MediumCount {
    id: number;
    name: string;
    count: number;
}

export interface SizeRanges {
    widthMinimum: number;
    widthMaximum: number;
    heightMinimum: number;
    heightMaximum: number;
}

export interface ProductMetadata {
    priceRange: PriceRange;
    mediumCounts: MediumCount[];
    sizeRanges: SizeRanges;
}
