#!/bin/bash
# Start the Drug Interaction Knowledge Graph system

echo "🌱 Seeding Neo4j graph..."
python3 setup_graph.py

echo ""
echo "🚀 Starting FastAPI backend on http://localhost:8000 ..."
python3 api.py &
API_PID=$!

sleep 2

echo "🎨 Starting Streamlit frontend on http://localhost:8501 ..."
streamlit run frontend.py &
FRONTEND_PID=$!

echo ""
echo "✅ System running!"
echo "   API:      http://localhost:8000"
echo "   Frontend: http://localhost:8501"
echo "   API Docs: http://localhost:8000/docs"
echo ""
echo "Press Ctrl+C to stop."

trap "kill $API_PID $FRONTEND_PID 2>/dev/null; exit" INT TERM
wait
