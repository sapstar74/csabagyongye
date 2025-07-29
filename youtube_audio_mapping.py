# YouTube audio mapping functions

# Cache for YouTube audio filenames
_youtube_audio_cache = {}

def get_youtube_audio_filename_cached(index, topic):
    """Get YouTube audio filename from cache"""
    cache_key = f"{topic}_{index}"
    return _youtube_audio_cache.get(cache_key)

def get_youtube_audio_info(index, topic):
    """Get YouTube audio info"""
    filename = get_youtube_audio_filename_cached(index, topic)
    if filename:
        return {
            "filename": filename,
            "path": f"audio_files/{filename}",
            "exists": True
        }
    return None

# Initialize cache with existing mappings
def init_youtube_audio_cache():
    """Initialize YouTube audio cache"""
    # This would normally load from a mapping file
    # For now, return empty cache
    pass

# Initialize cache on import
init_youtube_audio_cache() 