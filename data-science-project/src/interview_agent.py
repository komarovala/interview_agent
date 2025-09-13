"""
Агент для генерации сценария интервью с использованием LangGraph и OpenRouter.ai
"""

from typing import Dict, Any, List
from langgraph.graph import StateGraph, END
from langchain_core.messages import HumanMessage, AIMessage
import json
from openrouter_client import OpenRouterClient
from config import config


class InterviewState:
    """Состояние агента интервью"""
    def __init__(self):
        self.messages: List[Dict[str, str]] = []
        self.candidate_name: str = ""
        self.candidate_age: int = 0
        self.candidate_position: str = "разработчик"
        self.vacancy_text: str = ""
        self.vacancy_requirements: List[Dict[str, Any]] = []
        self.general_questions: List[str] = []
        self.general_answers: List[Dict[str, str]] = []
        self.technical_questions: List[str] = []
        self.technical_answers: List[Dict[str, str]] = []
        self.followup_questions: List[str] = []
        self.interview_questions: List[str] = []
        self.current_step: str = "start"
        self.ai_responses: List[str] = []
        self.analysis_results: List[Dict[str, Any]] = []
    
    def add_message(self, role: str, content: str):
        """Добавить сообщение в историю"""
        self.messages.append({"role": role, "content": content})
    
    def to_dict(self) -> Dict[str, Any]:
        """Преобразовать состояние в словарь"""
        return {
            "messages": self.messages,
            "candidate_name": self.candidate_name,
            "candidate_age": self.candidate_age,
            "candidate_position": self.candidate_position,
            "vacancy_text": self.vacancy_text,
            "vacancy_requirements": self.vacancy_requirements,
            "general_questions": self.general_questions,
            "general_answers": self.general_answers,
            "technical_questions": self.technical_questions,
            "technical_answers": self.technical_answers,
            "followup_questions": self.followup_questions,
            "interview_questions": self.interview_questions,
            "current_step": self.current_step,
            "ai_responses": self.ai_responses,
            "analysis_results": self.analysis_results
        }


