"""
Конфигурация для агента интервью с OpenRouter.ai
"""

import os
from dotenv import load_dotenv

# Загружаем переменные окружения
load_dotenv()

class OpenRouterConfig:
    """Конфигурация для OpenRouter.ai"""
    
    def __init__(self):
        self.api_key = os.getenv('OPENROUTER_API_KEY', '')
        self.base_url = os.getenv('OPENROUTER_BASE_URL', 'https://openrouter.ai/api/v1')
        self.model = os.getenv('OPENROUTER_MODEL', 'claude-3.5-sonnet')
        self.app_name = os.getenv('OPENROUTER_APP_NAME', 'InterviewAgent')
        self.app_url = os.getenv('OPENROUTER_APP_URL', 'https://github.com/interview-agent')
        
        # Проверяем наличие API ключа
        if not self.api_key:
            print("⚠️  ВНИМАНИЕ: OPENROUTER_API_KEY не найден!")
            print("Создайте файл .env и добавьте:")
            print("OPENROUTER_API_KEY=your_api_key_here")
    
    def get_headers(self):
        """Получить заголовки для запросов к OpenRouter"""
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": self.app_url,
            "X-Title": self.app_name,
        }
    
    def is_configured(self):
        """Проверить, настроена ли конфигурация"""
        return bool(self.api_key)

# Глобальный экземпляр конфигурации
config = OpenRouterConfig()
