
# utils.py 或直接写在 main.py 中
import sys
from PySide6.QtCore import Signal, QObject

class PrintRedirector(QObject):
    # 定义一个信号，用于线程安全地更新 GUI
    print_signal = Signal(str)

    def __init__(self, text_widget):
        super().__init__()
        self.text_widget = text_widget
        # 连接信号到显示函数
        self.print_signal.connect(self.display_message)

    def write(self, text):
        # 过滤空文本（比如 print() 换行）
        if text.strip():
            # 发射信号（线程安全）
            self.print_signal.emit(text.strip())

    def display_message(self, message):
        """在 GUI 组件中显示消息"""
        self.text_widget.appendPlainText(message)
        # 自动滚动到底部
        scrollbar = self.text_widget.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())

    def flush(self):
        # 兼容 stdout 要求
        pass