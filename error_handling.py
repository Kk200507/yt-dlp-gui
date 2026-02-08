def get_user_friendly_error(error_msg: str) -> tuple[str, str]:
    """
    Parses a raw exception message and returns a tuple of (title, friendly_description).
    """
    msg = error_msg.lower()

    if "already been downloaded" in msg:
        return (
            "Already Downloaded",
            "This file already exists in the selected folder."
        )

    if "javascript runtime" in msg:
        return (
            "Limited Format Support",
            "Some video formats may be unavailable due to missing JavaScript runtime.\n"
            "Basic downloads should still work."
        )
    
    # FFmpeg issues
    if "ffmpeg" in msg or "merging" in msg:
        return (
            "FFmpeg Missing", 
            "High-quality downloads require FFmpeg to merge video and audio streams.\n\n"
            "Please install FFmpeg and add it to your system PATH, or ensure it is in the application folder."
        )
    
    # Access/Permissions
    if "private video" in msg:
        return (
            "Private Video", 
            "This video is marked as private. The application cannot download it without access permissions."
        )
        
    if "sign in to confirm your age" in msg or "age-restricted" in msg:
        return (
            "Age Restricted", 
            "This video is age-restricted by YouTube. The application currently does not support age verification."
        )

    if "geo-restricted" in msg or "not available in your country" in msg:
        return (
            "Region Locked", 
            "This video is not available in your country or region."
        )

    if "member-only" in msg:
        return (
            "Members Only",
            "This video is available to channel members only."
        )

    # Network Errors
    if any(x in msg for x in ["network is unreachable", "timed out", "connection refused", "eof occurred", "temporary failure in name resolution"]):
        return (
            "Network Error", 
            "Could not connect to the server. Please check your internet connection and try again."
        )
        
    # Invalid Input
    if "unable to download webpage" in msg or "incomplete youtube id" in msg or "is not a valid url" in msg:
        return (
            "Invalid URL", 
            "The provided URL could not be accessed. Please ensure it is a valid YouTube link."
        )

    if "video unavailable" in msg:
        return (
            "Video Unavailable",
            "This video is unavailable. It may have been deleted or removed by the uploader."
        )

    # File System
    if "permission denied" in msg:
        return (
            "Permission Denied",
            "The application does not have permission to write to the selected download folder.\n"
            "Please choose a different folder."
        )
    
    if "disk is full" in msg or "no space left" in msg:
        return (
            "Disk Full",
            "There is not enough space on the disk to save this video."
        )

    # Default
    return (
        "Download Failed", 
        "An unexpected error occurred during the download process."
    )

