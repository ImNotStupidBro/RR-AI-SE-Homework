import React, { useEffect, useState } from 'react';
import TranscriptList from '../components/TranscriptList';
import { fetchTranscripts } from '../services/transcriptService';

const Home: React.FC = () => {
    const [transcripts, setTranscripts] = useState([]);

    useEffect(() => {
        const getTranscripts = async () => {
            const data = await fetchTranscripts();
            setTranscripts(data);
        };

        getTranscripts();
    }, []);

    return (
        <div>
            <h1>NVIDIA Earnings Calls Transcripts</h1>
            <TranscriptList transcripts={transcripts} />
        </div>
    );
};

export default Home;