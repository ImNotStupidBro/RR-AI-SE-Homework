import axios from 'axios';

const BASE_URL = 'https://api.example.com/nvidia/earnings-calls'; // Replace with the actual API endpoint

export interface Transcript {
    quarter: string;
    date: string;
    transcript: string;
}

export const fetchTranscripts = async (): Promise<Transcript[]> => {
    try {
        const response = await axios.get(`${BASE_URL}?quarters=4`);
        return response.data;
    } catch (error) {
        console.error('Error fetching transcripts:', error);
        throw error;
    }
};