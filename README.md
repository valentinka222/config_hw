# Конфигурационный язык: трансляция в XML (вариант 23)

## 1. Общее описание

Инструмент командной строки преобразует текст на учебном конфигурационном языке в XML.
Текст читается из стандартного ввода, результат записывается в файл, путь к которому задан ключом `-o`.
Синтаксические ошибки выявляются с указанием строки и столбца.
Разбор выполняется с помощью библиотеки Lark (генератор парсеров).

Состояние проекта: реализованы все 5 этапов (грамматика, XML, константы, проверка ошибок, примеры).

## 2. Описание функций и настроек

### Синтаксис языка

- Число: `[+-]?([1-9][0-9]*|0)`, например `0`, `42`, `-7`, `+15`.
- Имя: `[a-z]+`.
- Словарь: `@{ имя = значение; имя = значение; }`. Значением может быть число или словарь,
  поэтому словари можно вкладывать друг в друга.
- Многострочный комментарий: `{- текст комментария -}`. Допустим между любыми элементами.
- Объявление константы: `(def имя значение)`. Объявления пишутся в начале текста, до основного значения.
- Вычисление константы: `$[имя]`. Заменяется значением константы на этапе трансляции;
  использовать можно только после объявления.

Пример:

```
{- настройки сервера -}
(def port 8080)
@{
  port = $[port];
  limits = @{ min = 1; max = -1; };
}
```

### Файлы проекта

- `src/grammar.py` - грамматика языка для Lark;
- `src/config_parser.py` - разбор текста, ошибка `ConfigSyntaxError` с позицией;
- `src/config_transformer.py` - превращает дерево разбора в числа и словари Python и вычисляет константы;
- `src/xml_writer.py` - строит XML и записывает его в файл;
- `src/errors.py` - классы ошибок трансляции;
- `src/translator.py` - разбор текста и вычисление констант;
- `src/main.py` - точка входа: читает stdin, переводит текст в XML, записывает файл по ключу `-o`.

### Параметры командной строки

- `-o`, `--output` - путь к выходному XML-файлу (обязательный). Недостающие папки создаются.
- Текст конфигурации читается из стандартного ввода.

### Формат XML

- корневой элемент `<config>`;
- число: `<number>8080</number>`;
- словарь: `<dict>` с вложенными `<entry name="имя">значение</entry>`.

### Ошибки

Программа завершается с кодом 1 и выводит одно сообщение:
- синтаксическая ошибка - строка, столбец и фрагмент текста;
- `Строка N: константа 'имя' не объявлена`;
- `Строка N: константа 'имя' уже объявлена`;
- `Строка N: ключ 'имя' повторяется в словаре`.

## 3. Команды сборки и запуска тестов

Установка зависимостей:

```
py -m pip install -r requirements.txt
```

Запуск (Windows и Git Bash):

```
run.bat -o out\result.xml < tests\examples\server.conf
bash run.sh -o out/result.xml < tests/examples/server.conf
```

Тесты:

```
py -m unittest discover -s tests -v
```

Скрипты демонстрации:

```
tests\run_examples.bat (или bash tests/run_examples.sh) - три примера конфигураций
tests\run_errors.bat (или bash tests/run_errors.sh) - примеры ошибок
```

## 4. Примеры использования

### Примеры из разных областей

- `tests/examples/server.conf` - настройки веб-сервера;
- `tests/examples/game.conf` - параметры компьютерной игры;
- `tests/examples/home.conf` - умный дом (температура и освещение по комнатам).

Пример `server.conf`:

```
{- Конфигурация веб-сервера -}
(def http 80)
(def timeout 30)
(def retries 3)

@{
  server = @{
    port = $[http];
    workers = 4;
    timeout = $[timeout];
  };
  proxy = @{
    port = 8080;
    timeout = $[timeout];
    retries = $[retries];
  };
  limits = @{
    connections = 1000;
    uploadmb = 25;
  };
}
```

Результат:

```
$ bash run.sh -o out/server.xml < tests/examples/server.conf
Результат записан в out/server.xml
$ cat out/server.xml
<?xml version='1.0' encoding='utf-8'?>
<config>
  <dict>
    <entry name="server">
      <dict>
        <entry name="port">
          <number>80</number>
        </entry>
        <entry name="workers">
          <number>4</number>
        </entry>
        <entry name="timeout">
          <number>30</number>
        </entry>
      </dict>
    </entry>
    <entry name="proxy">
      <dict>
        <entry name="port">
          <number>8080</number>
        </entry>
        <entry name="timeout">
          <number>30</number>
        </entry>
        <entry name="retries">
          <number>3</number>
        </entry>
      </dict>
    </entry>
    <entry name="limits">
      <dict>
        <entry name="connections">
          <number>1000</number>
        </entry>
        <entry name="uploadmb">
          <number>25</number>
        </entry>
      </dict>
    </entry>
  </dict>
</config>
```

### Ошибки

Ошибки имен:

```
$ echo '$[port]' | bash run.sh -o out/e.xml
Строка 1: константа 'port' не объявлена
$ printf '(def a 1)\n(def a 2)\n3' | bash run.sh -o out/e.xml
Строка 2: константа 'a' уже объявлена
$ printf '@{\n  a = 1;\n  a = 2;\n}' | bash run.sh -o out/e.xml
Строка 3: ключ 'a' повторяется в словаре
```

Синтаксическая ошибка (файл `tests/errors/nosemicolon.conf`):

```
$ bash run.sh -o out/e.xml < tests/errors/nosemicolon.conf
Синтаксическая ошибка: строка 1, столбец 10
@{ a = 1 }
         ^
```