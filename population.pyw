import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import matplotlib.ticker as mticker
import numpy as np

# ---------- DATA ----------
data = [
    (2026, 8.300678395), (2027, 8.369094344), (2028, 8.436618886), (2029, 8.503285323),
    (2030, 8.569124911), (2031, 8.634119333), (2032, 8.698229812), (2033, 8.761449081),
    (2034, 8.823784909), (2035, 8.885210181), (2036, 8.945686614), (2037, 9.005152624),
    (2038, 9.063572926), (2039, 9.120928380), (2040, 9.177190203), (2041, 9.232281575),
    (2042, 9.286110371), (2043, 9.338661314), (2044, 9.389873693), (2045, 9.439639668),
    (2046, 9.487889604), (2047, 9.534545977), (2048, 9.579536043), (2049, 9.622824029),
    (2050, 9.664378587), (2051, 9.704192304), (2052, 9.742264515), (2053, 9.778614614),
    (2054, 9.813251659), (2055, 9.846237570), (2056, 9.877680392), (2057, 9.907637193),
    (2058, 9.936164379), (2059, 9.963337082), (2060, 9.989232292), (2061, 10.013916213),
    (2062, 10.037466600), (2063, 10.059950035), (2064, 10.081402737), (2065, 10.101849561),
    (2066, 10.121317107), (2067, 10.139808361), (2068, 10.157301941), (2069, 10.173782135),
    (2070, 10.189241959), (2071, 10.203681568), (2072, 10.217055169), (2073, 10.229327824),
    (2074, 10.240485056), (2075, 10.250496432), (2076, 10.259351432), (2077, 10.267045023),
    (2078, 10.273556322), (2079, 10.278887473), (2080, 10.283078029), (2081, 10.286161735),
    (2082, 10.288205050), (2083, 10.289247323), (2084, 10.289315244), (2085, 10.288456599),
    (2086, 10.286708360), (2087, 10.284111374), (2088, 10.280704572), (2089, 10.276518280),
    (2090, 10.271565070), (2091, 10.265861714), (2092, 10.259408375), (2093, 10.252184759),
    (2094, 10.244185837), (2095, 10.235403601), (2096, 10.225850874), (2097, 10.215549310),
    (2098, 10.204489862), (2099, 10.192689066), (2100, 10.180160751),
    (2101, 10.1674), (2102, 10.1545), (2103, 10.1414), (2104, 10.1281),
    (2105, 10.1146), (2106, 10.1009), (2107, 10.0870), (2108, 10.0729),
    (2109, 10.0586), (2110, 10.0441), (2111, 10.0294), (2112, 10.0145),
    (2113, 9.9994), (2114, 9.9841), (2115, 9.9686), (2116, 9.9529),
    (2117, 9.9370), (2118, 9.9209), (2119, 9.9046), (2120, 9.8881),
    (2121, 9.8714), (2122, 9.8545), (2123, 9.8374), (2124, 9.8201),
    (2125, 9.8026), (2126, 9.7849), (2127, 9.7670), (2128, 9.7489),
    (2129, 9.7306), (2130, 9.7121), (2131, 9.6934), (2132, 9.6745),
    (2133, 9.6554), (2134, 9.6361), (2135, 9.6166), (2136, 9.5969),
    (2137, 9.5770), (2138, 9.5569), (2139, 9.5366), (2140, 9.5161),
    (2141, 9.4954), (2142, 9.4745), (2143, 9.4534), (2144, 9.4321),
    (2145, 9.4106), (2146, 9.3889), (2147, 9.3670), (2148, 9.3449),
    (2149, 9.3226), (2150, 9.3001),
]

years_all = np.array([d[0] for d in data])
pop_all   = np.array([d[1] for d in data])          # in billions
MIN_YEAR, MAX_YEAR = 2026, 2150
PEAK_YEAR, PEAK_POP = 2084, 10.289315244

# Colors
BLUE_EXACT = "#1f6feb"     # 2026–2100
BLUE_LINEAR = "#1f6feb"    # 2101–2150 (now also blue)

def pop_at(year: int) -> float:
    idx = year - MIN_YEAR
    if 0 <= idx < len(pop_all):
        return float(pop_all[idx])
    return float("nan")

def fmt_people(billions: float) -> str:
    if np.isnan(billions):
        return "—"
    return f"{int(round(billions * 1_000_000_000)):,}"

