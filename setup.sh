mkdir -p ~/.streamlit/
echo "[theme]
base='dark'
primaryColor='#FF4B4B'
secondaryBackgroundColor='#262730'
textColor='#FAFAFA'
font = 'sans serif'
[server]
headless = true
port = $PORT
enableCORS = false
" > ~/.streamlit/config.toml