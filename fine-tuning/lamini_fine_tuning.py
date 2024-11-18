import lamini
import os

from lamini import Lamini
from data.get_data import get_data
from dotenv import load_dotenv
load_dotenv()

lamini.api_key = os.getenv('LAMINI_API_KEY')

data = get_data()

llm = Lamini(model_name='meta-llama/Meta-Llama-3-8B-Instruct')

llm.tune(
    data_or_dataset_id=data,
    finetune_args={
        'learning_rate': 1.0e-4,
        'optim': 'adamw_hf',
        'r_value': 8
    }
)



