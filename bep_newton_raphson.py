# ============================================================
#  METODE NUMERIK – Newton-Raphson
#  Kasus: Mencari Titik Impas (Break-Even Point) Usaha
#         UMKM Keripik Singkong
# ============================================================
#  Parameter Usaha:
#    Harga jual      (p)  = Rp 15.000 / unit
#    Biaya tetap     (FC) = Rp 2.000.000
#    Biaya variabel  (vc) = Rp 8.000 / unit
#    Koefisien kuadrat(a) = 0.0005  (komponen non-linier)
#
#  Model Matematika:
#    R(x)  = 15000 * x
#    TC(x) = 2000000 + 8000*x + 0.0005*x^2
#    f(x)  = R(x) - TC(x) = -0.0005x^2 + 7000x - 2000000
#    f'(x) = -0.001x + 7000
#
#  Metode  : Newton-Raphson  →  x_(n+1) = x_n - f(x_n)/f'(x_n)
#  Kriteria: |x_(n+1) - x_n| < epsilon
# ============================================================

# ── Parameter usaha ──────────────────────────────────────────
p   = 15_000       # harga jual per unit (Rp)
FC  = 2_000_000    # biaya tetap (Rp)
vc  = 8_000        # biaya variabel per unit (Rp)
a   = 0.0005       # koefisien non-linier

# ── Fungsi f(x) dan turunannya f'(x) ────────────────────────
def f(x):
    """Persamaan BEP: R(x) - TC(x)"""
    return -a * x**2 + (p - vc) * x - FC

def f_prime(x):
    """Turunan pertama f(x)"""
    return -2 * a * x + (p - vc)

# ── Newton-Raphson ───────────────────────────────────────────
def newton_raphson(x0, epsilon=1e-4, max_iter=100):
    """
    Mencari akar f(x) = 0 menggunakan metode Newton-Raphson.

    Parameter:
        x0       : tebakan awal
        epsilon  : toleransi galat
        max_iter : batas maksimum iterasi

    Return:
        akar (float), jumlah iterasi (int)
    """
    print("=" * 65)
    print("  ITERASI NEWTON-RAPHSON – Break-Even Point (BEP)")
    print("=" * 65)
    print(f"  Tebakan awal  : x0 = {x0}")
    print(f"  Toleransi     : ε  = {epsilon}")
    print("-" * 65)
    print(f"{'Iter':>4} {'x_n':>12} {'f(x_n)':>14} {'f\'(x_n)':>12} "
          f"{'x_(n+1)':>12} {'|Galat|':>10}")
    print("-" * 65)

    x = x0
    for i in range(1, max_iter + 1):
        fx  = f(x)
        fpx = f_prime(x)

        if fpx == 0:
            print("  ⚠  f'(x) = 0 — metode gagal, coba nilai awal lain.")
            return None, i

        x1   = x - fx / fpx
        galat = abs(x1 - x)

        print(f"{i:>4} {x:>12.4f} {fx:>14.4f} {fpx:>12.4f} "
              f"{x1:>12.4f} {galat:>10.6f}")

        if galat < epsilon:
            print("-" * 65)
            print(f"  ✔  Konvergen pada iterasi ke-{i}  (galat = {galat:.8f})")
            return x1, i

        x = x1

    print("  ⚠  Belum konvergen setelah", max_iter, "iterasi.")
    return x, max_iter

# ── Jalankan program ─────────────────────────────────────────
if __name__ == "__main__":
    x0      = 400          # tebakan awal (unit)
    epsilon = 1e-4         # toleransi

    bep, n_iter = newton_raphson(x0, epsilon)

    if bep is not None:
        print()
        print("=" * 65)
        print("  HASIL AKHIR")
        print("=" * 65)
        print(f"  BEP ≈ {bep:.4f} unit  →  dibulatkan  {round(bep)} unit")
        print()
        print(f"  Validasi  →  f({bep:.4f}) = {f(bep):.6f}  ≈ 0  ✓")
        print()
        print("  Interpretasi:")
        print(f"  UMKM harus memproduksi minimal {round(bep)} unit keripik")
        print("  singkong agar mencapai titik impas (tidak untung / rugi).")
        print("=" * 65)

        # ── Grafik (opsional, butuh matplotlib) ──────────────
        try:
            import matplotlib.pyplot as plt
            import numpy as np

            xs = np.linspace(50, 600, 500)
            ys = [f(x) / 1_000 for x in xs]     # satuan ribu Rp

            plt.figure(figsize=(8, 5))
            plt.plot(xs, ys, color="#1A237E", linewidth=2, label="f(x) = R(x) − TC(x)")
            plt.axhline(0, color="#B0BEC5", linewidth=1, linestyle="--")
            plt.axvline(bep, color="#C62828", linewidth=1.2,
                        linestyle=":", label=f"BEP ≈ {bep:.2f} unit")
            plt.scatter([bep], [0], color="#C62828", s=60, zorder=5)
            plt.annotate(f"BEP ≈ {bep:.2f}",
                         xy=(bep, 0),
                         xytext=(bep + 20, 150),
                         fontsize=10, color="#C62828",
                         arrowprops=dict(arrowstyle="->", color="#C62828"))
            plt.xlabel("Jumlah Unit Produksi (x)", fontsize=11)
            plt.ylabel("f(x)  [ribu Rp]", fontsize=11)
            plt.title("Grafik Break-Even Point – Metode Newton-Raphson", fontsize=13)
            plt.legend(fontsize=10)
            plt.grid(True, alpha=0.3)
            plt.tight_layout()
            plt.savefig("grafik_bep.png", dpi=150)
            plt.show()
            print("  Grafik disimpan sebagai  grafik_bep.png")
        except ImportError:
            print("  (Install matplotlib untuk menampilkan grafik)")
