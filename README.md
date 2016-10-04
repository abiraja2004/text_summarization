По ссылке доступны предобработанные данные:
https://drive.google.com/drive/folders/0B5Sz52EAqYyTOG5zVkhxOVdCc2s?usp=sharing

В preprocessed-files.tar.gz лежат txt, pickle2 и pickle3 файлы с авторами, названиями, абстрактами, и текстами статей.
В txt n-ой строке в каждом файле соответсвует одна и та же статья. Авторы разделены ";"
В pickle лежат массивы. n-ый элемент массивов соответсвует одной и той же статье. Авторы представлены в виде массива

pickle2 - python2 pickle format
pickle3 - python3 pickle format

В no_spec_topic_articles.csv.tar.gz часть колонок из no_spec_topic_articles, но в формате который можно прочитать не только из R. Например он хорошо считывается pandas (см preprocess.ipynb).

