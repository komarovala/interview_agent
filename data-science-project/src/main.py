# main.py

from interview_agent import InterviewAgent
from example_usage import demo_interview, test_workflow

def main():
    """Основная функция для запуска агента интервью"""
    print("🎯 АГЕНТ ГЕНЕРАЦИИ СЦЕНАРИЯ ИНТЕРВЬЮ")
    print("Использует LangGraph для создания персональных вопросов")
    print("="*60)
    
    print("\nВыберите режим работы:")
    print("1. 🎬 Интерактивная демонстрация (полный интервью процесс)")
    print("2. 🧪 Тестирование workflow (без интерактивного ввода)")
    print("3. 🚀 Прямой запуск агента")
    
    choice = input("\nВведите номер (1, 2 или 3): ").strip()
    
    if choice == "1":
        print("\n🎬 Запуск интерактивной демонстрации...")
        demo_interview()
    elif choice == "2":
        print("\n🧪 Запуск тестирования workflow...")
        test_workflow()
    elif choice == "3":
        print("\n🚀 Прямой запуск агента...")
        agent = InterviewAgent()
        result = agent.run_interview()
        if result:
            summary = agent.get_interview_summary()
            print(f"\n✅ Интервью завершено для {summary['candidate_name']}")
    else:
        print("❌ Неверный выбор. Запускаем тестирование...")
        test_workflow()

if __name__ == "__main__":
    main()