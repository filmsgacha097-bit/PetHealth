Руководство разработчика
========================

Настройка среды разработки
--------------------------

1. Установите **Python 3.9+** с `python.org <https://python.org>`_.
2. Склонируйте репозиторий:

   .. code-block:: bash

      git clone https://github.com/filmsgacha097-bit/PetHealth.git
      cd PetHealth

3. Создайте виртуальное окружение:

   .. code-block:: bash

      python -m venv venv

4. Активируйте его:

   * **Windows:** ``venv\Scripts\activate``
   * **Linux:** ``source venv/bin/activate``

5. Установите зависимости:

   .. code-block:: bash

      pip install -r requirements.txt

Структура проекта
-----------------

.. code-block:: text

   PetHealth/
   ├── main.py                # точка входа
   ├── models.py              # модели данных
   ├── database_manager.py    # работа с БД
   ├── ui/                    # интерфейс (фреймы)
   ├── utils/                 # утилиты (PDF)
   ├── tests/                 # тесты
   ├── docs/                  # документация Sphinx
   └── assets/                # ресурсы (иконки, шрифты)

Запуск тестов
-------------

.. code-block:: bash

   pytest tests/ -v

Измерение покрытия:

.. code-block:: bash

   coverage run -m pytest tests/
   coverage report

Сборка .exe
-----------

.. code-block:: bash

   pyinstaller --onefile --windowed --name PetHealth --add-data "assets;assets" main.py

Сборка документации
-------------------

.. code-block:: bash

   cd docs
   make html

Результат — в ``docs/build/html/index.html``.

Принципы разработки
-------------------

* **Clean Code** — осмысленные имена, маленькие функции, DRY.
* **Docstrings** — для каждого модуля, класса, функции.
* **flake8 + black** — единый стиль кода.
* **Git** — Feature Branch Workflow.
* **pytest** — модульные, интеграционные тесты.

Передача знаний: как присоединиться к проекту
----------------------------------------------

Если вы новый разработчик и хотите присоединиться к проекту,
следуйте этому пошаговому руководству.

Шаг 1. Изучите документацию
^^^^^^^^^^^^^^^^^^^^^^^^^^^

1. **README.md** — краткое описание проекта.
2. **BACKLOG.md** — список идей для развития.
3. **Эта документация** — архитектура, функциональность, API.
4. **CODE_REVIEW.md** — пример code review.

Шаг 2. Настройте окружение
^^^^^^^^^^^^^^^^^^^^^^^^^^

1. Установите Python 3.9+.
2. Склонируйте репозиторий:

   .. code-block:: bash

      git clone https://github.com/filmsgacha097-bit/PetHealth.git
      cd PetHealth

3. Создайте виртуальное окружение:

   .. code-block:: bash

      python -m venv venv

4. Активируйте его:

   * **Windows:** ``venv\Scripts\activate``
   * **Linux:** ``source venv/bin/activate``

5. Установите зависимости:

   .. code-block:: bash

      pip install -r requirements.txt

6. Запустите приложение, чтобы убедиться, что всё работает:

   .. code-block:: bash

      python main.py

Шаг 3. Разберитесь в структуре кода
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Ключевые точки в проекте:

* **``main.py``** — точка входа. Запускает приложение.
* **``ui/app.py``** — главное окно ``PetHealthApp``.
  Управляет переключением экранов.
* **``database_manager.py``** — класс ``DatabaseManager``.
  Вся работа с базой данных.
* **``models.py``** — модели данных (``Pet``, ``Record``, ``Disease``,
  ``PetDisease``).
* **``ui/``** — экраны приложения (фреймы).
* **``utils/print_pet.py``** — формирование PDF.
* **``tests/``** — тесты.

Шаг 4. Запустите тесты
^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

   pytest tests/ -v

Проверьте покрытие:

.. code-block:: bash

   coverage run -m pytest tests/
   coverage report

Шаг 5. Правила разработки
^^^^^^^^^^^^^^^^^^^^^^^^^

1. **Ветвление.** Используйте Feature Branch Workflow:
   ``git checkout -b feature/новая-функция``.
2. **Коммиты.** Атомарные, с осмысленными сообщениями
   (``feat:``, ``fix:``, ``docs:``, ``test:``).
3. **Стиль кода.** Соблюдайте PEP 8. Запускайте
   ``flake8`` и ``black`` перед коммитом.
4. **Docstrings.** Для каждого модуля, класса и функции —
   в стиле Google.
5. **Тесты.** Новая функция — новые тесты.
6. **Pull Request.** После завершения работы — создайте PR,
   проведите Code Review.

Шаг 6. Как решать задачи
^^^^^^^^^^^^^^^^^^^^^^^^^

1. Откройте **Issues** на GitHub.
2. Выберите задачу с метками ``bug`` или ``enhancement``.
3. Создайте ветку под задачу.
4. Реализуйте, протестируйте, закоммитьте.
5. Создайте Pull Request.
6. Дождитесь Code Review.

Шаг 7. Полезные команды
^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

   # Запуск приложения
   python main.py

   # Запуск тестов
   pytest tests/ -v

   # Проверка стиля
   flake8 .

   # Форматирование
   black .

   # Сборка документации
   cd docs && make html

   # Сборка .exe
   pyinstaller --onefile --windowed --name PetHealth --add-data "assets;assets" main.py

Контакт
^^^^^^^

* **Автор проекта:** Макарова Варвара Николаевна
* **Группа:** ИСП34
* **GitHub:** https://github.com/filmsgacha097-bit