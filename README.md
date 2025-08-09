# Mystem Wrapper

## Установка

1. Скачать архив лемматизатора mystem по [ссылке](http://download.cdn.yandex.net/mystem/mystem-3.1-win-64bit.zip). 
Если ссылка не работает, найти mystem версии 3.1 на сайте https://yandex.ru/dev/mystem.
2. Распаковать архив. Исполняемый файл mystem.exe переместить в *C:\Users\CurrentUser\\.local\bin*. 
Т.е. итоговый путь файла будет *C:\Users\CurrentUser\\.local\bin\mystem.exe*. Если директории .local\bin не существует, создать самостоятельно.
3. Переместить исполняемый файл main.exe и папку _internal из dist\main в любое удобное место, например на рабочий стол.

## Использование

Перейти в папку, где находится исполняемый файл main.exe. ПКМ по папке / Открыть в терминале.

Общий случай:
`.\main.exe --texts [PATHS_TO_FILES] [OPTIONS]`

Формируемый отчет *Statistics.xlsx* будет сохранен там, где расположен исполняемый файл main.exe.

Например:
`.\main.exe --texts "C:\Users\User\text1.txt" "C:\Users\User\text2.txt" --exclude-proper-names --sort frequency`

`.\main.exe --texts "C:\User\Miroslav\text1.txt"`

В свойствах файла указано расположение.

### Опции

`-t` `--texts` - Пути к текстовым файлам, обязательный параметр. Файлы в формате txt, в кодировке UTF-8.
Если используется другая кодировка - преобразовать в UTF-8 при помощи Notepad++.

Пример: `.\main.exe --texts "C:\User\Miroslav\text1.txt" "C:\User\Miroslav\text2.txt" `

`-e` ИЛИ `--exclude-proper-names` - Исключить из подсчета имена собственные.

Пример: `.\main.exe --texts "C:\User\Miroslav\text1.txt" --exclude-proper-names`

`-s` ИЛИ `--sort` - Сортировка по алфавиту (`alphabetic`, `alphabetic-reverse`) или частоте (`frequency`, `frequency-reverse`).
По умолчанию применяется сортировка по алфавиту (`--sort alphabetic`).

Пример: `.\main.exe --texts "C:\User\Miroslav\text1.txt" --sort frequency-reverse`

Также есть сортировка по частоте только для первого текста, при которой остальные тексты сортируются по порядку слов из первого текста (`frequency-first`).  

Пример: `.\main.exe --texts "C:\User\Miroslav\text1.txt" "C:\User\Miroslav\text2.txt" --sort frequency-first`

`-ep` ИЛИ `--exclude-pos` - Исключить из подсчета отдельные части речи.  Части речи указываются через пробел. 
Расшифровку частей речи mystem можно посмотреть по [ссылке](https://yandex.ru/dev/mystem/doc/ru/grammemes-values) или в таблице ниже.

Пример: `.\main.exe --texts "C:\User\Miroslav\text1.txt" --exclude-pos PART PR` для исключения частиц и предлогов.

| Ключ   | Часть речи                       |
|--------|----------------------------------|
| A      | прилагательное                   |
| ADV    | наречие                          |
| ADVPRO | местоименное наречие             |
| ANUM   | числительное-прилагательное      |
| APRO   | местоимение-прилагательное       |
| COM    | часть композита - сложного слова |
| CONJ   | союз                             |
| INTJ   | междометие                       |
| NUM    | числительное                     |
| PART   | частица                          |
| PR     | предлог                          |
| S      | существительное                  |
| SPRO   | местоимение-существительное      |
| V      | глагол                           |