class InterviewAgent:
    """Агент для проведения интервью"""
    
    def __init__(self):
        self.state = InterviewState()
        self.openrouter_client = OpenRouterClient()
        self.graph = self._create_graph()
    
    def _create_graph(self) -> StateGraph:
        """Создать граф с нодами для интервью"""
        
        # Создаем граф с типом состояния как словарь
        workflow = StateGraph(dict)
        
        # Добавляем ноды
        workflow.add_node("get_name", self._get_name_node)
        workflow.add_node("get_age", self._get_age_node)
        workflow.add_node("get_vacancy_requirements", self._get_vacancy_requirements_node)
        workflow.add_node("ask_general_questions", self._ask_general_questions_node)
        workflow.add_node("generate_technical_questions", self._generate_technical_questions_node)
        workflow.add_node("ask_technical_questions", self._ask_technical_questions_node)
        workflow.add_node("generate_followup_questions", self._generate_followup_questions_node)
        workflow.add_node("finalize_interview", self._finalize_interview_node)
        
        # Определяем поток выполнения
        workflow.set_entry_point("get_name")
        workflow.add_edge("get_name", "get_age")
        workflow.add_edge("get_age", "get_vacancy_requirements")
        workflow.add_edge("get_vacancy_requirements", "ask_general_questions")
        workflow.add_edge("ask_general_questions", "generate_technical_questions")
        workflow.add_edge("generate_technical_questions", "ask_technical_questions")
        workflow.add_edge("ask_technical_questions", "generate_followup_questions")
        workflow.add_edge("generate_followup_questions", "finalize_interview")
        workflow.add_edge("finalize_interview", END)
        
        return workflow.compile()
    
    def _get_name_node(self, state: dict) -> dict:
        """Нода для получения имени кандидата"""
        # Инициализируем состояние, если оно пустое
        if not state:
            state = {
                "messages": [],
                "candidate_name": "",
                "candidate_age": 0,
                "candidate_position": "разработчик",
                "vacancy_text": "",
                "vacancy_requirements": [],
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
        
        # Генерируем приветствие через OpenRouter
        welcome_messages = [
            {"role": "system", "content": "Ты - дружелюбный HR-специалист, который проводит интервью. Поприветствуй кандидата и спроси его имя."},
            {"role": "user", "content": "Начни интервью"}
        ]
        
        ai_response = self.openrouter_client.generate_response(welcome_messages)
        if ai_response:
            print(f"🤖 Агент: {ai_response}")
            state["ai_responses"].append(ai_response)
        else:
            print("🤖 Агент: Добро пожаловать на интервью! Меня зовут InterviewBot.")
            print("🤖 Агент: Для начала, как вас зовут?")
        
        # Получаем имя от пользователя
        name = input("👤 Ваш ответ: ").strip()
        
        if name:
            state["candidate_name"] = name
            state["messages"].append({"role": "assistant", "content": f"Приятно познакомиться, {name}!"})
            state["messages"].append({"role": "user", "content": name})
            state["current_step"] = "name_collected"
            print(f"🤖 Агент: Приятно познакомиться, {name}!")
        else:
            state["messages"].append({"role": "assistant", "content": "Пожалуйста, введите ваше имя."})
            print("🤖 Агент: Пожалуйста, введите ваше имя.")
        
        return state
    
    def _get_age_node(self, state: dict) -> dict:
        """Нода для получения возраста кандидата"""
        # Генерируем вопрос о возрасте через OpenRouter
        age_messages = [
            {"role": "system", "content": f"Ты - HR-специалист. Вежливо спроси у кандидата {state.get('candidate_name', '')} его возраст."},
            {"role": "user", "content": "Спроси возраст кандидата"}
        ]
        
        ai_response = self.openrouter_client.generate_response(age_messages)
        if ai_response:
            print(f"🤖 Агент: {ai_response}")
            state["ai_responses"].append(ai_response)
        else:
            print("🤖 Агент: Скажите, пожалуйста, сколько вам лет?")
        
        # Получаем возраст от пользователя
        while True:
            try:
                age_input = input("👤 Ваш ответ: ").strip()
                age = int(age_input)
                
                if age > 0 and age < 100:
                    state["candidate_age"] = age
                    state["messages"].append({"role": "assistant", "content": f"Спасибо! Вам {age} лет."})
                    state["messages"].append({"role": "user", "content": str(age)})
                    state["current_step"] = "age_collected"
                    print(f"🤖 Агент: Спасибо! Вам {age} лет.")
                    break
                else:
                    print("🤖 Агент: Пожалуйста, введите корректный возраст (от 1 до 99 лет).")
            except ValueError:
                print("🤖 Агент: Пожалуйста, введите возраст числом.")
        
        return state
    
    def _get_vacancy_requirements_node(self, state: dict) -> dict:
        """Нода для получения и анализа текста вакансии"""
        print("\n🤖 Агент: Теперь мне нужен полный текст вакансии для анализа.")
        print("🤖 Агент: Пожалуйста, вставьте текст вакансии:")
        print("   (включая описание, требования, обязанности, условия)")
        
        # Получаем текст вакансии от пользователя
        print("\n📝 Введите текст вакансии (завершите ввод пустой строкой):")
        vacancy_lines = []
        while True:
            line = input()
            if line.strip() == "":
                break
            vacancy_lines.append(line)
        
        vacancy_text = "\n".join(vacancy_lines).strip()
        
        if vacancy_text:
            state["vacancy_text"] = vacancy_text
            state["messages"].append({"role": "assistant", "content": "Получил текст вакансии, анализирую требования..."})
            state["messages"].append({"role": "user", "content": f"Текст вакансии: {vacancy_text[:100]}..."})
            
            # Анализируем требования через OpenRouter
            print("🤖 Агент: Анализирую текст вакансии и извлекаю требования...")
            analyzed_requirements = self.openrouter_client.analyze_vacancy_requirements(vacancy_text)
            state["vacancy_requirements"] = analyzed_requirements
            state["current_step"] = "vacancy_requirements_collected"
            
            print(f"✅ Анализ завершен! Извлечено {len(analyzed_requirements)} требований:")
            for i, req in enumerate(analyzed_requirements[:5], 1):
                print(f"   {i}. {req.get('skill', '')} - {req.get('level', '')} ({req.get('category', '')})")
            
            if len(analyzed_requirements) > 5:
                print(f"   ... и еще {len(analyzed_requirements) - 5} требований")
        else:
            # Используем базовые требования
            default_requirements = [
                {"skill": "Python", "level": "Средний", "category": "Языки программирования"},
                {"skill": "Опыт разработки", "level": "2+ года", "category": "Опыт работы"},
                {"skill": "Знание баз данных", "level": "Базовый", "category": "Технологии"},
                {"skill": "Командная работа", "level": "Обязательно", "category": "Soft skills"}
            ]
            state["vacancy_requirements"] = default_requirements
            state["vacancy_text"] = "Стандартные требования для разработчика"
            state["current_step"] = "vacancy_requirements_collected"
            print("🤖 Агент: Буду использовать стандартные требования для разработчика.")
        
        return state
    
    def _ask_general_questions_node(self, state: dict) -> dict:
        """Нода для общих вопросов"""
        print("\n🤖 Агент: Начнем с общих вопросов о вашем опыте.")
        
        # Генерируем общие вопросы через OpenRouter
        general_questions = self.openrouter_client.generate_general_questions(
            state.get("candidate_name", ""),
            state.get("candidate_age", 0),
            state.get("candidate_position", "разработчик")
        )
        state["general_questions"] = general_questions
        
        # Задаем вопросы и собираем ответы
        for i, question in enumerate(general_questions[:3], 1):  # Берем первые 3 вопроса
            print(f"\n❓ Вопрос {i}: {question}")
            answer = input("👤 Ваш ответ: ").strip()
            
            if answer:
                state["general_answers"].append({
                    "question": question,
                    "answer": answer,
                    "question_number": i
                })
                state["messages"].append({"role": "user", "content": f"Вопрос {i}: {answer}"})
                print("🤖 Агент: Спасибо за ответ!")
            else:
                print("🤖 Агент: Пропускаем этот вопрос.")
        
        state["current_step"] = "general_questions_completed"
        print(f"\n✅ Общие вопросы завершены. Собрано {len(state['general_answers'])} ответов.")
        
        return state
    
    def _generate_technical_questions_node(self, state: dict) -> dict:
        """Нода для генерации технических вопросов на основе вакансии"""
        print("\n🤖 Агент: Теперь сгенерирую технические вопросы на основе требований вакансии.")
        
        # Генерируем технические вопросы через OpenRouter
        technical_questions = self.openrouter_client.generate_technical_questions_from_analysis(
            state.get("vacancy_requirements", []),
            state.get("candidate_position", "разработчик"),
            state.get("general_answers", [])
        )
        state["technical_questions"] = technical_questions
        
        state["current_step"] = "technical_questions_generated"
        print(f"✅ Сгенерировано {len(technical_questions)} технических вопросов.")
        
        return state
    
    def _ask_technical_questions_node(self, state: dict) -> dict:
        """Нода для технических вопросов"""
        print("\n🤖 Агент: Переходим к техническим вопросам.")
        
        technical_questions = state.get("technical_questions", [])
        
        # Задаем технические вопросы
        for i, question in enumerate(technical_questions[:4], 1):  # Берем первые 4 вопроса
            print(f"\n🔧 Технический вопрос {i}: {question}")
            answer = input("👤 Ваш ответ: ").strip()
            
            if answer:
                state["technical_answers"].append({
                    "question": question,
                    "answer": answer,
                    "question_number": i,
                    "type": "technical"
                })
                state["messages"].append({"role": "user", "content": f"Технический вопрос {i}: {answer}"})
                print("🤖 Агент: Отличный ответ!")
            else:
                print("🤖 Агент: Пропускаем этот вопрос.")
        
        state["current_step"] = "technical_questions_completed"
        print(f"\n✅ Технические вопросы завершены. Собрано {len(state['technical_answers'])} ответов.")
        
        return state
    
    def _generate_followup_questions_node(self, state: dict) -> dict:
        """Нода для генерации уточняющих вопросов на основе ответов"""
        print("\n🤖 Агент: Анализирую ваши ответы и генерирую уточняющие вопросы.")
        
        # Генерируем уточняющие вопросы на основе всех ответов
        all_answers = state.get("general_answers", []) + state.get("technical_answers", [])
        followup_questions = []
        
        for answer_data in all_answers[:3]:  # Берем первые 3 ответа для уточнения
            followup_question = self.openrouter_client.generate_follow_up_question(
                answer_data["answer"],
                {
                    "question": answer_data["question"],
                    "candidate_name": state.get("candidate_name", ""),
                    "position": state.get("candidate_position", "")
                }
            )
            if followup_question:
                followup_questions.append(followup_question)
        
        state["followup_questions"] = followup_questions
        state["current_step"] = "followup_questions_generated"
        print(f"✅ Сгенерировано {len(followup_questions)} уточняющих вопросов.")
        
        return state
    
    def _finalize_interview_node(self, state: dict) -> dict:
        """Нода для финализации интервью"""
        print("\n🤖 Агент: Завершаем интервью. Создаю итоговый отчет.")
        
        # Собираем все вопросы в один список
        all_questions = []
        all_questions.extend(state.get("general_questions", []))
        all_questions.extend(state.get("technical_questions", []))
        all_questions.extend(state.get("followup_questions", []))
        
        state["interview_questions"] = all_questions
        state["current_step"] = "interview_completed"
        
        # Создаем итоговый отчет
        self._create_interview_report(state)
        
        return state
    
    def _generate_questions_node(self, state: dict) -> dict:
        """Нода для генерации вопросов интервью"""
        print("🤖 Агент: Отлично! Теперь я сгенерирую персональные вопросы для интервью.")
        
        # Генерируем вопросы через OpenRouter
        questions = self.openrouter_client.generate_interview_questions(
            state.get("candidate_name", ""), 
            state.get("candidate_age", 0), 
            state.get("candidate_position", "разработчик")
        )
        state["interview_questions"] = questions
        
        state["messages"].append({"role": "assistant", "content": "Вот ваш персональный сценарий интервью:"})
        state["current_step"] = "questions_generated"
        
        print("\n" + "="*50)
        print("📋 ПЕРСОНАЛЬНЫЙ СЦЕНАРИЙ ИНТЕРВЬЮ")
        print("="*50)
        print(f"👤 Кандидат: {state.get('candidate_name', '')}")
        print(f"🎂 Возраст: {state.get('candidate_age', 0)} лет")
        print(f"💼 Позиция: {state.get('candidate_position', 'разработчик')}")
        print("\n📝 Вопросы для интервью:")
        
        for i, question in enumerate(questions, 1):
            print(f"{i}. {question}")
        
        print("\n🤖 Агент: Удачи на интервью!")
        print("="*50)
        
        return state
    
    def _create_interview_report(self, state: dict):
        """Создать итоговый отчет интервью"""
        print("\n" + "="*60)
        print("📋 ИТОГОВЫЙ ОТЧЕТ ИНТЕРВЬЮ")
        print("="*60)
        
        print(f"👤 Кандидат: {state.get('candidate_name', '')}")
        print(f"🎂 Возраст: {state.get('candidate_age', 0)} лет")
        print(f"💼 Позиция: {state.get('candidate_position', '')}")
        requirements = state.get('vacancy_requirements', [])
        if requirements and isinstance(requirements[0], dict):
            requirements_text = ', '.join([f"{req.get('skill', '')} ({req.get('level', '')})" for req in requirements[:3]])
            if len(requirements) > 3:
                requirements_text += f" и еще {len(requirements) - 3}"
        else:
            requirements_text = ', '.join(requirements) if requirements else "Не указаны"
        print(f"📋 Требования: {requirements_text}")
        
        print(f"\n📊 СТАТИСТИКА:")
        print(f"   • Общих вопросов: {len(state.get('general_questions', []))}")
        print(f"   • Технических вопросов: {len(state.get('technical_questions', []))}")
        print(f"   • Уточняющих вопросов: {len(state.get('followup_questions', []))}")
        print(f"   • Всего ответов: {len(state.get('general_answers', [])) + len(state.get('technical_answers', []))}")
        
        print(f"\n📝 ВСЕ ВОПРОСЫ ИНТЕРВЬЮ:")
        all_questions = []
        all_questions.extend(state.get("general_questions", []))
        all_questions.extend(state.get("technical_questions", []))
        all_questions.extend(state.get("followup_questions", []))
        
        for i, question in enumerate(all_questions, 1):
            print(f"{i}. {question}")
        
        print("\n🤖 Агент: Интервью завершено! Спасибо за участие!")
        print("="*60)
    
    def _generate_personalized_questions(self, name: str, age: int) -> List[str]:
        """Генерировать персональные вопросы на основе данных кандидата"""
        base_questions = [
            "Расскажите о себе и своем профессиональном опыте.",
            "Почему вы заинтересованы в этой позиции?",
            "Какие у вас сильные стороны?",
            "Опишите ситуацию, когда вам пришлось решать сложную задачу.",
            "Где вы видите себя через 5 лет?",
            "Есть ли у вас вопросы к нам?"
        ]
        
        # Персонализируем вопросы на основе возраста
        if age < 25:
            personalized_questions = [
                f"Привет, {name}! Как молодой специалист, расскажите о ваших образовательных достижениях.",
                "Какие проекты вы реализовали во время учебы или стажировок?",
                "Как вы планируете развивать свои навыки в нашей компании?"
            ]
        elif age < 35:
            personalized_questions = [
                f"Здравствуйте, {name}! Расскажите о вашем карьерном пути до сих пор.",
                "Какие проекты вы считаете наиболее значимыми в вашей карьере?",
                "Как вы видите свое развитие в нашей команде?"
            ]
        else:
            personalized_questions = [
                f"Добро пожаловать, {name}! Поделитесь своим богатым профессиональным опытом.",
                "Какие лидерские качества вы развили за годы работы?",
                "Как вы можете поделиться своим опытом с молодыми коллегами?"
            ]
        
        return personalized_questions + base_questions
    
    def run_interview(self):
        """Запустить процесс интервью"""
        print("🚀 Запуск агента интервью...")
        print("="*50)
        
        try:
            # Запускаем граф с пустым состоянием
            result = self.graph.invoke({})
            
            # Обновляем внутреннее состояние агента
            if result:
                self.state.messages = result.get("messages", [])
                self.state.candidate_name = result.get("candidate_name", "")
                self.state.candidate_age = result.get("candidate_age", 0)
                self.state.candidate_position = result.get("candidate_position", "разработчик")
                self.state.vacancy_text = result.get("vacancy_text", "")
                self.state.vacancy_requirements = result.get("vacancy_requirements", [])
                self.state.general_questions = result.get("general_questions", [])
                self.state.general_answers = result.get("general_answers", [])
                self.state.technical_questions = result.get("technical_questions", [])
                self.state.technical_answers = result.get("technical_answers", [])
                self.state.followup_questions = result.get("followup_questions", [])
                self.state.interview_questions = result.get("interview_questions", [])
                self.state.current_step = result.get("current_step", "start")
                self.state.ai_responses = result.get("ai_responses", [])
                self.state.analysis_results = result.get("analysis_results", [])
            
            return result
        except Exception as e:
            print(f"❌ Ошибка при выполнении интервью: {e}")
            return None
    
    def get_interview_summary(self) -> Dict[str, Any]:
        """Получить сводку интервью"""
        return {
            "candidate_name": self.state.candidate_name,
            "candidate_age": self.state.candidate_age,
            "candidate_position": self.state.candidate_position,
            "vacancy_text": self.state.vacancy_text,
            "vacancy_requirements": self.state.vacancy_requirements,
            "general_questions": self.state.general_questions,
            "general_answers": self.state.general_answers,
            "technical_questions": self.state.technical_questions,
            "technical_answers": self.state.technical_answers,
            "followup_questions": self.state.followup_questions,
            "total_questions": len(self.state.interview_questions),
            "questions": self.state.interview_questions,
            "conversation_history": self.state.messages,
            "ai_responses": self.state.ai_responses,
            "analysis_results": self.state.analysis_results,
            "openrouter_used": config.is_configured()
        }


def main():
    """Основная функция для запуска агента"""
    print("🎯 АГЕНТ ГЕНЕРАЦИИ СЦЕНАРИЯ ИНТЕРВЬЮ")
    print("Использует LangGraph для создания персональных вопросов")
    print("="*60)
    
    # Создаем и запускаем агента
    agent = InterviewAgent()
    result = agent.run_interview()
    
    if result:
        print("\n📊 СВОДКА ИНТЕРВЬЮ:")
        summary = agent.get_interview_summary()
        print(f"✅ Имя кандидата: {summary['candidate_name']}")
        print(f"✅ Возраст: {summary['candidate_age']}")
        print(f"✅ Количество вопросов: {summary['total_questions']}")
        print(f"✅ Статус: Интервью завершено успешно")


if __name__ == "__main__":
    main()
