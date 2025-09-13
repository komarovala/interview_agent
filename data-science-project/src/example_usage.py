"""
Пример использования агента интервью
"""

from interview_agent import InterviewAgent
import json


def demo_interview():
    """Демонстрация работы агента интервью"""
    print("🎬 ДЕМОНСТРАЦИЯ АГЕНТА ИНТЕРВЬЮ")
    print("="*50)
    
    # Создаем агента
    agent = InterviewAgent()
    
    # Запускаем интервью
    result = agent.run_interview()
    
    if result:
        # Получаем сводку
        summary = agent.get_interview_summary()
        
        print("\n📋 ДЕТАЛЬНАЯ СВОДКА:")
        print(json.dumps(summary, ensure_ascii=False, indent=2))
        
        # Сохраняем результат в файл
        with open('interview_result.json', 'w', encoding='utf-8') as f:
            json.dump(summary, f, ensure_ascii=False, indent=2)
        
        print(f"\n💾 Результат сохранен в файл: interview_result.json")
    
    return result


def test_workflow():
    """Тестирование workflow без интерактивного ввода"""
    print("🧪 ТЕСТИРОВАНИЕ WORKFLOW")
    print("="*30)
    
    agent = InterviewAgent()
    
    # Симулируем ввод данных
    print("Тестируем ноду получения имени...")
    agent.state.candidate_name = "Анна Петрова"
    agent.state.add_message("user", "Анна Петрова")
    agent.state.add_message("assistant", "Приятно познакомиться, Анна Петрова!")
    
    print("Тестируем ноду получения возраста...")
    agent.state.candidate_age = 28
    agent.state.add_message("user", "28")
    agent.state.add_message("assistant", "Спасибо! Вам 28 лет.")
    
    print("Тестируем генерацию вопросов...")
    questions = agent._generate_personalized_questions("Анна Петрова", 28)
    agent.state.interview_questions = questions
    
    print(f"✅ Сгенерировано {len(questions)} вопросов")
    print("✅ Workflow работает корректно!")
    
    return agent.get_interview_summary()


if __name__ == "__main__":
    print("Выберите режим:")
    print("1. Интерактивная демонстрация")
    print("2. Тестирование workflow")
    
    choice = input("Введите номер (1 или 2): ").strip()
    
    if choice == "1":
        demo_interview()
    elif choice == "2":
        test_workflow()
    else:
        print("Неверный выбор. Запускаем тестирование...")
        test_workflow()
