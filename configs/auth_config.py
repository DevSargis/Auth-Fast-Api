"""
Authentication Configuration Module

This module provides configuration management for authentication settings,
including Clerk integration, environment variables, and authentication provider setup.

Configuration Management:
- Environment variable loading and validation
- Clerk API configuration
- Authentication provider selection
- Error handling for missing configuration

Environment Variables:
- AUTH_PROVIDER: Authentication provider (default: "clerk")
- CLERK_SECRET_KEY: Clerk secret key for API access
- CLERK_API_URL: Clerk API base URL

Configuration Validation:
- Checks for required environment variables
- Provides default values where appropriate
- Raises clear error messages for missing configuration

Security Considerations:
- Secret keys should be stored securely
- Environment variables should not be committed to version control
- API URLs should use HTTPS in production

Example Usage:
    from configs.auth_config import AUTH_PROVIDER, CLERK_SECRET_KEY
    
    if AUTH_PROVIDER == "clerk":
        # Use Clerk authentication
        pass
    
    # Access Clerk configuration
    secret_key = CLERK_SECRET_KEY
    api_url = CLERK_API_URL
"""

import os
from typing import Optional

# Authentication provider configuration
AUTH_PROVIDER = os.getenv("AUTH_PROVIDER", "clerk")

# Clerk configuration
CLERK_SECRET_KEY = os.getenv("CLERK_SECRET_KEY")
CLERK_API_URL = os.getenv("CLERK_API_URL", "https://api.clerk.com/v1")

# Validate required configuration
if not AUTH_PROVIDER:
    raise ValueError("AUTH_PROVIDER environment variable is not set")

if AUTH_PROVIDER == "clerk" and not CLERK_SECRET_KEY:
    raise ValueError("CLERK_SECRET_KEY environment variable is not set")

# Configuration validation functions
def validate_clerk_config() -> bool:
    """
    Validate Clerk configuration.
    
    Checks that all required Clerk environment variables are set.
    
    Returns:
        bool: True if configuration is valid
        
    Raises:
        ValueError: If required configuration is missing
    """
    if not CLERK_SECRET_KEY:
        raise ValueError("CLERK_SECRET_KEY is required for Clerk authentication")
    
    if not CLERK_API_URL:
        raise ValueError("CLERK_API_URL is required for Clerk authentication")
    
    return True

def get_auth_provider() -> str:
    """
    Get current authentication provider.
    
    Returns:
        str: Current authentication provider name
    """
    return AUTH_PROVIDER

def is_clerk_enabled() -> bool:
    """
    Check if Clerk authentication is enabled.
    
    Returns:
        bool: True if Clerk is the current provider
    """
    return AUTH_PROVIDER == "clerk" 