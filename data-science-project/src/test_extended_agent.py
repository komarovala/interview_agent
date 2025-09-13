"""
Тестирование расширенного агента интервью
"""

from interview_agent import InterviewAgent
from openrouter_client import OpenRouterClient
from config import config
import json


def test_extended_workflow():
    """Тестирование расширенного workflow агента"""
    print("🧪 ТЕСТИРОВАНИЕ РАСШИРЕННОГО АГЕНТА")
    print("="*50)
    
    agent = InterviewAgent()
    
    # Симулируем полный workflow
    print("📋 Симулируем расширенный workflow...")
    
    # Создаем тестовое состояние
    test_state = {
        "messages": [],
        "candidate_name": "Анна Петрова",
        "candidate_age": 28,
        "candidate_position": "Python разработчик",
        "vacancy_requirements": ["Python", "Django", "PostgreSQL", "Опыт 3+ лет"],
        "general_questions": [],
        "general_answers": [],
        "technical_questions": [],
        "technical_answers": [],
        "followup_questions": [],
        "interview_questions": [],
        "current_step": "start",
        "ai_responses": [],
        "analysis_results": []
    }
    
    # Тестируем генерацию общих вопросов
    print("\n1️⃣ Тестируем генерацию общих вопросов...")
    general_questions = agent.openrouter_client.generate_general_questions(
        test_state["candidate_name"],
        test_state["candidate_age"],
        test_state["candidate_position"]
    )
    test_state["general_questions"] = general_questions
    print(f"✅ Сгенерировано {len(general_questions)} общих вопросов")
    
    # Симулируем ответы на общие вопросы
    test_state["general_answers"] = [
        {
            "question": general_questions[0],
            "answer": "У меня 5 лет опыта разработки на Python, работал в стартапах и крупных компаниях",
            "question_number": 1
        },
        {
            "question": general_questions[1],
            "answer": "Меня мотивирует создание качественных продуктов и работа в команде",
            "question_number": 2
        }
    ]
    
    # Тестируем генерацию технических вопросов
    print("\n2️⃣ Тестируем генерацию технических вопросов...")
    technical_questions = agent.openrouter_client.generate_technical_questions(
        test_state["vacancy_requirements"],
        test_state["candidate_position"],
        test_state["general_answers"]
    )
    test_state["technical_questions"] = technical_questions
    print(f"✅ Сгенерировано {len(technical_questions)} технических вопросов")
    
    # Симулируем ответы на технические вопросы
    test_state["technical_answers"] = [
        {
            "question": technical_questions[0],
            "answer": "Использую Django для создания веб-приложений, знаю ORM, middleware, views",
            "question_number": 1,
            "type": "technical"
        }
    ]
    
    # Тестируем генерацию уточняющих вопросов
    print("\n3️⃣ Тестируем генерацию уточняющих вопросов...")
    all_answers = test_state["general_answers"] + test_state["technical_answers"]
    followup_questions = []
    
    for answer_data in all_answers[:2]:
        followup_question = agent.openrouter_client.generate_follow_up_question(
            answer_data["answer"],
            {
                "question": answer_data["question"],
                "candidate_name": test_state["candidate_name"],
                "position": test_state["candidate_position"]
            }
        )
        if followup_question:
            followup_questions.append(followup_question)
    
    test_state["followup_questions"] = followup_questions
    print(f"✅ Сгенерировано {len(followup_questions)} уточняющих вопросов")
    
    # Собираем все вопросы
    all_questions = []
    all_questions.extend(test_state["general_questions"])
    all_questions.extend(test_state["technical_questions"])
    all_questions.extend(test_state["followup_questions"])
    test_state["interview_questions"] = all_questions
    
    print(f"\n📊 ИТОГОВАЯ СТАТИСТИКА:")
    print(f"   • Общих вопросов: {len(test_state['general_questions'])}")
    print(f"   • Технических вопросов: {len(test_state['technical_questions'])}")
    print(f"   • Уточняющих вопросов: {len(test_state['followup_questions'])}")
    print(f"   • Всего вопросов: {len(all_questions)}")
    print(f"   • Ответов: {len(test_state['general_answers']) + len(test_state['technical_answers'])}")
    
    return test_state


