import textdistance

def compare_text(alg, wrd1, wrd2):
    text_dist = getattr(textdistance, alg)
    result = text_dist(wrd1, wrd2)
    return result
