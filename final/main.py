import requests
import json
import pandas as pd
from difflib import SequenceMatcher

MODEL = "llama3.2"

# -----------------------
# 呼叫 Ollama
# -----------------------

def ask_llm(prompt):

    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": MODEL,
            "prompt": prompt,
            "stream": False
        }
    )

    return response.json()["response"]


# -----------------------
# 自動評分
# -----------------------

def similarity(a, b):

    return SequenceMatcher(
        None,
        a.lower(),
        b.lower()
    ).ratio()


# -----------------------
# 主程式
# -----------------------

with open("prompts.json", "r", encoding="utf8") as f:
    prompts = json.load(f)

with open("questions.json", "r", encoding="utf8") as f:
    questions = json.load(f)

results = []

for prompt_info in prompts:

    prompt_name = prompt_info["name"]
    template = prompt_info["prompt"]

    print("\n===================")
    print(prompt_name)
    print("===================\n")

    total_score = 0

    for q in questions:

        question = q["question"]
        answer = q["answer"]

        prompt = template.format(
            question=question
        )

        llm_answer = ask_llm(prompt)

        score = similarity(
            llm_answer,
            answer
        )

        total_score += score

        print("問題:", question)
        print("標準答案:", answer)
        print("模型答案:", llm_answer)
        print("分數:", round(score,3))
        print()

        results.append(
            {
                "Prompt": prompt_name,
                "Question": question,
                "Expected": answer,
                "Response": llm_answer,
                "Score": score
            }
        )

    avg_score = total_score / len(questions)

    print(
        f"{prompt_name} 平均分數 = {avg_score:.3f}"
    )

# -----------------------
# 儲存結果
# -----------------------

df = pd.DataFrame(results)

df.to_csv(
    "results.csv",
    index=False,
    encoding="utf-8-sig"
)

# -----------------------
# 找最佳 Prompt
# -----------------------

summary = (
    df.groupby("Prompt")["Score"]
      .mean()
      .sort_values(ascending=False)
)

best_prompt = summary.index[0]

with open(
    "report.txt",
    "w",
    encoding="utf8"
) as f:

    f.write("Prompt Engineering 實驗報告\n")
    f.write("="*40 + "\n\n")

    for p,s in summary.items():
        f.write(
            f"{p}: {s:.3f}\n"
        )

    f.write(
        f"\n最佳 Prompt: {best_prompt}\n"
    )

print("\n結果已輸出")
print("results.csv")
print("report.txt")