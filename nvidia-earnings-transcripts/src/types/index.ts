export interface Transcript {
    id: string;
    date: string;
    title: string;
    content: string;
}

export interface EarningsCall {
    quarter: string;
    year: number;
    transcripts: Transcript[];
}