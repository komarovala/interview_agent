# 🎯 Агент Генерации Сценария Интервью

Интеллектуальный агент для создания персональных сценариев интервью с использованием LangGraph и OpenRouter.ai.

## 🚀 Возможности

- **Расширенный workflow**: 8 нод для полного цикла интервью
- **Анализ текста вакансии**: автоматическое извлечение требований и их уровня
- **Общие вопросы**: мотивация, опыт, карьерные цели
- **Технические вопросы**: на основе требований вакансии
- **Уточняющие вопросы**: на основе предыдущих ответов
- **Интеграция с OpenRouter.ai**: использование современных языковых моделей
- **Анализ ответов**: оценка релевантности и качества
- **Итоговый отчет**: полная статистика интервью
- **Fallback режим**: работа без API ключа

## 📋 Структура проекта

```
src/
├── interview_agent.py    # Основной агент с LangGraph workflow
├── openrouter_client.py  # Клиент для работы с OpenRouter.ai
├── example_usage.py      # Примеры использования
└── main.py              # Точка входа в приложение
config.py                 # Конфигурация OpenRouter
env_example.txt          # Пример файла .env
```

## 🛠 Установка и запуск

### 1. Установка зависимостей

```bash
# Активируйте виртуальное окружение
.\venv\Scripts\Activate.ps1

# Установите зависимости
pip install -r requirements.txt
```

### 2. Настройка OpenRouter.ai (опционально)

```bash
# Скопируйте пример конфигурации
copy env_example.txt .env

# Отредактируйте .env файл и добавьте ваш API ключ
# Получить ключ можно на https://openrouter.ai/
```

**Без API ключа агент будет работать в fallback режиме с базовыми вопросами.**

### 3. Запуск агента

```bash
python src/main.py
```

## 🎮 Режимы работы

### 1. Интерактивная демонстрация
Полный процесс интервью с живым общением:
- Агент спрашивает имя
- Агент спрашивает возраст
- Генерирует персональные вопросы
- Сохраняет результат в JSON

### 2. Тестирование workflow
Проверка работы без интерактивного ввода:
- Симуляция ввода данных
- Тестирование всех нод
- Проверка генерации вопросов

### 3. Прямой запуск агента
Минималистичный запуск с базовым функционалом.

## 🔧 Архитектура

### Workflow LangGraph

```
start → get_name → get_age → get_vacancy_requirements → ask_general_questions → 
generate_technical_questions → ask_technical_questions → generate_followup_questions → 
finalize_interview → end
```

### Ноды агента

1. **get_name_node**: Получение имени кандидата
2. **get_age_node**: Получение возраста кандидата
3. **get_vacancy_requirements_node**: Анализ текста вакансии и извлечение требований
4. **ask_general_questions_node**: Общие вопросы о мотивации и опыте
5. **generate_technical_questions_node**: Генерация технических вопросов
6. **ask_technical_questions_node**: Технические вопросы
7. **generate_followup_questions_node**: Уточняющие вопросы
8. **finalize_interview_node**: Создание итогового отчета

### Состояние агента

```python
class InterviewState:
    messages: List[Dict[str, str]]           # История сообщений
    candidate_name: str                     # Имя кандидата
    candidate_age: int                      # Возраст кандидата
    candidate_position: str                 # Позиция кандидата
    vacancy_text: str                       # Полный текст вакансии
    vacancy_requirements: List[Dict[str, Any]] # Структурированные требования
    general_questions: List[str]            # Общие вопросы
    general_answers: List[Dict[str, str]]   # Ответы на общие вопросы
    technical_questions: List[str]          # Технические вопросы
    technical_answers: List[Dict[str, str]] # Ответы на технические вопросы
    followup_questions: List[str]           # Уточняющие вопросы
    interview_questions: List[str]          # Все вопросы интервью
    current_step: str                       # Текущий шаг процесса
```

## 📊 Персонализация вопросов

Агент адаптирует вопросы в зависимости от:

### Возраста кандидата:
- **< 25 лет**: Фокус на образовании и стажировках
- **25-35 лет**: Карьерный путь и профессиональный опыт
- **> 35 лет**: Лидерские качества и менторство

### Требований вакансии:
- **Автоматический анализ**: извлечение навыков, уровня и категории
- **Структурированные данные**: skill, level, category, importance
- **Технические навыки**: Python, Django, PostgreSQL и др.
- **Опыт работы**: количество лет, уровень позиции
- **Soft skills**: командная работа, лидерство, коммуникация

### Предыдущих ответов:
- **Уточняющие вопросы**: на основе общих ответов
- **Технические детали**: углубление в технические темы
- **Контекстные вопросы**: связь с опытом кандидата

## 📁 Выходные данные

Результат сохраняется в `interview_result.json`:

```json
{
  "candidate_name": "Анна Петрова",
  "candidate_age": 28,
  "candidate_position": "Python разработчик",
  "vacancy_text": "Python Developer...",
  "vacancy_requirements": [
    {"skill": "Python", "level": "Продвинутый", "category": "Языки программирования", "importance": "высокая"},
    {"skill": "Django", "level": "Средний", "category": "Фреймворки", "importance": "высокая"}
  ],
  "general_questions": ["...", "..."],
  "general_answers": [{"question": "...", "answer": "..."}],
  "technical_questions": ["...", "..."],
  "technical_answers": [{"question": "...", "answer": "..."}],
  "followup_questions": ["...", "..."],
  "total_questions": 15,
  "questions": ["...", "..."],
  "conversation_history": [...]
}
```

## 🧪 Тестирование

```bash
# Запуск тестового режима
python src/example_usage.py
# Выберите опцию 2 для тестирования

# Запуск тестирования расширенного агента
python src/test_extended_agent.py

# Запуск тестирования анализа вакансий
python src/test_vacancy_analysis.py
```

## 🔮 Расширение функционала

Для добавления новых нод:

1. Создайте новую функцию-ноду
2. Добавьте её в граф: `workflow.add_node("node_name", function)`
3. Определите связи: `workflow.add_edge("from", "to")`

Пример:
```python
def _get_experience_node(self, state: InterviewState) -> InterviewState:
    # Ваша логика
    return state

# Добавление в граф
workflow.add_node("get_experience", self._get_experience_node)
workflow.add_edge("get_age", "get_experience")
```

## 🐛 Устранение неполадок

### Проблема: Ошибка импорта LangGraph
```bash
pip install --upgrade langgraph langchain
```

### Проблема: Ошибка активации виртуального окружения
```bash
# В PowerShell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
.\venv\Scripts\Activate.ps1
```

## 📝 Лицензия

MIT License - используйте свободно для своих проектов!

---

**Создано с ❤️ используя LangGraph**
