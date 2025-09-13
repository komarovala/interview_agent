"""
Тестирование агента интервью с OpenRouter
"""

from interview_agent import InterviewAgent
from openrouter_client import OpenRouterClient
from config import config
import json


def test_openrouter_connection():
    """Тестирование подключения к OpenRouter"""
    print("🧪 Тестирование подключения к OpenRouter...")
    
    client = OpenRouterClient()
    
    # Простой тест
    test_messages = [
        {"role": "system", "content": "Ты - помощник. Ответь кратко."},
        {"role": "user", "content": "Привет! Как дела?"}
    ]
    
    response = client.generate_response(test_messages)
    
    if response:
        print(f"✅ OpenRouter работает! Ответ: {response[:100]}...")
        return True
    else:
        print("❌ OpenRouter недоступен, используется fallback режим")
        return False


def test_agent_workflow():
    """Тестирование workflow агента без интерактивного ввода"""
    print("\n🧪 Тестирование workflow агента...")
    
    agent = InterviewAgent()
    
    # Симулируем данные
    agent.state.candidate_name = "Анна Петрова"
    agent.state.candidate_age = 28
    agent.state.candidate_position = "Python разработчик"
    
    # Тестируем генерацию вопросов
    print("📝 Генерация вопросов...")
    questions = agent.openrouter_client.generate_interview_questions(
        agent.state.candidate_name,
        agent.state.candidate_age,
        agent.state.candidate_position
    )
    
    print(f"✅ Сгенерировано {len(questions)} вопросов:")
    for i, q in enumerate(questions[:3], 1):
        print(f"  {i}. {q}")
    
    if len(questions) > 3:
        print(f"  ... и еще {len(questions) - 3} вопросов")
    
    return questions


def test_agent_summary():
    """Тестирование сводки агента"""
    print("\n🧪 Тестирование сводки агента...")
    
    agent = InterviewAgent()
    agent.state.candidate_name = "Иван Сидоров"
    agent.state.candidate_age = 32
    agent.state.candidate_position = "Data Scientist"
    agent.state.interview_questions = ["Вопрос 1", "Вопрос 2", "Вопрос 3"]
    
    summary = agent.get_interview_summary()
    
    print("📊 Сводка агента:")
    print(f"  Имя: {summary['candidate_name']}")
    print(f"  Возраст: {summary['candidate_age']}")
    print(f"  Позиция: {summary['candidate_position']}")
    print(f"  Вопросов: {summary['total_questions']}")
    print(f"  OpenRouter: {'✅' if summary['openrouter_used'] else '❌'}")
    
    return summary


def main():
    """Основная функция тестирования"""
    print("🎯 ТЕСТИРОВАНИЕ АГЕНТА ИНТЕРВЬЮ")
    print("="*50)
    
    # Проверяем конфигурацию
    print(f"🔧 Конфигурация OpenRouter: {'✅' if config.is_configured() else '❌'}")
    if config.is_configured():
        print(f"   Модель: {config.model}")
    else:
        print("   Работаем в fallback режиме")
    
    # Тестируем подключение
    openrouter_works = test_openrouter_connection()
    
    # Тестируем workflow
    questions = test_agent_workflow()
    
    # Тестируем сводку
    summary = test_agent_summary()
    
    # Итоговый результат
    print("\n" + "="*50)
    print("📋 ИТОГИ ТЕСТИРОВАНИЯ:")
    print(f"  OpenRouter: {'✅' if openrouter_works else '❌'}")
    print(f"  Генерация вопросов: {'✅' if questions else '❌'}")
    print(f"  Сводка агента: {'✅' if summary else '❌'}")
    print(f"  Общий статус: {'✅ ВСЕ РАБОТАЕТ' if all([questions, summary]) else '⚠️ ЕСТЬ ПРОБЛЕМЫ'}")
    
    # Сохраняем результат теста
    test_result = {
        "openrouter_works": openrouter_works,
        "questions_generated": len(questions) if questions else 0,
        "summary_works": bool(summary),
        "config_configured": config.is_configured(),
        "model": config.model if config.is_configured() else "fallback"
    }
    
    with open('test_result.json', 'w', encoding='utf-8') as f:
        json.dump(test_result, f, ensure_ascii=False, indent=2)
    
    print(f"\n💾 Результат теста сохранен в test_result.json")


if __name__ == "__main__":
    main()
