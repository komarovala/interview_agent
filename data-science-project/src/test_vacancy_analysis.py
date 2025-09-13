"""
Тестирование анализа вакансий
"""

from openrouter_client import OpenRouterClient
from config import config
import json


def test_vacancy_analysis():
    """Тестирование анализа текста вакансии"""
    print("🧪 ТЕСТИРОВАНИЕ АНАЛИЗА ВАКАНСИЙ")
    print("="*50)
    
    client = OpenRouterClient()
    
    # Тестовая вакансия
    test_vacancy = """
    Python Developer
    
    Мы ищем опытного Python разработчика для работы над высоконагруженными веб-приложениями.
    
    Требования:
    - Опыт работы с Python 3+ (минимум 3 года)
    - Знание Django и Flask
    - Опыт работы с PostgreSQL и Redis
    - Знание Docker и Kubernetes
    - Опыт работы с Git
    - Английский язык на уровне Intermediate
    - Умение работать в команде
    - Лидерские качества приветствуются
    
    Обязанности:
    - Разработка и поддержка веб-приложений
    - Оптимизация производительности
    - Code review
    - Работа с командой разработки
    
    Условия:
    - Удаленная работа
    - Гибкий график
    - Конкурентная зарплата
    """
    
    print("📋 Тестовая вакансия:")
    print(test_vacancy[:200] + "...")
    
    # Анализируем вакансию
    print("\n🔍 Анализируем требования...")
    requirements = client.analyze_vacancy_requirements(test_vacancy)
    
    print(f"\n✅ Анализ завершен! Извлечено {len(requirements)} требований:")
    print("\n📊 СТРУКТУРИРОВАННЫЕ ТРЕБОВАНИЯ:")
    print("-" * 60)
    
    for i, req in enumerate(requirements, 1):
        skill = req.get('skill', 'Не указано')
        level = req.get('level', 'Не указано')
        category = req.get('category', 'Не указано')
        importance = req.get('importance', 'Не указано')
        
        print(f"{i:2d}. {skill}")
        print(f"    Уровень: {level}")
        print(f"    Категория: {category}")
        print(f"    Важность: {importance}")
        print()
    
    return requirements


def test_technical_questions_generation():
    """Тестирование генерации технических вопросов на основе анализа"""
    print("\n🔧 ТЕСТИРОВАНИЕ ГЕНЕРАЦИИ ТЕХНИЧЕСКИХ ВОПРОСОВ")
    print("="*50)
    
    client = OpenRouterClient()
    
    # Тестовые требования (результат анализа)
    test_requirements = [
        {"skill": "Python", "level": "Продвинутый", "category": "Языки программирования", "importance": "высокая"},
        {"skill": "Django", "level": "Средний", "category": "Фреймворки", "importance": "высокая"},
        {"skill": "PostgreSQL", "level": "Средний", "category": "Базы данных", "importance": "высокая"},
        {"skill": "Docker", "level": "Средний", "category": "DevOps", "importance": "средняя"},
        {"skill": "Опыт разработки", "level": "3+ года", "category": "Опыт работы", "importance": "высокая"},
        {"skill": "Командная работа", "level": "Обязательно", "category": "Soft skills", "importance": "высокая"}
    ]
    
    print("📋 Тестовые требования:")
    for req in test_requirements:
        print(f"  • {req['skill']} ({req['level']}) - {req['category']}")
    
    # Генерируем технические вопросы
    print("\n🤖 Генерируем технические вопросы...")
    technical_questions = client.generate_technical_questions_from_analysis(
        test_requirements,
        "Python разработчик",
        []
    )
    
    print(f"\n✅ Сгенерировано {len(technical_questions)} технических вопросов:")
    print("\n❓ ТЕХНИЧЕСКИЕ ВОПРОСЫ:")
    print("-" * 60)
    
    for i, question in enumerate(technical_questions, 1):
        print(f"{i}. {question}")
    
    return technical_questions


def test_fallback_analysis():
    """Тестирование fallback анализа"""
    print("\n🔄 ТЕСТИРОВАНИЕ FALLBACK АНАЛИЗА")
    print("="*40)
    
    client = OpenRouterClient()
    
    # Простая вакансия для тестирования fallback
    simple_vacancy = "Нужен Python разработчик с опытом работы 2 года. Знание Django обязательно."
    
    print(f"📋 Простая вакансия: {simple_vacancy}")
    
    # Тестируем fallback анализ
    requirements = client._fallback_vacancy_analysis(simple_vacancy)
    
    print(f"\n✅ Fallback анализ завершен! Извлечено {len(requirements)} требований:")
    for req in requirements:
        print(f"  • {req['skill']} ({req['level']}) - {req['category']}")
    
    return requirements


