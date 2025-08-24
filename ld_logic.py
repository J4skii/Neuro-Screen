def evaluate_dyslexia(answers):
    key = ['b','b','a','a','b']
    score = sum(1 for a,k in zip(answers, key) if a == k)
    return {
        "type": "Dyslexia",
        "score": score,
        "flag": score < 3,
        "message": "Possible signs of dyslexia" if score < 3 else "No major signs detected."
    }

def evaluate_dyscalculia(answers):
    key = ['c','b','a','a','b']
    score = sum(1 for a,k in zip(answers, key) if a == k)
    return {
        "type": "Dyscalculia",
        "score": score,
        "flag": score < 3,
        "message": "Possible signs of dyscalculia" if score < 3 else "No major signs detected."
    }

def evaluate_memory(selected, correct):
    tp = len([s for s in selected if s in correct])
    fp = len([s for s in selected if s not in correct])
    fn = len([c for c in correct if c not in selected])
    total = len(correct)
    score = tp
    flag = (score < (total/2)) or (fp >= 2)
    message = "Possible working memory challenges" if flag else "Working memory within typical range."
    return {
        "type": "Working Memory",
        "score": score,
        "flag": flag,
        "message": message,
        "tp": tp, "fp": fp, "fn": fn
    }
