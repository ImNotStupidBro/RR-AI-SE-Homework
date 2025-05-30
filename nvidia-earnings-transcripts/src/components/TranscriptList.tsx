import React, { useEffect, useState } from 'react';
import { fetchTranscripts } from '../services/transcriptService';
import { Transcript } from '../types';

const TranscriptList: React.FC = () => {
    const [transcripts, setTranscripts] = useState<Transcript[]>([]);
    const [loading, setLoading] = useState<boolean>(true);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        const getTranscripts = async () => {
            try {
                const data = await fetchTranscripts();
                setTranscripts(data);
            } catch (err) {
                setError('Failed to fetch transcripts');
            } finally {
                setLoading(false);
            }
        };

        getTranscripts();
    }, []);

    if (loading) {
        return <div>Loading...</div>;
    }

    if (error) {
        return <div>{error}</div>;
    }

    return (
        <div>
            <h2>NVIDIA Earnings Call Transcripts</h2>
            <ul>
                {transcripts.map((transcript) => (
                    <li key={transcript.id}>
                        <h3>{transcript.title}</h3>
                        <p>{transcript.date}</p>
                        <a href={transcript.link}>View Transcript</a>
                    </li>
                ))}
            </ul>
        </div>
    );
};

export default TranscriptList;