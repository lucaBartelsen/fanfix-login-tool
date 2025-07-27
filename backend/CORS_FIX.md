# CORS Configuration for Chrome Extensions

## The Issue

Chrome extensions have unique origin URLs like `chrome-extension://djanlfmfldfabkjcehpnjphnfaflfnfc` which need special CORS handling.

## Solution

The backend has been updated to use a regex pattern to allow all Chrome extension origins:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origin_regex="chrome-extension://.*",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"]
)
```

## Alternative Solutions

### 1. If you want to restrict to specific extensions:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "chrome-extension://djanlfmfldfabkjcehpnjphnfaflfnfc",
        "chrome-extension://your-other-extension-id",
        "https://api.chatsassistant.com"  # For web access
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### 2. For development with both local and production:

```python
origins = [
    "chrome-extension://djanlfmfldfabkjcehpnjphnfaflfnfc",
    "http://localhost:3000",
    "https://api.chatsassistant.com"
]

# Or use regex for all Chrome extensions
app.add_middleware(
    CORSMiddleware,
    allow_origin_regex="(chrome-extension://.*|http://localhost:.*)",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## Deployment Steps

1. Update the backend code with the CORS fix
2. Restart your backend service:
   ```bash
   # If using systemd
   sudo systemctl restart fanfix-backend
   
   # Or if running directly
   # Kill the current process and restart
   uvicorn app.main:app --host 0.0.0.0 --port 8000
   ```

3. Test the Chrome extension again

## Testing CORS

You can test if CORS is working with curl:

```bash
curl -H "Origin: chrome-extension://djanlfmfldfabkjcehpnjphnfaflfnfc" \
     -H "Access-Control-Request-Method: POST" \
     -H "Access-Control-Request-Headers: Content-Type" \
     -X OPTIONS \
     https://api.chatsassistant.com/token -v
```

Look for these headers in the response:
- `Access-Control-Allow-Origin: chrome-extension://djanlfmfldfabkjcehpnjphnfaflfnfc`
- `Access-Control-Allow-Credentials: true`

## Chrome Extension Manifest

Make sure your manifest.json includes the API domain in host_permissions:

```json
"host_permissions": [
    "https://auth.fanfix.io/*",
    "https://fanfix.io/*",
    "https://api.chatsassistant.com/*"
]
```