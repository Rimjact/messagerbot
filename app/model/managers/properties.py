from app.model.database.requests import async_get_bot_properties


async def async_is_forms_acceptance_blocked() -> bool:
    """Проверяет, заблокирован ли на данный момент
    приём новых заявок на регистрацию от пользователей.

    Returns
    -------
    True если заблокирован, иначе False
    """

    bot_properties = await async_get_bot_properties()
    return bool(bot_properties.forms_acceptance_blocked)