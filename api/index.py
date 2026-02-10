from app import app

# Vercel serverless function handler
async def handler(request):
    """Serverless function handler for Vercel"""
    return app
