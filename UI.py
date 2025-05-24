import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import os
import time


class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("文本段落处理工具")
        self.geometry("900x770")
        self.configure(bg="#f0f0f0")

        # 设置中文字体
        self.font_config()

        # 创建界面组件
        self.create_widgets()

        # 绑定窗口关闭事件
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

    def font_config(self):
        """配置中文字体"""
        import tkinter.font as tkfont
        default_font = tkfont.nametofont("TkDefaultFont")
        default_font.configure(family="SimHei", size=10)
        self.option_add("*Font", default_font)

    def create_widgets(self):
        """创建界面组件"""
        # 创建主框架
        main_frame = ttk.Frame(self, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # 标题
        title_label = ttk.Label(main_frame, text="文本段落处理工具", font=("SimHei", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20), sticky="w")

        # 源文件选择区域
        ttk.Label(main_frame, text="源文件:").grid(row=1, column=0, sticky="w", pady=5)
        self.source_path_var = tk.StringVar()
        source_entry = ttk.Entry(main_frame, textvariable=self.source_path_var, width=50)
        source_entry.grid(row=1, column=1, sticky="ew", pady=5, padx=(10, 0))

        browse_btn = ttk.Button(main_frame, text="浏览...", command=self.browse_file)
        browse_btn.grid(row=1, column=2, padx=10, pady=5)

        # 目标文件夹选择区域
        ttk.Label(main_frame, text="目标文件夹:").grid(row=2, column=0, sticky="w", pady=5)
        self.dest_path_var = tk.StringVar()
        dest_entry = ttk.Entry(main_frame, textvariable=self.dest_path_var, width=50)
        dest_entry.grid(row=2, column=1, sticky="ew", pady=5, padx=(10, 0))

        browse_dir_btn = ttk.Button(main_frame, text="浏览...", command=self.browse_directory)
        browse_dir_btn.grid(row=2, column=2, padx=10, pady=5)

        # 处理选项
        options_frame = ttk.LabelFrame(main_frame, text="处理选项", padding="10")
        options_frame.grid(row=3, column=0, columnspan=3, sticky="ew", pady=10)

        self.option1_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(options_frame, text="选项 1: 执行数据清洗", variable=self.option1_var).grid(row=0, column=0,
                                                                                                    sticky="w", padx=5,
                                                                                                    pady=5)

        self.option2_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(options_frame, text="选项 2: 生成报告", variable=self.option2_var).grid(row=0, column=1,
                                                                                                sticky="w", padx=5,
                                                                                                pady=5)

        self.option3_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(options_frame, text="选项 3: 高级处理", variable=self.option3_var).grid(row=1, column=0,
                                                                                                sticky="w", padx=5,
                                                                                                pady=5)

        self.option4_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(options_frame, text="选项 4: 自动添加txt", variable=self.option4_var).grid(row=1, column=1,
                                                                                                   sticky="w", padx=5,
                                                                                                   pady=5)

        # 自定义段落处理区域
        paragraphs_frame = ttk.LabelFrame(main_frame, text="自定义段落处理", padding="10")
        paragraphs_frame.grid(row=4, column=0, columnspan=3, sticky="nsew", pady=10)

        # 段落规则表格
        columns = ("起始标识", "结束标识", "保存文件名")
        self.paragraph_tree = ttk.Treeview(paragraphs_frame, columns=columns, show="headings", height=5)

        for col in columns:
            self.paragraph_tree.heading(col, text=col)
            self.paragraph_tree.column(col, width=200, anchor=tk.W)

        self.paragraph_tree.grid(row=0, column=0, columnspan=3, sticky="nsew", pady=5)

        # 添加/编辑/删除按钮
        btn_frame = ttk.Frame(paragraphs_frame)
        btn_frame.grid(row=1, column=0, columnspan=3, sticky="ew", pady=5)

        add_btn = ttk.Button(btn_frame, text="添加规则", command=self.add_paragraph_rule)
        add_btn.pack(side=tk.LEFT, padx=5)

        edit_btn = ttk.Button(btn_frame, text="编辑选中", command=self.edit_paragraph_rule)
        edit_btn.pack(side=tk.LEFT, padx=5)

        delete_btn = ttk.Button(btn_frame, text="删除选中", command=self.delete_paragraph_rule)
        delete_btn.pack(side=tk.LEFT, padx=5)

        # 进度条
        ttk.Label(main_frame, text="处理进度:").grid(row=5, column=0, sticky="w", pady=5)
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(main_frame, variable=self.progress_var, length=500)
        self.progress_bar.grid(row=5, column=1, sticky="ew", pady=5, padx=(10, 0))

        # 日志区域
        ttk.Label(main_frame, text="处理日志:").grid(row=6, column=0, sticky="nw", pady=5)
        self.log_text = tk.Text(main_frame, height=10, width=70, wrap=tk.WORD)
        self.log_text.grid(row=6, column=1, sticky="nsew", pady=5, padx=(10, 0))

        scrollbar = ttk.Scrollbar(main_frame, command=self.log_text.yview)
        scrollbar.grid(row=6, column=2, sticky="ns", pady=5)
        self.log_text.config(yscrollcommand=scrollbar.set)

        # 状态栏
        self.status_var = tk.StringVar(value="就绪")
        status_bar = ttk.Label(self, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)

        # 按钮区域
        button_frame = ttk.Frame(self)
        button_frame.pack(side=tk.BOTTOM, pady=20)

        start_btn = ttk.Button(button_frame, text="开始处理", command=self.start_processing, width=15)
        start_btn.pack(side=tk.LEFT, padx=10)

        cancel_btn = ttk.Button(button_frame, text="取消", command=self.on_closing, width=15)
        cancel_btn.pack(side=tk.LEFT, padx=10)

        # 设置列和行的权重，使界面可以自适应调整
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(6, weight=1)
        paragraphs_frame.columnconfigure(0, weight=1)
        paragraphs_frame.rowconfigure(0, weight=1)

    def browse_file(self):
        """浏览并选择文件"""
        filename = filedialog.askopenfilename(
            title="选择文件",
            filetypes=[("文本文件", "*.txt"), ("所有文件", "*.*")]
        )
        if filename:
            self.source_path_var.set(filename)
            self.log(f"已选择文件: {filename}")

    def browse_directory(self):
        """浏览并选择目录"""
        directory = filedialog.askdirectory(title="选择目标文件夹")
        if directory:
            self.dest_path_var.set(directory)
            self.log(f"已选择目标文件夹: {directory}")

    def log(self, message):
        """向日志区域添加消息"""
        timestamp = time.strftime("%H:%M:%S")
        self.log_text.insert(tk.END, f"[{timestamp}] {message}\n")
        self.log_text.see(tk.END)  # 滚动到最新日志

    def update_status(self, message):
        """更新状态栏消息"""
        self.status_var.set(message)
        self.update_idletasks()  # 立即更新UI

    def update_progress(self, value):
        """更新进度条"""
        self.progress_var.set(value)
        self.update_idletasks()  # 立即更新UI

    def add_paragraph_rule(self):
        """添加段落处理规则"""
        # 创建对话框
        dialog = tk.Toplevel(self)
        dialog.title("添加段落处理规则")
        dialog.geometry("400x250")
        dialog.transient(self)
        dialog.grab_set()

        # 居中显示
        dialog.update_idletasks()
        width = dialog.winfo_width()
        height = dialog.winfo_height()
        x = (self.winfo_width() // 2) - (width // 2) + self.winfo_rootx()
        y = (self.winfo_height() // 2) - (height // 2) + self.winfo_rooty()
        dialog.geometry(f"+{x}+{y}")

        # 创建输入框
        ttk.Label(dialog, text="起始标识:").grid(row=0, column=0, sticky="w", padx=10, pady=10)
        start_marker = ttk.Entry(dialog, width=40)
        start_marker.grid(row=0, column=1, sticky="ew", padx=10, pady=10)

        ttk.Label(dialog, text="结束标识:").grid(row=1, column=0, sticky="w", padx=10, pady=10)
        end_marker = ttk.Entry(dialog, width=40)
        end_marker.grid(row=1, column=1, sticky="ew", padx=10, pady=10)

        ttk.Label(dialog, text="保存文件名:").grid(row=2, column=0, sticky="w", padx=10, pady=10)
        file_name = ttk.Entry(dialog, width=40)
        file_name.grid(row=2, column=1, sticky="ew", padx=10, pady=10)

        # 确认按钮
        def on_confirm():
            sm = start_marker.get().strip()
            em = end_marker.get().strip()
            fn = file_name.get().strip()

            if not sm or not em or not fn:
                messagebox.showerror("错误", "请填写完整的规则信息")
                return

            # 添加到表格
            self.paragraph_tree.insert("", tk.END, values=(sm, em, fn))
            dialog.destroy()

        ttk.Button(dialog, text="确定", command=on_confirm).grid(row=3, column=0, pady=20)
        ttk.Button(dialog, text="取消", command=dialog.destroy).grid(row=3, column=1, pady=20)

        dialog.columnconfigure(1, weight=1)

    def edit_paragraph_rule(self):
        """编辑选中的段落处理规则"""
        selected_item = self.paragraph_tree.selection()
        if not selected_item:
            messagebox.showinfo("提示", "请先选择要编辑的规则")
            return

        if len(selected_item) > 1:
            messagebox.showinfo("提示", "每次只能编辑一条规则")
            return

        item = selected_item[0]
        values = self.paragraph_tree.item(item, "values")

        # 创建对话框
        dialog = tk.Toplevel(self)
        dialog.title("编辑段落处理规则")
        dialog.geometry("400x250")
        dialog.transient(self)
        dialog.grab_set()

        # 居中显示
        dialog.update_idletasks()
        width = dialog.winfo_width()
        height = dialog.winfo_height()
        x = (self.winfo_width() // 2) - (width // 2) + self.winfo_rootx()
        y = (self.winfo_height() // 2) - (height // 2) + self.winfo_rooty()
        dialog.geometry(f"+{x}+{y}")

        # 创建输入框并填充当前值
        ttk.Label(dialog, text="起始标识:").grid(row=0, column=0, sticky="w", padx=10, pady=10)
        start_marker = ttk.Entry(dialog, width=40)
        start_marker.insert(0, values[0])
        start_marker.grid(row=0, column=1, sticky="ew", padx=10, pady=10)

        ttk.Label(dialog, text="结束标识:").grid(row=1, column=0, sticky="w", padx=10, pady=10)
        end_marker = ttk.Entry(dialog, width=40)
        end_marker.insert(0, values[1])
        end_marker.grid(row=1, column=1, sticky="ew", padx=10, pady=10)

        ttk.Label(dialog, text="保存文件名:").grid(row=2, column=0, sticky="w", padx=10, pady=10)
        file_name = ttk.Entry(dialog, width=40)
        file_name.insert(0, values[2])
        file_name.grid(row=2, column=1, sticky="ew", padx=10, pady=10)

        # 确认按钮
        def on_confirm():
            sm = start_marker.get().strip()
            em = end_marker.get().strip()
            fn = file_name.get().strip()

            if not sm or not em or not fn:
                messagebox.showerror("错误", "请填写完整的规则信息")
                return

            # 更新表格中的数据
            self.paragraph_tree.item(item, values=(sm, em, fn))
            dialog.destroy()

        ttk.Button(dialog, text="确定", command=on_confirm).grid(row=3, column=0, pady=20)
        ttk.Button(dialog, text="取消", command=dialog.destroy).grid(row=3, column=1, pady=20)

        dialog.columnconfigure(1, weight=1)

    def delete_paragraph_rule(self):
        """删除选中的段落处理规则"""
        selected_item = self.paragraph_tree.selection()
        if not selected_item:
            messagebox.showinfo("提示", "请先选择要删除的规则")
            return

        for item in selected_item:
            self.paragraph_tree.delete(item)

    def start_processing(self):
        """开始处理数据"""
        source_file = self.source_path_var.get()
        dest_folder = self.dest_path_var.get()

        # 检查输入
        if not source_file:
            messagebox.showerror("错误", "请选择源文件")
            return

        if not dest_folder:
            messagebox.showerror("错误", "请选择目标文件夹")
            return

        # 获取段落规则
        paragraphs = []
        for item in self.paragraph_tree.get_children():
            values = self.paragraph_tree.item(item, "values")
            paragraphs.append(values)

        if not paragraphs:
            messagebox.showerror("错误", "请添加段落处理规则")
            return

        # 清空日志
        self.log_text.delete(1.0, tk.END)

        # 开始处理
        self.log("开始处理数据...")
        self.update_status("处理中...")

        try:
            # 读取源文件
            with open(source_file, 'r', encoding='utf-8') as f:
                content = f.read()

            total_steps = len(paragraphs)
            for i, (start_marker, end_marker, file_name) in enumerate(paragraphs, 1):
                self.log(f"正在处理段落 {i}/{total_steps}: {file_name}")

                # 查找段落位置
                start_index = content.find(start_marker)
                end_index = content.find(end_marker)

                if start_index == -1:
                    self.log(f"警告: 未找到段落起始标识 '{start_marker}'")
                    continue

                if end_index == -1:
                    self.log(f"警告: 未找到段落结束标识 '{end_marker}'")
                    continue

                end_index += len(end_marker)

                # 提取段落内容
                paragraph_content = content[start_index:end_index]

                # 自动添加.txt后缀
                if self.option4_var.get() and not file_name.lower().endswith('.txt'):
                    file_name += '.txt'

                # 保存文件
                output_path = os.path.join(dest_folder, file_name)
                with open(output_path, 'w', encoding='utf-8') as f:
                    f.write(paragraph_content)

                self.log(f"成功保存段落至: {output_path}")
                self.update_progress(i / total_steps * 100)

            self.log(f"处理完成！共处理 {total_steps} 个段落")
            self.update_status("处理完成")
            messagebox.showinfo("成功", f"数据处理完成！共处理 {total_steps} 个段落")

        except Exception as e:
            self.log(f"错误: {str(e)}")
            self.update_status("处理失败")
            messagebox.showerror("处理失败", f"发生错误: {str(e)}")

    def on_closing(self):
        """窗口关闭时的处理"""
        if messagebox.askokcancel("退出", "确定要退出程序吗?"):
            self.destroy()


if __name__ == "__main__":
    app = Application()
    app.mainloop()
