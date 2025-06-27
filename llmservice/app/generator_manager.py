# generator_manager.py
import threading
from app.generator import Generator
from app.models import Model
import torch
from app.context_handler import save_utterance, get_recent_segments

torch.set_grad_enabled(False)
torch.backends.cuda.matmul.allow_tf32 = True
torch.backends.cudnn.benchmark = True
torch.set_float32_matmul_precision('high')  # or 'medium'

print("[INFO] CUDA Available:", torch.cuda.is_available())
print("[INFO] CUDA Device:", torch.cuda.get_device_name(0) if torch.cuda.is_available() else "N/A")
print("[INFO] Current Device:", torch.cuda.current_device())
print("[INFO] Memory Allocated:", torch.cuda.memory_allocated() // 1024**2, "MB")
print("[INFO] Memory Reserved:", torch.cuda.memory_reserved() // 1024**2, "MB")


class GeneratorManager:
    def __init__(self, device="cuda"):
        self.lock = threading.Lock()
        self.model = Model.from_pretrained("sesame/csm-1b").to(device=device, dtype=torch.float32)
        self.generator = Generator(self.model)
        for name, param in self.generator._model.named_parameters():
            if param.device.type != "cuda":
                print(f"[WARNING] Parameter {name} is on {param.device}")
        # self.warm_up()

    def run_safe(self, *args, **kwargs):
        with self.lock:
            assert torch.cuda.is_available(), "CUDA not available!"
            assert next(self.generator._model.parameters()).is_cuda, "Model not on GPU"

            # if the 'speaker' argument is passed, let's get segments
            if 'speaker' in kwargs:
                speaker_id = kwargs['speaker']
                recent_segments = get_recent_segments(speaker_id, self.generator.sample_rate)
                kwargs['context'] = recent_segments
            return self.generator.generate(*args, **kwargs)

    def warm_up(self):
        print("[🚀] Warming up generator...")
        try:
            _ = self.generator.generate(
                text="Hello world.",
                speaker=0,
                context=[],
                max_audio_length_ms=1000,
                temperature=0.7,
                topk=20
            )
            print("[✅] Generator warm-up complete.")
        except Exception as e:
            print(f"[⚠️] Warm-up failed: {e}")

class GeneratorLoader:
    """
    Singleton class to manage a preloaded GeneratorManager instance.
    This avoids reloading the model on every request.
    """
    _instance = None
    _preloaded_generator_manager = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(GeneratorLoader, cls).__new__(cls)
            cls._instance._preloaded_generator_manager = None
        return cls._instance

    def __init__(cls):
        cls._instance._preloaded_generator_manager = None

    def get_generator_manager(cls):
        """
        Returns a preloaded GeneratorManager instance.
        This is useful for avoiding reloading the model on every request.
        """
        if cls._instance._preloaded_generator_manager is None:
            cls._instance._preloaded_generator_manager = GeneratorManager(device="cuda")
            print("[INFO] Preloaded GeneratorManager instance created.")
        
        return cls._instance._preloaded_generator_manager