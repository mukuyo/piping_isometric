import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

# 実際の距離データ (x)
x = np.array([0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5, 5.5, 6])

# 新しい実際のデータ (y_actual)
y_actual = np.array([0.0005804, 0.000422344, 0.000460954, 0.000716329, 0.001140156, 0.001804504, 0.002712209, 0.003707376, 0.004907379, 0.006388684, 0.008037361, 0.009789262])

# 指数関数モデルの定義
def exp_model(x, a, b):
    return a * np.exp(b * x)

# フィッティング
popt_new, pcov_new = curve_fit(exp_model, x, y_actual)

# フィッティング結果のパラメータ
a_new, b_new = popt_new

# フィッティングによる近似値
y_fit_new = exp_model(x, a_new, b_new)

# プロット
plt.figure(figsize=(10, 6))
plt.plot(x, y_actual, 'bo', label='実際のデータ')
plt.plot(x, y_fit_new, 'r-', label=f'指数関数近似: y = {a_new:.6f} * exp({b_new:.6f} * x)')
plt.xlabel('実際の距離')
plt.ylabel('データ値')
plt.legend()
plt.title('実際のデータの指数関数近似')
plt.grid(True)
plt.show()

print(a_new, b_new)