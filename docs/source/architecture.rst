Архитектура приложения
======================

Приложение построено по **многослойной архитектуре** с использованием
паттерна **MVC** (Model-View-Controller).

Слои приложения
---------------

**Model (модель)** — работа с данными:

* Класс :class:`database_manager.DatabaseManager` — доступ к базе данных SQLite.
* Классы :class:`models.Pet`, :class:`models.Record`, :class:`models.Disease`,
  :class:`models.PetDisease` — модели данных.

**View (представление)** — пользовательский интерфейс:

* :class:`ui.login_frame.LoginFrame` — экран авторизации.
* :class:`ui.register_frame.RegisterFrame` — экран регистрации.
* :class:`ui.main_frame.MainFrame` — главный экран со списком питомцев.
* :class:`ui.pet_card_frame.PetCardFrame` — карточка питомца.
* :class:`ui.catalog_frame.CatalogFrame` — справочник заболеваний.
* :class:`ui.reminders_frame.RemindersFrame` — окно напоминаний.

**Controller (контроллер)** — управление:

* :class:`ui.app.PetHealthApp` — главное окно приложения,
  переключает экраны.

Схема базы данных
-----------------

База данных состоит из **пяти таблиц**:

* ``pets`` — питомцы.
* ``records`` — записи о здоровье.
* ``diseases`` — справочник заболеваний.
* ``symptoms`` — справочник симптомов.
* ``pet_diseases`` — история болезней питомцев.

Связи между таблицами реализованы через внешние ключи
с каскадным удалением (``ON DELETE CASCADE``).

Используемые паттерны
---------------------

* **MVC** — разделение логики, интерфейса и данных.
* **Repository** — доступ к данным через :class:`~database_manager.DatabaseManager`.
* **Singleton** — единое подключение к базе данных.

Технологии
----------

* **Python 3.9+** — язык разработки.
* **SQLite** — встроенная база данных.
* **CustomTkinter** — графический интерфейс.
* **Pillow** — работа с изображениями.
* **fpdf2** — создание PDF.
* **rlottie-python** — воспроизведение Lottie-анимаций.
* **pytest** — тестирование.
* **Sphinx** — документация.