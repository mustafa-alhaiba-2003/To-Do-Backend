# notifications/services.py
from firebase_admin import messaging
from apps.notifications.models import FCMDevice, NotificationHistory

def create_and_send_notification(user, title, body, data=None):
    NotificationHistory.objects.create(
        user=user,
        title=title,
        body=body,
        data_payload=data
    )

    devices = FCMDevice.objects.filter(user=user, is_active=True)
    tokens = list(devices.values_list('registration_token', flat=True))

    if not tokens:
        return {"status": "ignored", "reason": "No active devices found."}

    message = messaging.MulticastMessage(
        notification=messaging.Notification(title=title, body=body),
        data=data or {},
        tokens=tokens,
    )

    response = messaging.send_multicast(message)
    
    if response.failure_count > 0:
        _cleanup_failed_tokens(tokens, response.responses)

    return {"status": "success", "success_count": response.success_count}

def _cleanup_failed_tokens(tokens, responses):
    """Removes tokens that Firebase tells us are no longer valid."""
    failed_tokens = []
    for idx, resp in enumerate(responses):
        if not resp.success:
            if resp.exception.code in ['messaging/invalid-registration-token', 'messaging/registration-token-not-registered']:
                failed_tokens.append(tokens[idx])
    
    if failed_tokens:
        FCMDevice.objects.filter(registration_token__in=failed_tokens).update(is_active=False)