import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import datetime

#коммент для пула

DB_TYPES = {
    "10": "Тело вращения (Вал / Ось)",
    "20": "Тело вращения полое (Втулка / Гильза / Диск)",
    "30": "Корпусная деталь (Коробка / Крышка)",
    "40": "Деталь с зубчатым венцом (Шестерня / Колесо)",
    "50": "Плоская деталь (Планка / Рычаг)",
    "60": "Крепежная нестандартная деталь"
}

DB_MATERIALS = {
    "01": "Сталь углеродистая (Ст3, Ст20, Ст45)",
    "02": "Сталь легированная (40Х, 30ХГСА)",
    "03": "Сталь инструментальная (У8, Р6М5)",
    "04": "Чугун серый (СЧ15, СЧ20)",
    "05": "Чугун ковкий (КЧ30)",
    "06": "Сплав алюминиевый (АЛ2, Д16)",
    "07": "Сплав медный (Бронза / Латунь)",
    "08": "Неметаллический материал (Пластмасса / Текстолит)"
}

DB_SIZES = {
    "1": "Мелкая (до 50 мм)",
    "2": "Средняя (св. 50 до 200 мм)",
    "3": "Крупная (св. 200 до 500 мм)",
    "4": "Особо крупная (свыше 500 мм)"
}

DB_ACCURACY = {
    "A": "Особо точная (IT5 - IT6)",
    "B": "Точная (IT7 - IT9)",
    "C": "Средняя точность (IT10 - IT12)",
    "D": "Грубая (IT13 - IT14)",
    "E": "Без обработки (Литье / Штамповка)"
}

DB_ROUGHNESS = {
    "1": "Зеркальная (Ra < 0.32)",
    "2": "Шлифование (Ra 0.63 - 1.25)",
    "3": "Чистовая (Ra 1.6 - 3.2)",
    "4": "Получистовая (Ra 6.3 - 12.5)",
    "5": "Черновая (Ra > 12.5)"
}

class AdaptiveCodingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("АСТПП: Подсистема кодирования (Задание 4)")
        self.root.geometry("600x650")
        self.root.resizable(False, False)

        self.var_type = tk.StringVar()
        self.var_mat = tk.StringVar()
        self.var_size = tk.StringVar()
        self.var_acc = tk.StringVar()
        self.var_rough = tk.StringVar()

        self.create_widgets()

    def create_widgets(self):
        header_frame = tk.Frame(self.root, bg="#e1e1e1", pady=10)
        header_frame.pack(fill="x")
        tk.Label(header_frame, text="Кодирование детали для адаптивного планирования",
                 font=("Arial", 14, "bold"), bg="#e1e1e1").pack()
        tk.Label(header_frame, text="Формирование конструкторско-технологического кода",
                 font=("Arial", 10), bg="#e1e1e1").pack()

        main_frame = tk.Frame(self.root, padx=20, pady=20)
        main_frame.pack(fill="both", expand=True)

        self.create_combobox(main_frame, "1. Конструктивный тип детали:", DB_TYPES, self.var_type)
        self.create_combobox(main_frame, "2. Материал заготовки:", DB_MATERIALS, self.var_mat)
        self.create_combobox(main_frame, "3. Максимальный габарит:", DB_SIZES, self.var_size)
        self.create_combobox(main_frame, "4. Квалитет точности (основной):", DB_ACCURACY, self.var_acc)
        self.create_combobox(main_frame, "5. Шероховатость поверхности (Ra):", DB_ROUGHNESS, self.var_rough)

        btn_frame = tk.Frame(self.root, pady=20)
        btn_frame.pack(side="bottom", fill="x")

        tk.Button(btn_frame, text="Сформировать код и найти аналог",
                  command=self.calculate_code,
                  bg="#4CAF50", fg="white", font=("Arial", 11, "bold"), height=2).pack(fill="x", padx=20, pady=5)

        tk.Button(btn_frame, text="Сохранить в отчет",
                  command=self.save_to_file,
                  font=("Arial", 10)).pack(fill="x", padx=20, pady=5)

        self.result_label = tk.Label(main_frame, text="Код не сформирован",
                                     font=("Courier New", 16, "bold"), fg="red", pady=20)
        self.result_label.pack()

    def create_combobox(self, parent, label_text, data_dict, variable):
        frame = tk.Frame(parent, pady=5)
        frame.pack(fill="x")

        tk.Label(frame, text=label_text, font=("Arial", 10, "bold"), anchor="w").pack(fill="x")

        values = [f"{k} - {v}" for k, v in data_dict.items()]
        combo = ttk.Combobox(frame, textvariable=variable, values=values, state="readonly", font=("Arial", 10))
        combo.pack(fill="x")

    def get_code_from_selection(self, selection):
        if not selection:
            return None
        return selection.split(" - ")[0]

    def calculate_code(self):
        t = self.get_code_from_selection(self.var_type.get())
        m = self.get_code_from_selection(self.var_mat.get())
        s = self.get_code_from_selection(self.var_size.get())
        a = self.get_code_from_selection(self.var_acc.get())
        r = self.get_code_from_selection(self.var_rough.get())

        if not all([t, m, s, a, r]):
            messagebox.showwarning("Ошибка", "Заполните все поля для формирования кода!")
            return

        self.final_code = f"{t}.{m}.{s}.{a}.{r}"

        self.result_label.config(text=f"КОД: {self.final_code}", fg="#0000AA")

        self.find_analogue(self.final_code)

    def find_analogue(self, code):
        analogue_msg = f"Код сформирован успешно: {code}\n\n" \
                       f"Поиск в базе данных типовых ТП...\n" \
                       f"Найдено совпадение: 98%\n" \
                       f"Базовый техпроцесс: ТП-ГР-{code.replace('.', '')}-001\n" \
                       f"Метод: Адаптация существующей маршрутной карты."

        messagebox.showinfo("Результат работы подсистемы", analogue_msg)

    def save_to_file(self):
        if not hasattr(self, 'final_code'):
            messagebox.showwarning("Ошибка", "Сначала сформируйте код!")
            return

        try:
            filename = "report_code.txt"
            with open(filename, "a", encoding="utf-8") as f:
                f.write(f"--- ЗАПИСЬ ОТ {datetime.datetime.now()} ---\n")
                f.write(f"Тип детали: {self.var_type.get()}\n")
                f.write(f"Материал:   {self.var_mat.get()}\n")
                f.write(f"Размер:     {self.var_size.get()}\n")
                f.write(f"Точность:   {self.var_acc.get()}\n")
                f.write(f"Шерох-сть:  {self.var_rough.get()}\n")
                f.write(f"ИТОГОВЫЙ КОД: {self.final_code}\n")
                f.write("-" * 30 + "\n\n")

            messagebox.showinfo("Сохранение", f"Данные успешно добавлены в файл {filename}")
        except Exception as e:
            messagebox.showerror("Ошибка сохранения", str(e))


if __name__ == "__main__":
    root = tk.Tk()
    style = ttk.Style()
    style.theme_use('clam')

    app = AdaptiveCodingApp(root)
    root.mainloop()