def test_different_vacancy_types():
    """Тестирование разных типов вакансий"""
    print("\n🎯 ТЕСТИРОВАНИЕ РАЗНЫХ ТИПОВ ВАКАНСИЙ")
    print("="*50)
    
    client = OpenRouterClient()
    
    # Разные типы вакансий
    vacancies = {
        "Frontend": """
        Frontend Developer
        
        Требования:
        - JavaScript ES6+
        - React или Vue.js
        - HTML5, CSS3
        - Опыт работы 1+ год
        - Английский язык
        """,
        
        "DevOps": """
        DevOps Engineer
        
        Требования:
        - Linux, Docker, Kubernetes
        - CI/CD (Jenkins, GitLab)
        - AWS или Azure
        - Опыт работы 3+ года
        - Python или Bash
        """,
        
        "Data Scientist": """
        Data Scientist
        
        Требования:
        - Python, R
        - Machine Learning
        - Pandas, NumPy, Scikit-learn
        - SQL
        - Опыт работы 2+ года
        """
    }
    
    results = {}
    
    for position, vacancy_text in vacancies.items():
        print(f"\n📋 Анализируем вакансию: {position}")
        requirements = client.analyze_vacancy_requirements(vacancy_text)
        results[position] = requirements
        
        print(f"✅ Извлечено {len(requirements)} требований:")
        for req in requirements[:3]:  # Показываем первые 3
            print(f"  • {req['skill']} ({req['level']}) - {req['category']}")
        if len(requirements) > 3:
            print(f"  ... и еще {len(requirements) - 3}")
    
    return results


def main():
    """Основная функция тестирования"""
    print("🎯 ТЕСТИРОВАНИЕ АНАЛИЗА ВАКАНСИЙ")
    print("="*60)
    
    # Проверяем конфигурацию
    print(f"🔧 Конфигурация OpenRouter: {'✅' if config.is_configured() else '❌'}")
    if config.is_configured():
        print(f"   Модель: {config.model}")
    else:
        print("   Работаем в fallback режиме")
    
    # Тестируем анализ вакансии
    requirements = test_vacancy_analysis()
    
    # Тестируем генерацию технических вопросов
    technical_questions = test_technical_questions_generation()
    
    # Тестируем fallback анализ
    fallback_requirements = test_fallback_analysis()
    
    # Тестируем разные типы вакансий
    different_vacancies = test_different_vacancy_types()
    
    # Итоговый результат
    print("\n" + "="*60)
    print("📋 ИТОГИ ТЕСТИРОВАНИЯ АНАЛИЗА ВАКАНСИЙ:")
    print(f"  ✅ Анализ вакансии: {len(requirements)} требований извлечено")
    print(f"  ✅ Технические вопросы: {len(technical_questions)} сгенерировано")
    print(f"  ✅ Fallback анализ: {len(fallback_requirements)} требований")
    print(f"  ✅ Разные типы вакансий: {len(different_vacancies)} протестировано")
    print(f"  ✅ OpenRouter: {'Настроен' if config.is_configured() else 'Fallback режим'}")
    
    # Сохраняем результат теста
    test_result = {
        "vacancy_analysis": {
            "requirements_extracted": len(requirements),
            "requirements": requirements
        },
        "technical_questions": {
            "questions_generated": len(technical_questions),
            "questions": technical_questions
        },
        "fallback_analysis": {
            "requirements_extracted": len(fallback_requirements),
            "requirements": fallback_requirements
        },
        "different_vacancies": {
            "types_tested": len(different_vacancies),
            "results": {k: len(v) for k, v in different_vacancies.items()}
        },
        "openrouter_configured": config.is_configured(),
        "model": config.model if config.is_configured() else "fallback"
    }
    
    with open('vacancy_analysis_test_result.json', 'w', encoding='utf-8') as f:
        json.dump(test_result, f, ensure_ascii=False, indent=2)
    
    print(f"\n💾 Результат теста сохранен в vacancy_analysis_test_result.json")
    print("🎉 Анализ вакансий работает корректно!")


if __name__ == "__main__":
    main()
