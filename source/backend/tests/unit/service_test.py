from app.core.services import GreetingService


def test_generate_greeting():
    test_message = "Test Hello!"
    service = GreetingService(test_message)
    
    result = service.generate_greeting("User")
    
    assert result == "Test Hello! Вітаємо, User."