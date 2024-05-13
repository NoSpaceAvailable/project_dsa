try:
    import fastapi
    import uvicorn
    import multipart
    print("[o] All required modules are installed. Booting application ...")
except:
    import os
    print("[o] Starting to install needed packets ...")
    os.system("pip3 install -r requirements.txt")

exit(0)