# ---------- APP ----------
class PopulationApp:
    def __init__(self, root):
        self.root = root
        root.title("World Population Projection (2026–2150) — Animated")
        root.geometry("1180x820")
        root.configure(bg="#f4f6fa")

        self.anim_running = False
        self.anim_job = None
        self.current_year = MIN_YEAR

        # ---------- Top controls ----------
        top = tk.Frame(root, bg="#ffffff")
        top.pack(side=tk.TOP, fill=tk.X)

        tk.Label(top, text="Start Year:", bg="#ffffff",
                 font=("Segoe UI", 11)).pack(side=tk.LEFT, padx=(15, 5), pady=12)
        self.start_var = tk.IntVar(value=MIN_YEAR)
        tk.Spinbox(top, from_=MIN_YEAR, to=MAX_YEAR, textvariable=self.start_var,
                   width=7, font=("Segoe UI", 11)).pack(side=tk.LEFT)

        tk.Label(top, text="End Year:", bg="#ffffff",
                 font=("Segoe UI", 11)).pack(side=tk.LEFT, padx=(20, 5))
        self.end_var = tk.IntVar(value=MAX_YEAR)
        tk.Spinbox(top, from_=MIN_YEAR, to=MAX_YEAR, textvariable=self.end_var,
                   width=7, font=("Segoe UI", 11)).pack(side=tk.LEFT)

        ttk.Button(top, text="Plot",  command=self.plot).pack(side=tk.LEFT, padx=15)
        ttk.Button(top, text="Reset", command=self.reset).pack(side=tk.LEFT)

        # ---------- Animation controls ----------
        anim_bar = tk.Frame(root, bg="#eef2f8")
        anim_bar.pack(side=tk.TOP, fill=tk.X)

        tk.Label(anim_bar, text="Animation:", bg="#eef2f8",
                 font=("Segoe UI", 11, "bold")).pack(side=tk.LEFT, padx=(15, 10), pady=10)

        ttk.Button(anim_bar, text="▶ Start",
                   command=self.start_animation).pack(side=tk.LEFT, padx=4)
        ttk.Button(anim_bar, text="■ Stop",
                   command=self.stop_animation).pack(side=tk.LEFT, padx=4)

        tk.Label(anim_bar, text="Seconds per year:", bg="#eef2f8",
                 font=("Segoe UI", 10)).pack(side=tk.LEFT, padx=(20, 5))
        self.speed_var = tk.DoubleVar(value=1.0)
        tk.Spinbox(anim_bar, from_=0.1, to=10.0, increment=0.1,
                   textvariable=self.speed_var, width=6,
                   font=("Segoe UI", 10)).pack(side=tk.LEFT)

        self.year_label = tk.Label(anim_bar, text="Year: —", bg="#eef2f8",
                                   fg="#1f6feb",
                                   font=("Segoe UI", 12, "bold"))
        self.year_label.pack(side=tk.LEFT, padx=25)

        # ---------- Live population counter ----------
        counter_frame = tk.Frame(root, bg="#0d1b2a")
        counter_frame.pack(side=tk.TOP, fill=tk.X)

        tk.Label(counter_frame, text="POPULATION", bg="#0d1b2a",
                 fg="#8fbcd4", font=("Segoe UI", 11, "bold")).pack(pady=(10, 0))

        self.counter_label = tk.Label(counter_frame, text="—",
                                      bg="#0d1b2a", fg="#7ef0c8",
                                      font=("Consolas", 26, "bold"))
        self.counter_label.pack(pady=(0, 12))

        # ---------- Graph area ----------
        self.fig = Figure(figsize=(10.5, 5.4), dpi=100)
        self.ax = self.fig.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.fig, master=root)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.plot()

    # ---------------- static full plot ----------------
    def plot(self):
        try:
            y0 = int(self.start_var.get())
            y1 = int(self.end_var.get())
        except Exception:
            messagebox.showerror("Invalid input", "Please enter valid years.")
            return
        if y0 < MIN_YEAR or y1 > MAX_YEAR or y0 >= y1:
            messagebox.showerror("Invalid range",
                                 f"Years must satisfy {MIN_YEAR} ≤ start < end ≤ {MAX_YEAR}.")
            return

        self.stop_animation()
        self.current_year = y0
        self.year_label.config(text="Year: —")
        self.counter_label.config(text=fmt_people(pop_at(y0)))
        self._draw_static(y0, y1)

    def _draw_static(self, y0, y1):
        mask = (years_all >= y0) & (years_all <= y1)
        y = years_all[mask]; p = pop_all[mask]
        exact  = y <= 2100
        linear = y >= 2101

        self.ax.clear()
        if exact.any():
            self.ax.plot(y[exact], p[exact], color=BLUE_EXACT,
                         linewidth=2.2, label="Projection (2026–2100)")
        if linear.any():
            # include the 2100 anchor so the two segments connect seamlessly
            if 2100 in years_all and y0 <= 2100 <= y1:
                anchor_x = [2100] + list(y[linear])
                anchor_y = [pop_at(2100)] + list(p[linear])
            else:
                anchor_x, anchor_y = y[linear], p[linear]
            self.ax.plot(anchor_x, anchor_y, color=BLUE_LINEAR,
                         linewidth=2.2, label="Linear projection (2101–2150)")

        if y0 <= PEAK_YEAR <= y1:
            self.ax.scatter([PEAK_YEAR], [PEAK_POP], color="crimson", s=70, zorder=5)
            self.ax.annotate("Peak 2084\n10.29 B",
                             xy=(PEAK_YEAR, PEAK_POP),
                             xytext=(PEAK_YEAR + (y1 - y0) * 0.05,
                                     PEAK_POP - (p.max() - p.min()) * 0.35),
                             arrowprops=dict(arrowstyle="->", color="crimson"),
                             fontsize=10, color="crimson", fontweight="bold")

        self._style_axes(y0, y1)
        self.canvas.draw()

    def _style_axes(self, y0, y1):
        self.ax.set_title(f"World Population Projection ({y0}–{y1})",
                          fontsize=14, fontweight="bold")
        self.ax.set_xlabel("Year", fontsize=11)
        self.ax.set_ylabel("Population (billions)", fontsize=11)
        self.ax.set_xlim(y0, y1)
        self.ax.grid(True, alpha=0.3)
        self.ax.legend(fontsize=10, loc="upper left")
        self.ax.yaxis.set_major_formatter(
            mticker.FuncFormatter(lambda x, _: f"{x:.1f} B"))
        self.fig.tight_layout()

    # ---------------- animation ----------------
    def start_animation(self):
        try:
            y0 = int(self.start_var.get())
            y1 = int(self.end_var.get())
        except Exception:
            messagebox.showerror("Invalid input", "Please enter valid years.")
            return
        if y0 < MIN_YEAR or y1 > MAX_YEAR or y0 >= y1:
            messagebox.showerror("Invalid range",
                                 f"Years must satisfy {MIN_YEAR} ≤ start < end ≤ {MAX_YEAR}.")
            return

        self.stop_animation()
        self.anim_running = True
        self.current_year = y0
        self.anim_y0, self.anim_y1 = y0, y1

        self.counter_label.config(text=fmt_people(pop_at(y0)))
        self.year_label.config(text=f"Year: {y0}")

        self.ax.clear()
        self._style_axes(y0, y1)

        # Two lines, both blue; the second one becomes active only after 2100
        self.line_exact,  = self.ax.plot([], [], color=BLUE_EXACT, linewidth=2.2,
                                         label="Projection (2026–2100)")
        self.line_linear, = self.ax.plot([], [], color=BLUE_LINEAR, linewidth=2.2,
                                         label="Linear projection (2101–2150)")
        self.ax.legend(fontsize=10, loc="upper left")

        self.peak_dot = self.ax.scatter([], [], color="crimson", s=70, zorder=5)
        self.peak_text = self.ax.annotate("", xy=(0, 0), xytext=(0, 0),
                                          fontsize=10, color="crimson",
                                          fontweight="bold")
        self.canvas.draw()

        self._animate_step()

    def _animate_step(self):
        if not self.anim_running:
            return

        y0, y1 = self.anim_y0, self.anim_y1
        cy = self.current_year

        mask = (years_all >= y0) & (years_all <= cy)
        y = years_all[mask]; p = pop_all[mask]
        exact_mask  = y <= 2100
        linear_mask = y >= 2101

        self.line_exact.set_data(y[exact_mask], p[exact_mask])

        # Linear segment: connect to the 2100 anchor for a seamless join
        if linear_mask.any():
            anchor_x = [2100] + list(y[linear_mask])
            anchor_y = [pop_at(2100)] + list(p[linear_mask])
            self.line_linear.set_data(anchor_x, anchor_y)
        else:
            self.line_linear.set_data([], [])

        if cy >= PEAK_YEAR:
            self.peak_dot.set_offsets([[PEAK_YEAR, PEAK_POP]])
            self.peak_text.set_text("Peak 2084\n10.29 B")
            self.peak_text.xy = (PEAK_YEAR, PEAK_POP)
            span = max(pop_all[mask].max() - pop_all[mask].min(), 0.001)
            self.peak_text.set_position(
                (PEAK_YEAR + (y1 - y0) * 0.05, PEAK_POP - span * 0.35))
        else:
            self.peak_dot.set_offsets(np.empty((0, 2)))
            self.peak_text.set_text("")

        self.year_label.config(text=f"Year: {cy}")
        self.counter_label.config(text=fmt_people(pop_at(cy)))

        self.canvas.draw_idle()

        if cy >= y1:
            self.anim_running = False
            self.year_label.config(text=f"Year: {y1}  (done)")
            self.counter_label.config(text=fmt_people(pop_at(y1)))
            return

        self.current_year = cy + 1
        delay_ms = max(int(self.speed_var.get() * 1000), 50)
        self.anim_job = self.root.after(delay_ms, self._animate_step)

    def stop_animation(self):
        self.anim_running = False
        if self.anim_job is not None:
            try:
                self.root.after_cancel(self.anim_job)
            except Exception:
                pass
            self.anim_job = None

    # ---------------- reset ----------------
    def reset(self):
        self.stop_animation()
        self.start_var.set(MIN_YEAR)
        self.end_var.set(MAX_YEAR)
        self.current_year = MIN_YEAR
        self.year_label.config(text="Year: —")
        self.counter_label.config(text="—")
        self.plot()


if __name__ == "__main__":
    root = tk.Tk()
    style = ttk.Style(root)
    try:
        style.theme_use("clam")
    except Exception:
        pass
    app = PopulationApp(root)
    root.mainloop()