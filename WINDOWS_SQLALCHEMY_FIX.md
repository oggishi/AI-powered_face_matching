# Windows SQLAlchemy Multiprocessing Fix

## Problem
When running the FastAPI application on **Windows with Python 3.11**, you may encounter this error:

```
File "C:\Users\...\Lib\platform.py", line 284, in _syscmd_ver
    info = subprocess.check_output(cmd,
...
```

This happens when using uvicorn's `--reload` option because:
1. Uvicorn uses multiprocessing for auto-reload
2. SQLAlchemy tries to detect platform information during import
3. Windows multiprocessing conflicts with subprocess calls in SQLAlchemy

## Solutions Implemented

### Solution 1: Disabled Auto-Reload on Windows (RECOMMENDED)
The `main.py` has been updated to automatically disable reload on Windows:

```python
# In main.py
if __name__ == "__main__":
    use_reload = settings.DEBUG and sys.platform != "win32"
    uvicorn.run("main:app", reload=use_reload, ...)
```

**Run with:**
```bash
python main.py
```

✅ **Pros:** No errors, stable
❌ **Cons:** Must restart server manually after code changes

### Solution 2: Use Uvicorn Without Reload
If you start the server directly, just don't use `--reload`:

```bash
face_env\Scripts\activate
uvicorn main:app --host 0.0.0.0 --port 8000
```

### Solution 3: Development Mode (Manual Restart)
For development, you have two options:

**Option A: Manual restart** (safest)
```bash
python main.py
# Make code changes
# Press Ctrl+C
# Run again: python main.py
```

**Option B: Use watchdog** (if you want auto-reload)
```bash
pip install watchdog
watchmedo auto-restart --patterns="*.py" --recursive -- python main.py
```

## Running the Application

### Production (No Auto-Reload)
```bash
# Windows
face_env\Scripts\activate
python main.py
```

### Development (With Manual Restart)
```bash
# Windows
face_env\Scripts\activate
python main.py

# Make changes, then:
# Ctrl+C to stop
# python main.py to restart
```

### Using start.bat (Easiest)
```bash
start.bat
```
This automatically activates the environment and runs without reload.

## Testing After Fix

1. **Start the server:**
   ```bash
   python main.py
   ```

2. **You should see:**
   ```
   ✅ Database initialized
   ✅ AI-Powered Face Matching System v1.0.0 started
   📝 API Documentation: http://0.0.0.0:8000/docs
   INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
   ```

3. **Open browser:**
   - Main UI: http://localhost:8000
   - API Docs: http://localhost:8000/docs

4. **Test the application:**
   - Upload a face image
   - Add it to database
   - Search for similar faces

## Why This Happens

This is a known compatibility issue between:
- **SQLAlchemy 2.0.44+** (uses Cython extensions)
- **Python 3.11** on Windows
- **Multiprocessing** (used by uvicorn --reload)

The issue occurs because:
1. Uvicorn's reload spawns a new process
2. SQLAlchemy imports try to detect the Windows version
3. The `platform.machine()` call uses subprocess
4. Windows multiprocessing doesn't fully initialize subprocess in spawned processes

## Alternative: Use Docker

If you need auto-reload in development, use Docker instead:

```bash
docker-compose up --build
```

Docker doesn't have this Windows-specific issue.

## References

- SQLAlchemy Issue: https://github.com/sqlalchemy/sqlalchemy/issues/9810
- Uvicorn Reload: https://www.uvicorn.org/#command-line-options
- Python Multiprocessing on Windows: https://docs.python.org/3/library/multiprocessing.html#multiprocessing-start-methods

## Status

✅ **FIXED** - The application now runs without errors on Windows
✅ Auto-reload disabled on Windows by default
✅ Use `start.bat` for easiest startup
