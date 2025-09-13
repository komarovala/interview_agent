"""
Клиент для работы с OpenRouter.ai
"""

import requests
import json
from typing import List, Dict, Any, Optional
from config import config


class OpenRouterClient:
    """Клиент для взаимодействия с OpenRouter.ai"""
    
    def __init__(self):
        self.api_key = config.api_key
        self.base_url = config.base_url
        self.model = config.model
        self.headers = config.get_headers()
    
    def generate_response(self, messages: List[Dict[str, str]], temperature: float = 0.7) -> Optional[str]:
        """Генерировать ответ от языковой модели"""
        
        if not config.is_configured():
            return self._get_fallback_response(messages)
        
        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": 1000,
            "top_p": 0.9,
            "frequency_penalty": 0.1,
            "presence_penalty": 0.1
        }
        
        try:
            response = requests.post(
                f"{self.base_url}/chat/completions",
                headers=self.headers,
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                return data['choices'][0]['message']['content']
            else:
                print(f"❌ Ошибка API: {response.status_code} - {response.text}")
                return self._get_fallback_response(messages)
                
        except Exception as e:
            print(f"❌ Ошибка при обращении к OpenRouter: {e}")
            return self._get_fallback_response(messages)
    
    def _get_fallback_response(self, messages: List[Dict[str, str]]) -> str:
        """Fallback ответ, если API недоступен"""
        last_message = messages[-1]['content'] if messages else ""
        
        if "имя" in last_message.lower() or "зовут" in last_message.lower():
            return "Приятно познакомиться! Теперь расскажите, сколько вам лет?"
        elif "возраст" in last_message.lower() or "лет" in last_message.lower():
            return "Отлично! Теперь я сгенерирую персональные вопросы для вашего интервью."
        else:
            return "Спасибо за информацию! Продолжаем интервью."
    
    def generate_interview_questions(self, name: str, age: int, position: str = "разработчик") -> List[str]:
        """Генерировать персональные вопросы для интервью"""
        
        system_prompt = f"""Ты - опытный HR-специалист, который проводит интервью для позиции {position}.
Создай персональные вопросы для кандидата по имени {name}, возраст {age} лет.
Вопросы должны быть:
1. Релевантными для возраста кандидата
2. Профессиональными
3. Разнообразными (технические, поведенческие, мотивационные)
4. На русском языке

Верни только список вопросов, каждый с новой строки, без нумерации."""

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Создай 8-10 вопросов для интервью с {name}, {age} лет, на позицию {position}"}
        ]
        
        response = self.generate_response(messages, temperature=0.8)
        
        if response:
            # Парсим ответ в список вопросов
            questions = [q.strip() for q in response.split('\n') if q.strip()]
            return questions[:10]  # Ограничиваем до 10 вопросов
        else:
            return self._get_default_questions(name, age)
    
    def _get_default_questions(self, name: str, age: int) -> List[str]:
        """Запасные вопросы, если API недоступен"""
        base_questions = [
            f"Привет, {name}! Расскажите о себе и своем профессиональном опыте.",
            "Почему вы заинтересованы в этой позиции?",
            "Какие у вас сильные стороны?",
            "Опишите ситуацию, когда вам пришлось решать сложную задачу.",
            "Где вы видите себя через 5 лет?",
            "Есть ли у вас вопросы к нам?"
        ]
        
        if age < 25:
            personalized = [
                "Какие проекты вы реализовали во время учебы?",
                "Как вы планируете развивать свои навыки?"
            ]
        elif age < 35:
            personalized = [
                "Расскажите о вашем карьерном пути.",
                "Какие проекты вы считаете наиболее значимыми?"
            ]
        else:
            personalized = [
                "Поделитесь своим богатым профессиональным опытом.",
                "Какие лидерские качества вы развили?"
            ]
        
        return personalized + base_questions
    
    def generate_follow_up_question(self, previous_answer: str, context: Dict[str, Any]) -> str:
        """Генерировать уточняющий вопрос на основе предыдущего ответа"""
        
        system_prompt = """Ты - опытный интервьюер. На основе ответа кандидата сформулируй один уточняющий вопрос.
Вопрос должен быть:
1. Релевантным к предыдущему ответу
2. Помогающим лучше понять кандидата
3. На русском языке
4. Профессиональным

Верни только вопрос, без дополнительных комментариев."""
        
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Ответ кандидата: {previous_answer}\nКонтекст: {context}\nСформулируй уточняющий вопрос."}
        ]
        
        response = self.generate_response(messages, temperature=0.7)
        return response if response else "Можете рассказать об этом подробнее?"
    
    def analyze_vacancy_requirements(self, vacancy_text: str) -> List[Dict[str, Any]]:
        """Анализировать текст вакансии и извлекать структурированные требования"""
        
        system_prompt = """Ты - опытный HR-аналитик. Проанализируй текст вакансии и извлеки структурированные требования.

Для каждого требования определи:
1. Навык/технологию
2. Уровень владения (Начинающий, Средний, Продвинутый, Эксперт)
3. Категорию (Языки программирования, Фреймворки, Базы данных, Опыт работы, Soft skills, Другое)

Верни результат в формате JSON массива:
[
    {
        "skill": "название навыка",
        "level": "уровень владения",
        "category": "категория",
        "importance": "высокая/средняя/низкая"
    }
]"""
        
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Проанализируй вакансию и извлеки требования:\n\n{vacancy_text}"}
        ]
        
        response = self.generate_response(messages, temperature=0.3)
        
        try:
            if response:
                requirements = json.loads(response)
                if isinstance(requirements, list):
                    return requirements[:15]  # Ограничиваем до 15 требований
        except json.JSONDecodeError:
            pass
        
        # Fallback анализ
        return self._fallback_vacancy_analysis(vacancy_text)
    
    def _fallback_vacancy_analysis(self, vacancy_text: str) -> List[Dict[str, Any]]:
        """Fallback анализ вакансии на основе ключевых слов"""
        requirements = []
        text_lower = vacancy_text.lower()
        
        # Анализируем технологии
        tech_keywords = {
            "python": {"skill": "Python", "level": "Средний", "category": "Языки программирования"},
            "java": {"skill": "Java", "level": "Средний", "category": "Языки программирования"},
            "javascript": {"skill": "JavaScript", "level": "Средний", "category": "Языки программирования"},
            "django": {"skill": "Django", "level": "Средний", "category": "Фреймворки"},
            "flask": {"skill": "Flask", "level": "Средний", "category": "Фреймворки"},
            "react": {"skill": "React", "level": "Средний", "category": "Фреймворки"},
            "postgresql": {"skill": "PostgreSQL", "level": "Средний", "category": "Базы данных"},
            "mysql": {"skill": "MySQL", "level": "Средний", "category": "Базы данных"},
            "mongodb": {"skill": "MongoDB", "level": "Средний", "category": "Базы данных"},
            "docker": {"skill": "Docker", "level": "Средний", "category": "DevOps"},
            "kubernetes": {"skill": "Kubernetes", "level": "Продвинутый", "category": "DevOps"},
            "git": {"skill": "Git", "level": "Средний", "category": "Инструменты разработки"}
        }
        
        for keyword, req_data in tech_keywords.items():
            if keyword in text_lower:
                requirements.append({
                    "skill": req_data["skill"],
                    "level": req_data["level"],
                    "category": req_data["category"],
                    "importance": "высокая"
                })
        
        # Анализируем опыт работы
        if "опыт" in text_lower or "стаж" in text_lower:
            if "1" in vacancy_text or "год" in text_lower:
                requirements.append({
                    "skill": "Опыт разработки",
                    "level": "1+ год",
                    "category": "Опыт работы",
                    "importance": "высокая"
                })
            elif "2" in vacancy_text or "3" in vacancy_text:
                requirements.append({
                    "skill": "Опыт разработки",
                    "level": "2-3 года",
                    "category": "Опыт работы",
                    "importance": "высокая"
                })
            elif "5" in vacancy_text or "старший" in text_lower:
                requirements.append({
                    "skill": "Опыт разработки",
                    "level": "5+ лет",
                    "category": "Опыт работы",
                    "importance": "высокая"
                })
        
        # Анализируем soft skills
        soft_skills = {
            "команд": {"skill": "Командная работа", "level": "Обязательно", "category": "Soft skills"},
            "лидер": {"skill": "Лидерские качества", "level": "Желательно", "category": "Soft skills"},
            "коммуника": {"skill": "Коммуникативные навыки", "level": "Обязательно", "category": "Soft skills"},
            "английск": {"skill": "Английский язык", "level": "Средний", "category": "Языки"}
        }
        
        for keyword, req_data in soft_skills.items():
            if keyword in text_lower:
                requirements.append({
                    "skill": req_data["skill"],
                    "level": req_data["level"],
                    "category": req_data["category"],
                    "importance": "средняя"
                })
        
        # Если ничего не найдено, добавляем базовые требования
        if not requirements:
            requirements = [
                {"skill": "Опыт разработки", "level": "2+ года", "category": "Опыт работы", "importance": "высокая"},
                {"skill": "Командная работа", "level": "Обязательно", "category": "Soft skills", "importance": "высокая"}
            ]
        
        return requirements[:10]  # Ограничиваем до 10 требований
    
    def generate_technical_questions_from_analysis(self, requirements: List[Dict[str, Any]], position: str, general_answers: List[Dict[str, str]]) -> List[str]:
        """Генерировать технические вопросы на основе анализа требований"""
        
        if not requirements:
            return self._get_default_technical_questions([], position)
        
        # Формируем описание требований
        requirements_text = []
        for req in requirements[:8]:  # Берем первые 8 требований
            skill = req.get('skill', '')
            level = req.get('level', '')
            category = req.get('category', '')
            requirements_text.append(f"{skill} ({level}) - {category}")
        
        requirements_desc = "; ".join(requirements_text)
        general_context = ""
        if general_answers:
            general_context = f"Контекст из общих ответов: {general_answers[0].get('answer', '')[:100]}..."
        
        system_prompt = f"""Ты - технический интервьюер для позиции {position}.
Создай 6-8 технических вопросов на основе проанализированных требований: {requirements_desc}.
{general_context}

Вопросы должны быть:
1. Релевантными к конкретным требованиям и их уровню
2. Практическими и конкретными
3. Разного уровня сложности (соответствующего требованиям)
4. На русском языке
5. Учитывать уровень требований (начинающий/средний/продвинутый)

Верни только список вопросов, каждый с новой строки, без нумерации."""
        
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Создай технические вопросы для {position} с требованиями: {requirements_desc}"}
        ]
        
        response = self.generate_response(messages, temperature=0.7)
        
        if response:
            questions = [q.strip() for q in response.split('\n') if q.strip()]
            return questions[:8]  # Ограничиваем до 8 вопросов
        else:
            return self._get_default_technical_questions_from_analysis(requirements, position)
    
    def _get_default_technical_questions_from_analysis(self, requirements: List[Dict[str, Any]], position: str) -> List[str]:
        """Запасные технические вопросы на основе анализа требований"""
        questions = []
        
        # Группируем требования по категориям
        categories = {}
        for req in requirements:
            category = req.get('category', 'Другое')
            if category not in categories:
                categories[category] = []
            categories[category].append(req)
        
        # Генерируем вопросы по категориям
        for category, reqs in categories.items():
            if category == "Языки программирования":
                for req in reqs[:2]:
                    skill = req.get('skill', '')
                    level = req.get('level', '')
                    if "python" in skill.lower():
                        questions.append(f"Расскажите о вашем опыте работы с Python. Какие версии используете?")
                        questions.append(f"Опишите различия между Python 2 и Python 3")
                    elif "java" in skill.lower():
                        questions.append(f"Расскажите о принципах ООП в Java")
                        questions.append(f"Объясните концепцию garbage collection в Java")
            
            elif category == "Фреймворки":
                for req in reqs[:2]:
                    skill = req.get('skill', '')
                    if "django" in skill.lower():
                        questions.append(f"Объясните архитектуру Django и его основные компоненты")
                        questions.append(f"Как работает Django ORM? Приведите примеры")
                    elif "react" in skill.lower():
                        questions.append(f"Объясните концепцию Virtual DOM в React")
                        questions.append(f"В чем разница между функциональными и классовыми компонентами?")
            
            elif category == "Базы данных":
                for req in reqs[:2]:
                    skill = req.get('skill', '')
                    if "postgresql" in skill.lower():
                        questions.append(f"Как вы оптимизируете запросы к PostgreSQL?")
                        questions.append(f"Объясните концепцию индексов в PostgreSQL")
                    elif "mysql" in skill.lower():
                        questions.append(f"В чем разница между MyISAM и InnoDB?")
                        questions.append(f"Как вы решаете проблемы с производительностью MySQL?")
            
            elif category == "Опыт работы":
                for req in reqs[:1]:
                    level = req.get('level', '')
                    questions.append(f"Опишите архитектуру последнего проекта, над которым вы работали")
                    questions.append(f"Как вы решаете проблемы производительности в приложениях?")
        
        # Добавляем общие технические вопросы
        questions.extend([
            "Как вы тестируете свой код? Какие инструменты используете?",
            "Опишите процесс деплоя приложений",
            "Как вы работаете с версионированием кода?"
        ])
        
        return questions[:8]  # Ограничиваем до 8 вопросов
    
    def generate_technical_questions(self, requirements: List[str], position: str, general_answers: List[Dict[str, str]]) -> List[str]:
        """Генерировать технические вопросы на основе требований вакансии"""
        
        requirements_text = ", ".join(requirements)
        general_context = ""
        if general_answers:
            general_context = f"Контекст из общих ответов: {general_answers[0].get('answer', '')[:100]}..."
        
        system_prompt = f"""Ты - технический интервьюер для позиции {position}.
Создай 5-7 технических вопросов на основе требований: {requirements_text}.
{general_context}

Вопросы должны быть:
1. Релевантными к требованиям
2. Практическими и конкретными
3. Разного уровня сложности
4. На русском языке

Верни только список вопросов, каждый с новой строки, без нумерации."""
        
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Создай технические вопросы для {position} с требованиями: {requirements_text}"}
        ]
        
        response = self.generate_response(messages, temperature=0.7)
        
        if response:
            questions = [q.strip() for q in response.split('\n') if q.strip()]
            return questions[:7]  # Ограничиваем до 7 вопросов
        else:
            return self._get_default_technical_questions(requirements, position)
    
    def _get_default_technical_questions(self, requirements: List[str], position: str) -> List[str]:
        """Запасные технические вопросы"""
        base_questions = [
            f"Расскажите о вашем опыте работы с {requirements[0] if requirements else 'основными технологиями'}",
            "Опишите архитектуру последнего проекта, над которым вы работали",
            "Как вы решаете проблемы производительности в приложениях?",
            "Расскажите о вашем опыте работы с базами данных",
            "Как вы тестируете свой код?",
            "Опишите процесс деплоя приложений"
        ]
        
        # Персонализируем на основе требований
        if "Python" in str(requirements):
            base_questions.append("Расскажите о различиях между Python 2 и Python 3")
        if "Django" in str(requirements):
            base_questions.append("Объясните архитектуру Django и его основные компоненты")
        if "PostgreSQL" in str(requirements):
            base_questions.append("Как вы оптимизируете запросы к PostgreSQL?")
        
        return base_questions[:7]
    
    def generate_general_questions(self, name: str, age: int, position: str) -> List[str]:
        """Генерировать общие вопросы для интервью"""
        
        system_prompt = f"""Ты - HR-специалист, проводящий интервью с кандидатом {name}, {age} лет, на позицию {position}.
Создай 4-5 общих вопросов о:
1. Мотивации кандидата
2. Опыте работы
3. Карьерных целях
4. Soft skills

Вопросы должны быть:
1. Персонализированными под возраст и позицию
2. Профессиональными
3. На русском языке
4. Открытыми (требующими развернутого ответа)

Верни только список вопросов, каждый с новой строки, без нумерации."""
        
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Создай общие вопросы для {name}, {age} лет, позиция {position}"}
        ]
        
        response = self.generate_response(messages, temperature=0.8)
        
        if response:
            questions = [q.strip() for q in response.split('\n') if q.strip()]
            return questions[:5]
        else:
            return self._get_default_general_questions(name, age, position)
    
    def _get_default_general_questions(self, name: str, age: int, position: str) -> List[str]:
        """Запасные общие вопросы"""
        if age < 25:
            return [
                f"Привет, {name}! Расскажите о ваших образовательных достижениях и проектах",
                "Почему вы выбрали именно эту сферу для развития карьеры?",
                "Какие у вас планы по профессиональному развитию?",
                "Опишите ситуацию, когда вам пришлось работать в команде"
            ]
        elif age < 35:
            return [
                f"Здравствуйте, {name}! Расскажите о вашем карьерном пути",
                "Что мотивирует вас в работе?",
                "Какие проекты вы считаете наиболее значимыми?",
                "Как вы видите свое развитие в нашей компании?"
            ]
        else:
            return [
                f"Добро пожаловать, {name}! Поделитесь своим профессиональным опытом",
                "Какие лидерские качества вы развили за годы работы?",
                "Как вы видите свою роль в развитии команды?",
                "Что для вас важно в работе?"
            ]
    
    def analyze_candidate_response(self, question: str, answer: str) -> Dict[str, Any]:
        """Анализировать ответ кандидата"""
        
        system_prompt = """Ты - опытный HR-аналитик. Проанализируй ответ кандидата на вопрос интервью.
Оцени по шкале 1-10:
1. Релевантность ответа
2. Структурированность
3. Профессионализм
4. Мотивация

Верни результат в формате JSON:
{
    "relevance": число,
    "structure": число,
    "professionalism": число,
    "motivation": число,
    "summary": "краткое резюме"
}"""
        
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Вопрос: {question}\nОтвет: {answer}\nПроанализируй ответ."}
        ]
        
        response = self.generate_response(messages, temperature=0.3)
        
        try:
            if response:
                return json.loads(response)
        except json.JSONDecodeError:
            pass
        
        # Fallback анализ
        return {
            "relevance": 7,
            "structure": 6,
            "professionalism": 7,
            "motivation": 6,
            "summary": "Ответ требует дополнительного анализа"
        }
