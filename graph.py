import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator
import math

# Загрузка настроек
with open("settings.txt", "r") as config_file:
    time_step_ms, voltage_step = map(float, config_file.read().split())

# Загрузка данных
adc_values = np.loadtxt("data.txt", dtype=int)

# Перевод в физические значения
time_step_s = time_step_ms / 1000
times = np.arange(len(adc_values)) * time_step_s
voltages = adc_values * voltage_step

# Нахождение индекса максимального напряжения
v_max_index = np.argmax(voltages)
v_max = voltages[v_max_index]

# Разделение фаз заряда и разряда
t_charge = times[:v_max_index + 1]
v_charge = voltages[:v_max_index + 1]
t_discharge = times[v_max_index:]
v_discharge = voltages[v_max_index:]

# Построение графика
fig, ax = plt.subplots(figsize=(14, 9), dpi=300)

# Линии графика
ax.plot(t_charge, v_charge, label="Charging", color="royalblue")
ax.plot(t_discharge, v_discharge, label="Discharging", color="orangered")

# Подписи осей и заголовок
ax.set_xlabel("Time (s)", fontsize=14)
ax.set_ylabel("Voltage (V)", fontsize=14)
ax.set_title("V(t) — Charging and Discharging of Capacitor", fontsize=18, wrap=True)

# Легенда
ax.legend(fontsize=12)

# Ограничения осей
ax.set_xlim(0, math.ceil(times[-1]))
ax.set_ylim(0, 3.5)

# Сетка
ax.grid(which="major", color="gray", linestyle="--", linewidth=0.7)
ax.grid(which="minor", color="lightgray", linestyle=":", linewidth=0.5)

# Деления на осях
ax.xaxis.set_major_locator(MultipleLocator(5))
ax.xaxis.set_minor_locator(MultipleLocator(0.5))
ax.yaxis.set_major_locator(MultipleLocator(0.5))
ax.yaxis.set_minor_locator(MultipleLocator(0.25))

# Время зарядки и разрядки
t_charge_duration = t_charge[-1] - t_charge[0]
t_discharge_duration = t_discharge[-1] - t_discharge[0]

# Добавление поясняющих надписей
ax.text(t_charge_duration / 2 - 0.4, v_max / 2, f"Charge: {t_charge_duration:.2f} s", color="blue", fontsize=12)
ax.text(t_charge_duration + t_discharge_duration / 2 - 0.4, v_max / 2, f"Discharge: {t_discharge_duration:.2f} s", color="red", fontsize=12)

# Вспомогательные линии
ax.axvline(x=t_charge_duration, color='green', linestyle='--')
ax.axhline(y=v_max, color='green', linestyle='--')

# Точки и подписи
ax.scatter([t_charge_duration], [0], color='green')
ax.scatter([0], [v_max], color='green')
ax.scatter([times[v_max_index]], [v_max], color='green')

ax.text(t_charge_duration + 0.1, 0.1, f"{t_charge_duration:.2f} s", fontsize=10)
ax.text(0.1, v_max + 0.1, f"{v_max:.2f} V", fontsize=10)

# Сохранение графика
fig.savefig("graph.svg")
