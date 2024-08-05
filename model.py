from modelscope import AutoModelForCausalLM, AutoTokenizer

device='cuda'
class Qwen():

    def __init__(self,model_name_path="qwen/Qwen2-0.5B"):
        self.model = AutoModelForCausalLM.from_pretrained(model_name_path,torch_dtype='auto',device_map='auto')
        self.tokenizer = AutoTokenizer.from_pretrained(model_name_path)

    def chat(self,input_text,history=None):

        model_inputs = self.tokenizer([input_text],return_tensors="pt").to(device)
        generate_ids = self.model.generate(model_inputs.input_ids,max_new_tokens=400,repetition_penalty=1.15)

        generate_ids = [
             output_ids[len(input_ids):]  for input_ids,output_ids in zip(model_inputs.input_ids,generate_ids)
        ]

        return self.tokenizer.batch_decode(generate_ids,skip_special_tokens=True)[0]

from vllm import LLM,SamplingParams


class QwenVllm():

     def __int__(self,model_path,temperature=0.8):
        prompts = ["Hello, my name is LiLei"]
        self.sampling_params = SamplingParams(temperature=temperature,top_p=0.95)

        self.model = LLM(model=model_path)

     def chat(self,message):

        outputs = self.model(message,self.sampling_params)
        return outputs[0].outputs[0].text




