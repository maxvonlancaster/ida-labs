# Георгій Апопій

Лабораторні роботи з аналізу даних.

- [Лаба 1](assignement-1.ipynb): зчитування даних, графіки погоди, пропуски й масштабування.
- [Лаба 2](assignement-2.ipynb): обробка текстів, TF-IDF і Word2Vec.
- [Лаба 3](assignement-3.ipynb): регресія, класифікація та оцінки відгуків.

Код, результати та пояснення є в ноутбуках. Графіки зберіг у `images`,
таблиці й інші результати в `results`. Дані викладача лежать у `resources`.

Четверту лабу поки не робив: у файлі є тільки заголовок, без завдання.

## Запуск

Потрібен Python 3.12. Після створення та активації віртуального середовища:

```bash
python -m pip install -r requirements.txt
python run_labs.py
```

Щоб запустити одну лабу: `python run_labs.py 1`.
Можна також відкрити ноутбуки в Jupyter або VS Code й виконати клітинки по черзі.
Для першого запуску потрібен інтернет, щоб завантажити дані Kaggle та NLTK.

## Дані

- [Завдання викладача](https://github.com/maxvonlancaster/ida-labs).
- [Оцінки студентів](https://www.kaggle.com/datasets/ilayaraja07/data-cleaning-feature-imputation).
- [Товари з пропусками](https://www.kaggle.com/datasets/himelsarder/retail-product-dataset-with-missing-values).
- [Відгуки Coursera](https://www.kaggle.com/datasets/septa97/100k-courseras-course-reviews-dataset).
- [Brown з NLTK](https://www.nltk.org/nltk_data/).