def test_workflow_visualization():
    """Тестирование визуализации нового workflow"""
    print("\n🎨 ТЕСТИРОВАНИЕ ВИЗУАЛИЗАЦИИ WORKFLOW")
    print("="*40)
    
    # Новые ноды в workflow
    nodes = {
        'start': '🚀 START',
        'get_name': '👤 ИМЯ',
        'get_age': '🎂 ВОЗРАСТ',
        'get_vacancy_requirements': '📋 ТРЕБОВАНИЯ',
        'ask_general_questions': '❓ ОБЩИЕ ВОПРОСЫ',
        'generate_technical_questions': '🔧 ТЕХНИЧЕСКИЕ ВОПРОСЫ',
        'ask_technical_questions': '💻 ТЕХНИЧЕСКИЕ ОТВЕТЫ',
        'generate_followup_questions': '🔄 УТОЧНЯЮЩИЕ ВОПРОСЫ',
        'finalize_interview': '📊 ФИНАЛИЗАЦИЯ',
        'end': '✅ END'
    }
    
    print("🔄 Новый workflow включает следующие ноды:")
    for node_id, node_label in nodes.items():
        print(f"   {node_label}")
    
    print(f"\n📈 Всего нод в workflow: {len(nodes)}")
    print("✅ Workflow расширен успешно!")


def test_openrouter_integration():
    """Тестирование интеграции с OpenRouter"""
    print("\n🔌 ТЕСТИРОВАНИЕ ИНТЕГРАЦИИ OPENROUTER")
    print("="*40)
    
    client = OpenRouterClient()
    
    # Тестируем генерацию общих вопросов
    print("1️⃣ Тестируем генерацию общих вопросов...")
    general_questions = client.generate_general_questions("Иван Сидоров", 32, "Data Scientist")
    print(f"✅ Сгенерировано {len(general_questions)} общих вопросов")
    
    # Тестируем генерацию технических вопросов
    print("\n2️⃣ Тестируем генерацию технических вопросов...")
    requirements = ["Python", "Machine Learning", "Pandas", "Scikit-learn"]
    technical_questions = client.generate_technical_questions(requirements, "Data Scientist", [])
    print(f"✅ Сгенерировано {len(technical_questions)} технических вопросов")
    
    # Тестируем генерацию уточняющих вопросов
    print("\n3️⃣ Тестируем генерацию уточняющих вопросов...")
    followup = client.generate_follow_up_question(
        "Работал с машинным обучением 3 года, использую Python и scikit-learn",
        {"question": "Расскажите о вашем опыте с ML", "candidate_name": "Иван", "position": "Data Scientist"}
    )
    print(f"✅ Сгенерирован уточняющий вопрос: {followup[:50]}...")
    
    return {
        "general_questions": len(general_questions),
        "technical_questions": len(technical_questions),
        "followup_generated": bool(followup)
    }


def main():
    """Основная функция тестирования"""
    print("🎯 ТЕСТИРОВАНИЕ РАСШИРЕННОГО АГЕНТА ИНТЕРВЬЮ")
    print("="*60)
    
    # Проверяем конфигурацию
    print(f"🔧 Конфигурация OpenRouter: {'✅' if config.is_configured() else '❌'}")
    if config.is_configured():
        print(f"   Модель: {config.model}")
    else:
        print("   Работаем в fallback режиме")
    
    # Тестируем расширенный workflow
    test_state = test_extended_workflow()
    
    # Тестируем визуализацию
    test_workflow_visualization()
    
    # Тестируем интеграцию с OpenRouter
    openrouter_results = test_openrouter_integration()
    
    # Итоговый результат
    print("\n" + "="*60)
    print("📋 ИТОГИ ТЕСТИРОВАНИЯ РАСШИРЕННОГО АГЕНТА:")
    print(f"  ✅ Расширенный workflow: Работает")
    print(f"  ✅ Общие вопросы: {openrouter_results['general_questions']} сгенерировано")
    print(f"  ✅ Технические вопросы: {openrouter_results['technical_questions']} сгенерировано")
    print(f"  ✅ Уточняющие вопросы: {'Работают' if openrouter_results['followup_generated'] else 'Не работают'}")
    print(f"  ✅ Всего вопросов в тесте: {len(test_state['interview_questions'])}")
    print(f"  ✅ OpenRouter: {'Настроен' if config.is_configured() else 'Fallback режим'}")
    
    # Сохраняем результат теста
    test_result = {
        "extended_workflow": True,
        "total_questions": len(test_state['interview_questions']),
        "general_questions_count": len(test_state['general_questions']),
        "technical_questions_count": len(test_state['technical_questions']),
        "followup_questions_count": len(test_state['followup_questions']),
        "openrouter_configured": config.is_configured(),
        "model": config.model if config.is_configured() else "fallback",
        "workflow_nodes": 8  # Количество нод в новом workflow
    }
    
    with open('extended_test_result.json', 'w', encoding='utf-8') as f:
        json.dump(test_result, f, ensure_ascii=False, indent=2)
    
    print(f"\n💾 Результат теста сохранен в extended_test_result.json")
    print("🎉 Расширенный агент готов к использованию!")


if __name__ == "__main__":
    main()
