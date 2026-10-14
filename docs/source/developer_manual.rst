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