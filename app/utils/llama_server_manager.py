import requests

from PySide6.QtCore import QObject, QProcess, QTimer, Signal


class LlamaServerManager(QObject):
    started = Signal()
    failed = Signal(str)

    SERVER_URL = "http://127.0.0.1:8080"
    HEALTH_URL = f"{SERVER_URL}/health"

    def __init__(self, parent=None):
        super().__init__(parent)

        self.process = None
        self.health_timer = None
        self._ready = False

    def start(self):
        # Check whether llama-server is already running
        if self._is_server_running():
            self._ready = True
            self.started.emit()
            return

        self.process = QProcess(self)
        '''
        # Prevent a separate CMD window from appearing
        self.process.setCreateProcessArgumentsModifier(
            lambda args: args.setCreateProcessArgumentsModifier
            if False else None
        )
        '''
        self.process.readyReadStandardError.connect(
            self._read_process_error
        )

        self.process.errorOccurred.connect(
            self._process_error
        )

        self.process.finished.connect(
            self._process_finished
        )

        self.process.start(
            "llama-server",
            [
                "-hf",
                "Qwen/Qwen3-4B-GGUF:Q4_K_M",
                "--reasoning",
                "off"
            ]
        )

        if not self.process.waitForStarted(3000):
            self.failed.emit(
                "Could not start llama-server.\n\n"
                "Make sure llama-server is installed and available "
                "in your PATH."
            )
            return

        # Check /health until the server becomes ready
        self.health_timer = QTimer(self)
        self.health_timer.timeout.connect(
            self._check_health
        )
        self.health_timer.start(1000)

    def _is_server_running(self):
        try:
            response = requests.get(
                self.HEALTH_URL,
                timeout=1
            )

            return response.status_code == 200

        except requests.RequestException:
            return False

    def _check_health(self):
        if self._is_server_running():
            self._ready = True

            if self.health_timer:
                self.health_timer.stop()

            self.started.emit()

    def is_ready(self):
        return self._ready and self._is_server_running()

    def stop(self):
        if self.health_timer:
            self.health_timer.stop()
            self.health_timer.deleteLater()
            self.health_timer = None

        if self.process:
            if self.process.state() != QProcess.NotRunning:
                self.process.terminate()

                if not self.process.waitForFinished(3000):
                    self.process.kill()
                    self.process.waitForFinished(1000)

            self.process.deleteLater()
            self.process = None

        self._ready = False

    def _process_error(self, error):
        if self._ready:
            return

        self.failed.emit(
            "llama-server could not be started.\n\n"
            "Please check that llama-server is installed "
            "and available in PATH."
        )

    def _process_finished(self, exit_code, exit_status):
        if self._ready:
            self._ready = False

    def _read_process_error(self):
        if not self.process:
            return

        output = bytes(
            self.process.readAllStandardError()
        ).decode(
            "utf-8",
            errors="ignore"
        )

        # Useful during development if something goes wrong.
        if output.strip():
            print(
                "[llama-server]",
                output.strip()
            )