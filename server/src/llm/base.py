from abc import ABC, abstractmethod

class BaseLLM(ABC):
    def __init__(self):
        self.token_usage = {"prompt_tokens": 0, "generated_tokens": 0}

    # def _apply_decorator(self, method, decorators, *args, **kwargs):
    #     for decorator in decorators:
    #         method = decorator(method)
    #     return method(self, *args, **kwargs)

    @abstractmethod
    # def _raw_gen(self, model, messages, stream, *args, **kwargs):
    def _raw_gen(self, messages, *args, **kwargs):

        pass

    def gen(self, messages, stream=False, *args, **kwargs):
        # decorators = [gen_token_usage, gen_cache]
        # return self._apply_decorator(self._raw_gen, decorators=decorators, model=model, messages=messages, stream=stream, tools=tools, *args, **kwargs)
        return self._raw_gen(messages, **kwargs)