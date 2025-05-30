# NVIDIA Earnings Transcripts

This project is a Python-based application that identifies and retrieves the full transcripts of NVIDIA's earning calls for the last four quarters. It uses SQLAlchemy for database management and Flask for the web framework.

## Project Structure

```
nvidia-earnings-transcripts
├── src
│   ├── db
│   │   └── database.py
│   ├── services
│   │   └── transcript_service.py
│   ├── models
│   │   └── transcript.py
│   ├── main.py
│   └── utils
│       └── fetch_transcripts.py
├── requirements.txt
├── README.md
└── alembic.ini
```

## Setup Instructions

1. **Clone the repository:**
   ```
   git clone https://github.com/yourusername/nvidia-earnings-transcripts.git
   cd nvidia-earnings-transcripts
   ```

2. **Install dependencies:**
   ```
   pip install -r requirements.txt
   ```

3. **Run the application:**
   ```
   python src/main.py
   ```

4. **Open your browser:**
   Navigate to `http://localhost:5000` to view the application.

## Usage

The application will automatically fetch and display the transcripts of NVIDIA's earning calls for the last four quarters. You can navigate through the transcripts using the provided interface.

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue for any suggestions or improvements.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.