from supabase import create_client, Client
from core.config import settings
import traceback

def get_supabase_client() -> Client:
    # Graceful degradation if Supabase is not properly configured by the user yet.
    try:
        # Avoid trying to connect if default placeholder keys are used
        if settings.SUPABASE_KEY == "your-supabase-anon-key":
            print("[WARNING] Supabase is using placeholder credentials. Database logging is disabled.")
            return None
            
        supabase: Client = create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)
        return supabase
    except Exception as e:
        print(f"[WARNING] Could not initialize Supabase client. Running in offline mode. Error: {e}")
        return None

supabase_client = get_supabase_client()
