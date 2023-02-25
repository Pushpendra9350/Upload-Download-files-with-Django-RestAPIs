from rest_framework_simplejwt.tokens import RefreshToken

def get_tokens_for_user(user):
    """
    This function will return refersh and access token for a user
    """
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }