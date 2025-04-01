successful_get_advertiser_response = """Рекламодатель успешно {action}!\n
Данные рекламодателя:
ID: `{id}`
Название: `{name}`"""

successful_send_ml_score_response = """ML-score успешно добавлен!\n
ID рекламодателя: `{advertiser_id}`
ID клиента: `{client_id}`
ML-score: `{ml_score}`"""

add_id = """Пришлите мне ID {model}, для которого вы хотите добавить ML-score"""

add_ml_score = (
    """Пришлите мне ML-score, который вы хотите присвоить рекламодателю `{advertiser_id}` и клиенту `{client_id}`"""
)

send_advertiser_menu = """Для добавления клиента вам необходимо последовательно прислать ID и название рекламодателя

Для начала пришлите ID рекламодателя (uuid)"""

send_advertiser_attribute = """Теперь пришлите {attribute} рекламодателя"""
