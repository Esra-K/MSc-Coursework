<h1 align="left" id="title">Exchange Market Price Predicition</h1>

<p id="description">In this project we trained a model called "LLM for Candlestick" to predict exchange market price. For this purpose we used a pretrained GPT-2 as the core of our model. As input our model takes sequence of candlesticks and predicts the next one.</p>

<h2 align="left" id="title">Models</h2>

- GPT-2
- Embedding-based
- Word-based
- Window-based


<h2 align="left" id="title">Results</h2>

<p id="description">Original Chart</p>

<img src="https://github.com/NLP-Final-Projects/LLMs_for_financial_data/blob/a1e630db6bad129c9075a4f3087211837c3a99eb/images/original.png" alt="project-screenshot" width="768.6" height="315/">

<p id="description">Predicted Chart</p>

<img src="https://github.com/NLP-Final-Projects/LLMs_for_financial_data/blob/6a19017ca6260fea4dae7c4c1e41d2816a7a6432/images/predicted.png" alt="project-screenshot" width="768.6" height="315/">

<h2 align="left" id="title">How to Use</h2>

<h4 align="left" id="title">Embedding-based</h4>

```python
  import pandas as pd
  import torch
  from transformers import GPT2Model
  from models.CustomGPT import CustomGPT

  WINDOW_SIZE = 10 # The model is trained on window size 10
  
  # Read Data, here for demonstration we use USDCAD Daily
  data = pd.read_csv('./datasets/USDCAD_D1.csv', header=None)
  data.columns = ['time', 'open', 'high', 'low', 'close', 'volume']

  # We only need open, high, low, close features
  data = data[['open', 'high', 'low', 'close']]

  # Selectiong window
  window = data.ilco[-WINDOW_SIZE:] # This way we will predict next day candlestick

  # Model instantiation
  gpt_pretrained = GPT2Model.from_pretrained('gpt2')
  del gpt_pretrained.wte

  model = CustomGPT(gpt_pretrained, WINDOW_SIZE)

  # Loading weights
  model.load_state_dict(torch.load(PATH))
  model.eval()

  # Creating input tensor
  input_tensor = torch.tensor(window.to_numpy(), dtype=torch.float32)

  # Predicting next candlestick
  candle_pred = model(input_tensor.unsqueeze(0))[0][-1]
```
