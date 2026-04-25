  ---                                                                                                                                                                                                   
  Step 1 — Start your Neo4j instance
                                                                                                                                                                                                        
  In Neo4j Desktop, click the Start button on your database instance. Wait until it shows a green "Active" status. The bolt port defaults to 7687.
                                                                                                                                                                                                        
  ---             
  Step 2 — Update your .env file                                                                                                                                                                        
                                
  cp "/Users/jayakrushnamohapatra/Knowledge Graph/.env.example" "/Users/jayakrushnamohapatra/Knowledge Graph/.env"
                                                                                                                                                                                                        
  Open .env and set only the password — everything else can stay as-is:                                                                                                                                 
                                                                                                                                                                                                        
  NEO4J_URI=bolt://localhost:7687                                                                                                                                                                       
  NEO4J_USERNAME=neo4j
  NEO4J_PASSWORD=your_password_here   ← change this
  OLLAMA_URL=http://localhost:11434                                                                                                                                                                     
  OLLAMA_MODEL=llama3.2
                                                                                                                                                                                                        
  Where to find your password: In Neo4j Desktop → click your database → the password is what you set when you created the instance. If you forgot it, you can reset it from the three-dot menu →        
  "Manage" → "Reset DBMS password".
                                                                                                                                                                                                        
  ---             
  Step 3 — Make sure Ollama is running with llama3.2
                                                                                                                                                                                                        
  ollama pull llama3.2       # download the model (once)
  ollama serve               # start the Ollama server if not already running                                                                                                                           
                  
  ---                                                                                                                                                                                                   
  Step 4 — Install Python dependencies
                                                                                                                                                                                                        
  cd ~/Knowledge\ Graph
  pip install -r requirements.txt                                                                                                                                                                       
                  
  ---
  Step 5 — Seed the graph, then start
                                                                                                                                                                                                        
  python3 setup_graph.py     # creates drugs + interactions in Neo4j
  ./start.sh                 # starts API (:8000) + Streamlit UI (:8501)                                                                                                                                
                                                                                                                                                                                                        
  ---                                                                                                                                                                                                   
  Quick verification                                                                                                                                                                                    
                    
  After seeding, open Neo4j Browser at http://localhost:7474, log in, and run:
                                                                                                                                                                                                        
  MATCH (d:Drug) RETURN d                                                                                                                                                                                                                                                                                                                                                               
  You should see 5 drug nodes. Run this to confirm interactions:   