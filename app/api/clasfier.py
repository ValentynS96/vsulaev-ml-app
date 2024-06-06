import spacy
from fastapi import APIRouter, HTTPException
from typing import Any

from app.models.pipeline import PipelineReq, PreprocessorType
from app.services.preprocessing import preprocess_text_nltk, preprocess_text_spacy

import pickle
import os

clasfier_router = APIRouter()

models = {}
word_features = ['the', 'a', 'and', 'of', 'to', 'is', 'in', 's', 'it', 'that', 'as', 'with', 'for', 'his', 'this', 'film', 'i', 'he', 'but', 'on', 'are', 't', 'by', 'be', 'one', 'movie', 'an', 'who', 'not', 'you', 'from', 'at', 'was', 'have', 'they', 'has', 'her', 'all', 'there', 'like', 'so', 'out', 'about', 'up', 'more', 'what', 'when', 'which', 'or', 'she', 'their', 'some', 'just', 'can', 'if', 'we', 'him', 'into', 'even', 'only', 'than', 'no', 'good', 'time', 'most', 'its', 'will', 'story', 'would', 'been', 'much', 'character', 'also', 'get', 'other', 'do', 'two', 'well', 'them', 'very', 'characters', ';', 'first', '--', 'after', 'see', 'way', 'because', 'make', 'life', 'off', 'too', 'any', 'does', 'really', 'had', 'while', 'films', 'how', 'plot', 'little', 'where', 'people', 'over', 'could', 'then', 'me', 'scene', 'man', 'bad', 'my', 'never', 'being', 'best', 'these', 'don', 'new', 'doesn', 'scenes', 'many', 'director', 'such', 'know', 'were', 'movies', 'through', 'here', 'action', 'great', 're', 'another', 'love', 'go', 'made', 'us', 'big', 'end', 'something', 'back', 'still', 'world', 'seems', 'work', 'those', 'makes', 'now', 'before', 'however', 'between', 'few', 'down', 'every', 'though', 'better', 'real', 'audience', 'enough', 'seen', 'take', 'around', 'both', 'going', 'year', 'performance', 'why', 'should', 'role', 'isn', 'same', 'old', 'gets', 'your', 'may', 'things', 'think', 'years', 'last', 'comedy', 'funny', 'actually', 've', 'long', 'look', 'almost', 'own', 'thing', 'fact', 'nothing', 'say', 'right', 'john', 'although', 'played', 'find', 'script', 'come', 'ever', 'cast', 'since', 'did', 'star', 'plays', 'young', 'show', 'comes', 'm', 'part', 'original', 'actors', 'screen', 'without', 'again', 'acting', 'three', 'day', 'each', 'point', 'lot', 'least', 'takes', 'guy', 'quite', 'himself', 'away', 'during', 'family', 'effects', 'course', 'goes', 'minutes', 'interesting', 'might', 'far', 'high', 'rather', 'once', 'must', 'anything', 'place', 'set', 'yet', 'watch', 'd', 'making', 'our', 'wife', 'hard', 'always', 'fun', 'didn', 'll', 'seem', 'special', 'bit', 'times', 'trying', 'hollywood', 'instead', 'give', 'want', 'picture', 'kind', 'american', 'job', 'sense', 'woman', 'home', 'having', 'series', 'actor', 'probably', 'help', 'half', 'along', 'men', 'everything', 'pretty', 'becomes', 'sure', 'black', 'together', 'dialogue', 'money', 'become', 'gives', 'given', 'looking', 'whole', 'watching', 'father', '`', 'feel', 'everyone', 'music', 'wants', 'sex', 'less', 'done', 'horror', 'got', 'death', 'perhaps', 'city', 'next', 'especially', 'play', 'girl', 'mind', '10', 'moments', 'looks', 'completely', '2', 'reason', 'mother', 'whose', 'line', 'night', 'human', 'until', 'rest', 'performances', 'different', 'evil', 'small', 'james', 'simply', 'couple', 'put', 'let', 'anyone', 'ending', 'case', 'several', 'dead', 'michael', 'left', 'thought', 'school', 'shows', 'humor', 'true', 'lost', 'written', 'itself', 'friend', 'entire', 'getting', 'town', 'turns', 'soon', 'someone', 'second', 'main', 'stars', 'found', 'use', 'problem', 'friends', 'tv', 'top', 'name', 'begins', 'called', 'based', 'comic', 'david', 'head', 'else', 'idea', 'either', 'wrong', 'unfortunately', 'later', 'final', 'hand', 'alien', 'house', 'group', 'full', 'used', 'tries', 'often', 'against', 'war', 'sequence', 'keep', 'turn', 'playing', 'boy', 'behind', 'named', 'certainly', 'live', 'believe', 'under', 'works', 'relationship', 'face', 'hour', 'run', 'style', 'said', 'despite', 'person', 'finally', 'shot', 'book', 'doing', 'tell', 'maybe', 'nice', 'son', 'perfect', 'side', 'seeing', 'able', 'finds', 'children', 'days', 'past', 'summer', 'camera', 'won', 'including', 'mr', 'kids', 'lives', 'directed', 'moment', 'game', 'running', 'fight', 'supposed', 'video', 'car', 'matter', 'kevin', 'joe', 'lines', 'worth', '=', 'daughter', 'earth', 'starts', 'need', 'entertaining', 'white', 'start', 'writer', 'dark', 'short', 'self', 'worst', 'nearly', 'opening', 'try', 'upon', 'care', 'early', 'violence', 'throughout', 'team', 'production', 'example', 'beautiful', 'title', 'exactly', 'jack', 'review', 'major', 'drama', 'problems', 'sequences', 'obvious', 'version', 'screenplay', 'known', 'killer', 'wasn', 'robert', 'disney', 'already', 'close', 'classic', 'others', 'hit', 'kill', 'deep', 'five', 'order', 'act', 'simple', 'fine', 'themselves', 'heart', 'roles', 'jackie', 'direction', 'eyes', 'four', 'question', 'sort', 'sometimes', 'knows', 'supporting', 'coming', 'voice', 'women', 'truly', 'save', 'jokes', 'computer', 'child', 'o', 'boring', 'tom', 'level', '1', 'body', 'guys', 'genre', 'brother', 'strong', 'stop', 'room', 'space', 'lee', 'ends', 'beginning', 'ship', 'york', 'attempt', 'thriller', 'scream', 'peter', 'aren', 'husband', 'fiction', 'happens', 'hero', 'novel', 'note', 'hope', 'king', 'yes', 'says', 'tells', 'quickly', 'romantic', 'dog', 'oscar', 'stupid', 'possible', 'saw', 'lead', 'career', 'murder', 'extremely', 'manages', 'god', 'mostly', 'wonder', 'particularly', 'future', 'fans', 'sound', 'worse', 'piece', 'involving', 'de', 'appears', 'planet', 'paul', 'involved', 'mean', 'none', 'taking', 'hours', 'laugh', 'police', 'sets', 'attention', 'co', 'hell', 'eventually', 'single', 'fall', 'falls', 'material', 'emotional', 'power', 'late', 'lack', 'dr', 'van', 'result', 'elements', 'meet', 'smith', 'science', 'experience', 'bring', 'wild', 'living', 'theater', 'interest', 'leads', 'word', 'feature', 'battle', 'girls', 'alone', 'obviously', 'george', 'within', 'usually', 'enjoy', 'guess', 'among', 'taken', 'feeling', 'laughs', 'aliens', 'talk', 'chance', 'talent', '3', 'middle', 'number', 'easy', 'across', 'needs', 'attempts', 'happen', 'television', 'chris', 'deal', 'poor', 'form', 'girlfriend', 'viewer', 'release', 'killed', 'forced', 'whether', 'wonderful', 'feels', 'oh', 'tale', 'serious', 'expect', 'except', 'light', 'success', 'features', 'premise', 'happy', 'words', 'leave', 'important', 'meets', 'history', 'giving', 'crew', 'type', 'call', 'turned', 'released', 'parents', 'art', 'impressive', 'mission', 'working', 'seemed', 'score', 'told', 'recent', 'robin', 'basically', 'entertainment', 'america', 'surprise', 'apparently', 'easily', 'ryan', 'cool', 'stuff', 'cop', 'change', 'williams', 'crime', 'office', 'parts', 'somehow', 'sequel', 'william', 'cut', 'die', 'jones', 'credits', 'batman', 'suspense', 'brings', 'events', 'reality', 'whom', 'local', 'talking', 'difficult', 'using', 'went', 'writing', 'remember', 'near', 'straight', 'hilarious', 'ago', 'certain', 'ben', 'kid', 'wouldn', 'slow', 'blood', 'mystery', 'complete', 'red', 'popular', 'effective', 'am', 'fast', 'flick', 'due', 'runs', 'gone', 'return', 'presence', 'quality', 'dramatic', 'filmmakers', 'age', 'brothers', 'business', 'general', 'rock', 'sexual', 'present', 'surprisingly', 'anyway', 'uses', '4', 'personal', 'figure', 'smart', 'ways', 'decides', 'annoying', 'begin', 'couldn', 'somewhat', 'shots', 'rich', 'minute', 'law', 'previous', 'jim', 'successful', 'harry', 'water', 'similar', 'absolutely', 'motion', 'former', 'strange', 'came', 'follow', 'read', 'project', 'million', 'secret', 'starring', 'clear', 'familiar', 'romance', 'intelligent', 'third', 'excellent', 'amazing', 'party', 'budget', 'eye', 'actress', 'prison', 'latest', 'means', 'company', 'towards', 'predictable', 'powerful', 'nor', 'bob', 'beyond', 'visual', 'leaves', 'r', 'nature', 'following', 'villain', 'leaving', 'animated', 'low', 'myself', 'b', 'bill', 'sam', 'filled', 'wars', 'questions', 'cinema', 'message', 'box', 'moving', 'herself', 'country', 'usual', 'martin', 'definitely', 'add', 'large', 'clever', 'create', 'felt', 'stories', 'brilliant', 'ones', 'giant', 'situation', 'murphy', 'break', 'opens', 'scary', 'doubt', 'drug', 'bunch', 'thinking', 'solid', 'effect', 'learn', 'move', 'force', 'potential', 'seriously', 'follows', 'above', 'saying', 'huge', 'class', 'plan', 'agent', 'created', 'unlike', 'pay', 'non', 'married', 'mark', 'sweet', 'perfectly', 'ex', 'realize', 'audiences', 'took', 'decent', 'likely', 'dream', 'view', 'scott', 'subject', 'understand', 'happened', 'enjoyable', 'studio', 'immediately', 'open', 'e', 'points', 'heard', 'viewers', 'cameron', 'truman', 'bruce', 'frank', 'private', 'stay', 'fails', 'impossible', 'cold', 'richard', 'overall', 'merely', 'exciting', 'mess', 'chase', 'free', 'ten', 'neither', 'wanted', 'gun', 'appear', 'carter', 'escape', 'ultimately', 'fan', 'inside', 'favorite', 'haven', 'modern', 'l', 'wedding', 'stone', 'trek', 'brought', 'trouble', 'otherwise', 'tim', '5', 'allen', 'bond', 'society', 'liked', 'dumb', 'musical', 'stand', 'political', 'various', 'talented', 'particular', 'west', 'state', 'keeps', 'english', 'silly', 'u', 'situations', 'park', 'teen', 'rating', 'slightly', 'steve', 'truth', 'air', 'element', 'joke', 'spend', 'key', 'biggest', 'members', 'effort', 'government', 'focus', 'eddie', 'soundtrack', 'hands', 'earlier', 'chan', 'purpose', 'today', 'showing', 'memorable', 'six', 'cannot', 'max', 'offers', 'rated', 'mars', 'heavy', 'totally', 'control', 'credit', 'fi', 'woody', 'ideas', 'sci', 'wait', 'sit', 'female', 'ask', 'waste', 'terrible', 'depth', 'simon', 'aspect', 'list', 'mary', 'sister', 'animation', 'entirely', 'fear', 'steven', 'moves', 'actual', 'army', 'british', 'constantly', 'fire', 'convincing', 'setting', 'gave', 'tension', 'street', '8', 'brief', 'ridiculous', 'cinematography', 'typical', 'nick', 'screenwriter', 'ability', 'spent', 'quick', 'violent', 'atmosphere', 'subtle', 'expected', 'fairly', 'seven', 'killing', 'tone', 'master', 'disaster', 'lots', 'thinks', 'song', 'cheap', 'suddenly', 'background', 'club', 'willis', 'whatever', 'highly', 'sees', 'complex', 'greatest', 'impact', 'beauty', 'front', 'humans', 'indeed', 'flat', 'grace', 'wrote', 'amusing', 'ii', 'mike', 'further', 'cute', 'dull', 'minor', 'recently', 'hate', 'outside', 'plenty', 'wish', 'godzilla', 'college', 'titanic', 'sounds', 'telling', 'sight', 'double', 'cinematic', 'queen', 'hold', 'meanwhile', 'awful', 'clearly', 'theme', 'hear', 'x', 'amount', 'baby', 'approach', 'dreams', 'shown', 'island', 'reasons', 'charm', 'miss', 'longer', 'common', 'sean', 'carry', 'believable', 'realistic', 'chemistry', 'possibly', 'casting', 'carrey', 'french', 'trailer', 'tough', 'produced', 'imagine', 'choice', 'ride', 'somewhere', 'hot', 'race', 'road', 'leader', 'thin', 'jerry', 'slowly', 'delivers', 'detective', 'brown', 'jackson', 'member', 'provide', 'president', 'puts', 'asks', 'critics', 'appearance', 'famous', 'okay', 'intelligence', 'energy', 'sent', 'spielberg', 'development', 'etc', 'language', 'blue', 'proves', 'vampire', 'seemingly', 'basic', 'caught', 'decide', 'opportunity', 'incredibly', 'images', 'band', 'j', 'writers', 'knew', 'interested', 'considering', 'boys', 'thanks', 'remains', 'climax', 'event', 'directing', 'conclusion', 'leading', 'ground', 'lies', 'forget', 'alive', 'tarzan', 'century', 'provides', 'trip', 'partner', 'central', 'tarantino', 'period', 'pace', 'yourself', 'worked', 'ready', 'date', 'thus', '1998', 'terrific', 'write', 'average', 'onto', 'songs', 'occasionally', 'doctor', 'stands', 'hardly', 'monster', 'led', 'mysterious', 'details', 'wasted', 'apart', 'aside', 'store', 'billy', 'boss', 'travolta', 'producer', 'pull', 'consider', 'pictures', 'becoming', 'cage', 'loud', 'looked', 'officer', 'twenty', 'system', 'contains', 'julia', 'subplot', 'missing', 'personality', 'building', 'learns', 'hong', 'la', 'apartment', '7', 'bizarre', 'powers', 'flaws', 'catch', 'lawyer', 'shoot', 'student', 'unique', '000', 'admit', 'concept', 'needed', 'thrown', 'christopher', 'laughing', 'green', 'twists', 'matthew', 'touch', 'waiting', 'victim', 'cover', 'machine', 'danny', 'mention', 'search', '1997', 'win', 'door', 'manner', 'train', 'saving', 'share', 'image', 'discovers', 'normal', 'cross', 'fox', 'returns', 'adult', 'adds', 'answer', 'adventure', 'lame', 'male', 'odd', 'singer', 'deserves', 'gore', 'states', 'include', 'equally', 'months', 'barely', 'directors', 'introduced', 'fashion', 'social', '1999', 'news', 'hair', 'dance', 'innocent', 'camp', 'teacher', 'became', 'sad', 'witch', 'includes', 'nights', 'jason', 'julie', 'latter', 'food', 'jennifer', 'land', 'menace', 'rate', 'storyline', 'contact', 'jean', 'elizabeth', 'fellow', 'changes', 'henry', 'hill', 'pulp', 'gay', 'tried', 'surprised', 'literally', 'walk', 'standard', '90', 'forward', 'wise', 'enjoyed', 'discover', 'pop', 'anderson', 'offer', 'recommend', 'public', 'drive', 'c', 'toy', 'charming', 'fair', 'chinese', 'rescue', 'terms', 'mouth', 'lucas', 'accident', 'dies', 'decided', 'edge', 'footage', 'culture', 'weak', 'presented', 'blade', 'younger', 'douglas', 'natural', 'born', 'generally', 'teenage', 'older', 'horrible', 'addition', 'sadly', 'creates', 'disturbing', 'roger', 'detail', 'devil', 'debut', 'track', 'developed', 'week', 'russell', 'attack', 'explain', 'rarely', 'fully', 'prove', 'exception', 'jeff', 'twist', 'gang', 'winning', 'jr', 'species', 'issues', 'fresh', 'rules', 'meaning', 'inspired', 'heroes', 'desperate', 'fighting', 'filmed', 'faces', 'alan', 'bright', 'ass', 'flying', 'kong', 'rush', 'forces', 'charles', 'numerous', 'emotions', 'involves', 'patrick', 'weird', 'apparent', 'information', 'revenge', 'jay', 'toward', 'surprising', 'twice', 'editing', 'calls', 'lose', 'vegas', 'stage', 'intended', 'gags', 'opinion', 'likes', 'crazy', 'owner', 'places', 'pair', 'genuine', 'epic', 'speak', 'throw', 'appeal', 'gibson', 'captain', 'military', '20', 'blair', 'nowhere', 'length', 'nicely', 'cause', 'pass', 'episode', 'kiss', 'arnold', 'please', 'hasn', 'phone', 'filmmaking', 'formula', 'boyfriend', 'talents', 'creating', 'kelly', 'buy', 'wide', 'fantasy', 'mood', 'heads', 'pathetic', 'lacks', 'loved', 'asked', 'mrs', 'witty', 'shakespeare', 'mulan', 'generation', 'affair', 'pieces', 'task', 'rare', 'kept', 'cameo', 'fascinating', 'ed', 'fbi', 'burton', 'incredible', 'accent', 'artist', 'superior', 'academy', 'thomas', 'spirit', 'technical', 'confusing', 'poorly', 'target', 'lover', 'woo', 'mentioned', 'theaters', 'plane', 'confused', 'dennis', 'rob', 'appropriate', 'christmas', 'considered', 'legend', 'shame', 'soul', 'matt', 'campbell', 'process', 'bottom', 'sitting', 'brain', 'creepy', '13', 'forever', 'dude', 'crap', 'superb', 'speech', 'ice', 'journey', 'masterpiece', 'intriguing', 'names', 'pick', 'speaking', 'virtually', 'award', 'worthy', 'marriage', 'deliver', 'cash', 'magic', 'respect', 'product', 'necessary', 'suppose', 'silent', 'pointless', 'station', 'affleck', 'dimensional', 'charlie', 'allows', 'avoid', 'meant', 'cops', 'attitude', 'relationships', 'hits', 'stephen', 'spends', 'relief', 'physical', 'count', 'reviews', 'appreciate', 'cliches', 'holds', 'pure', 'plans', 'limited', 'failed', 'pain', 'impression', 'unless', 'sub', '[', 'total', 'creature', 'viewing', 'loves', 'princess', 'kate', 'rising', 'woods', 'baldwin', 'angry', 'drawn', 'step', 'matrix', 'themes', 'satire', 'arts', ']', 'remake', 'wall', 'moral', 'color', 'ray', 'stuck', 'touching', 'wit', 'tony', 'hanks', 'continues', 'damn', 'nobody', 'cartoon', 'keeping', 'realized', 'criminal', 'unfunny', 'comedic', 'martial', 'disappointing', 'anti', 'graphic', 'stunning', 'actions', 'floor', 'emotion', 'soldiers', 'edward', 'comedies', 'driver', 'expectations', 'added', 'mad', 'angels', 'shallow', 'suspect', 'humorous', 'phantom', 'appealing', 'device', 'design', 'industry', 'reach', 'fat', 'blame', 'united', 'sign', 'portrayal', 'rocky', 'finale', 'grand', 'opposite', 'hotel', 'match', 'damme', 'speed', 'ok', 'loving', 'field', 'larry', 'urban', 'troopers', 'compared', 'apes', 'rose', 'falling', 'era', 'loses', 'adults', 'managed', 'dad', 'therefore', 'pg', 'results', 'guns', 'radio', 'lady', 'manage', 'spice', 'naked', 'started', 'intense', 'humanity', 'wonderfully', 'slasher', 'bland', 'imagination', 'walking', 'willing', 'horse', 'rent', 'mix', 'generated', 'g', 'utterly', 'scientist', 'washington', 'notice', 'players', 'teenagers', 'moore', 'board', 'price', 'frightening', 'tommy', 'spectacular', 'bored', 'jane', 'join', 'producers', 'johnny', 'zero', 'vampires', 'adaptation', 'dollars', 'parody', 'documentary', 'dvd', 'wayne', 'post', 'exist', 'matters', 'chosen', 'mel', 'attractive', 'plain', 'trust', 'safe', 'reading', 'hoping', 'protagonist', 'feelings', 'fate', 'finding', 'feet', 'visuals', 'spawn', 'compelling', 'hall', 'sympathetic', 'featuring', 'difference', 'professional', 'drugs', 'ford', 'shooting', 'gold', 'patch', 'build', 'boat', 'cruise', 'honest', 'media', 'flicks', 'bug', 'bringing', 'dangerous', 'watched', 'grant', 'smile', 'plus', 'shouldn', 'decision', 'visually', 'allow', 'starship', 'roberts', 'dying', 'portrayed', 'turning', 'believes', 'changed', 'shock', 'destroy', '30', 'crowd', 'broken', 'tired', 'fail', 'south', 'died', 'cult', 'fake', 'vincent', 'identity', 'sexy', 'hunt', 'jedi', 'flynt', 'alex', 'engaging', 'serve', 'snake', 'yeah', 'expecting', '100', 'decade', 'ups', 'constant', 'current', 'survive', 'jimmy', 'buddy', 'send', 'brooks', 'goofy', 'likable', 'humour', 'technology', 'files', 'babe', 'aspects', 'presents', 'kills', 'supposedly', 'eight', 'sandler', 'hospital', 'test', 'hidden', 'brian', 'books', 'promise', 'determined', 'professor', 'welcome', 'pleasure', 'succeeds', 'individual', 'annie', 'mob', 'ted', 'virus', 'content', 'gary', 'direct', 'contrived', 'carpenter', 'scale', 'sick', 'nasty', 'conflict', 'haunting', 'ghost', 'filmmaker', 'japanese', 'helps', 'fare', 'lucky', 'ultimate', 'window', 'support', 'goal', 'provided', 'genius', 'winner', 'taylor', 'fantastic', 'faith', 'lynch', 'fit', 'catherine', 'ms', 'paced', 'breaks', 'al', 'frame', 'travel', 'badly', 'available', 'cares', 'reeves', 'crash', 'driving', 'press', 'seagal', 'amy', '9', 'headed', 'instance', 'excuse', 'offensive', 'narrative', 'fault', 'bus', 'f', 'extreme', 'miller', 'guilty', 'grows', 'overly', 'liners', 'forgotten', 'ahead', 'accept', 'porn', 'directly', 'helen', 'began', 'lord', 'folks', 'mediocre', 'bar', 'surface', 'super', 'failure', '6', 'acted', 'quiet', 'laughable', 'sheer', 'security', 'emotionally', 'season', 'stuart', 'jail', 'deals', 'cheesy', 'court', 'beach', 'austin', 'model', 'outstanding', 'substance', 'nudity', 'slapstick', 'joan', 'reveal', 'placed', 'check', 'beast', 'hurt', 'bloody', 'acts', 'fame', 'meeting', 'nuclear', '1996', 'strength', 'center', 'funniest', 'standing', 'damon', 'clich', 'position', 'desire', 'driven', 'seat', 'stock', 'wondering', 'realizes', 'dealing', 'taste', 'routine', 'comparison', 'cinematographer', 'seconds', 'singing', 'gangster', 'responsible', 'football', 'remarkable', 'hunting', 'adams', 'fly', 'suspects', 'treat', 'hopes', 'heaven', 'myers', 'struggle', 'costumes', 'beat', 'happening', 'skills', 'ugly', 'figures', 'thoroughly', 'ill', 'surprises', 'player', 'rival', 'guard', 'anthony', 'strike', 'community', 'streets', 'hopkins', 'ended', 'originally', 'sarah', 'creative', 'characterization', 'thankfully', 'growing', 'sharp', 'williamson', 'eccentric', 'explained', 'hey', 'claire', 'steal', 'inevitable', 'joel', 'core', 'weren', 'sorry', 'built', 'anne', 'breaking', 'villains', 'critic', 'lets', 'visit', 'followed', 'serial', 'value', 'missed', 'oliver', 'hollow', 'sea', 'animal', 'freeman', 'animals', 'crystal', 'sidney', 'lacking', 'students', 'continue', 'extra', 'scorsese', 'church', 'stick', 'explanation', 'below', 'hip', 'quest', 'mistake', 'jump', 'fights', 'cusack', 'included', 'draw', '15', 'games', '1995', 'judge', 'gotten', 'chief', 'derek', 'thirty', 'record', 'everybody', 'veteran', 'develop', 'knowledge', 'serves', 'boogie', 'arrives', 'clooney', 'enter', 'russian', 'obsessed', 'vision', 'screenwriters', 'luck', 'holes', 'religious', 'witness', 'flashbacks', 'heavily', 'frequently', 'capable', 'armageddon', 'pacing', 'rise', 'mainly', 'fill', 'barry', 'schwarzenegger', 'clean', 'previously', 'grow', 'keaton', 'empty', 'synopsis', 'victims', 'adam', 'bed', 'lawrence', 'stallone', 'hunter', 'memory', 'suit', 'bobby', 'tragedy', 'saved', 'spot', 'unexpected', 'encounter', 'hearted', 'bacon', 'disappointment', 'bigger', 'noir', 'nicholson', 'evidence', 'relatively', 'morning', 'andrew', 'range', 'numbers', 'walter', 'vehicle', 'pulled', 'describe', 'cliched', 'sky', 'efforts', 'logic', 'verhoeven', 'assistant', 'existence', 'worker', 'freedom', 'theatre', 'wood', 'warm', 'fish', 'ripley', 'mental', 'study', 'justice', 'cliche', 'foot', 'jonathan', 'grown', 'unnecessary', 'rip', 'learned', 'skin', 'talks', 'ball', 'alice', 'roll', 'weeks', 'jon', 'courtroom', 'positive', 'putting', 'connection', 'london', 'angel', 'contrast', 'exact', 'fifteen', 'eric', 'prince', 'bound', 'traditional', 'regular', 'eve', 'niro', 'las', 'remain', 'anna', 'moved', 'asking', 'genuinely', 'rain', 'path', 'aware', 'causes', 'international', 'naturally', 'bank', 'faced', 'elaborate', 'shocking', 'besides', 'trash', 'paris', 'captured', 'concerned', 'rule', 'held', 'claims', 'cell', 'daniel', 'pilot', 'independence', 'ocean', 'eat', 'punch', 'desperately', 'reminiscent', 'knowing', 'greater', 'largely', 'hundred', 'shrek', 'flash', 'occasional', 'danger', 'thrillers', 'essentially', 'terror', 'whenever', 'suggest', 'baseball', 'blockbuster', 'pie', 'starting', 'satisfying', 'allowed', 'minds', 'neil', 'hank', 'storm', 'disappointed', 'jake', 'wearing', 'explains', 'marry', 'national', 'psychological', 'pig', 'nomination', 'critique', 'theatrical', 'psycho', 'necessarily', 'threatening', 'fallen', 'dogs', 'painful', 'plots', 'sends', 'department', 'agrees', 'league', 'covered', 'source', 'revealed', 'historical', 'perspective', 'patient', '17', 'arquette', 'successfully', 'n', 'afraid', 'mom', 'murders', 'jar', 'suicide', 'joy', 'nightmare', 'halloween', 'cuts', 'wilson', 'nine', '80', 'drunken', 'painfully', 'opera', 'wrestling', 'references', 'cars', 'bomb', 'luke', 'pulls', 'passion', 'sleep', 'structure', 'agree', 'occur', 'brad', 'chicago', 'con', 'attacks', 'service', 'stunts', 'bulworth', 'murray', 'trilogy', 'intensity', 'tradition', 'unfortunate', 'seth', 'stiller', 'suspenseful', 'steals', 'cat', 'investigation', 'lovely', 'stops', 'hanging', 'oddly', 'choices', 'warning', 'climactic', 'ape', 'jungle', 'england', 'sole', 'conspiracy', 'surely', 'author', '50', 'program', 'broderick', 'china', 'weapon', 'unbelievable', 'quaid', 'gross', 'ensemble', 'dinner', 'dirty', 'soft', 'loose', 'memories', 'harris', 'laughter', 'nevertheless', 'suffering', 'initially', 'narration', 'terribly', 'stolen', 'answers', 'wealthy', 'originality', 'reaction', 'foreign', 'significant', 'donnell', 'fu', 'reminded', 'subplots', 'risk', 'creatures', '12', 'african', 'convinced', 'lewis', 'capture', 'makers', 'requires', 'friendship', 'spy', 'met', 'uninteresting', 'christian', 'deadly', 'critical', 'behavior', 'slave', 'thrills', 'duvall', 'segment', 'monkey', 'bitter', 'status', 'refuses', 'nbsp', 'understanding', 'described', 'voiced', 'accidentally', 'endless', 'showed', 'schumacher', 'hired', '2001', 'terry', 'walks', 'li', 'complicated', 'weekend', 'sequels', 'excitement', 'commercial', 'performers', 'rick', 'beloved', 'unlikely', 'bag', 'keanu', 'tight', 'terminator', 'desert', 'german', 'wears', 'effectively', 'flaw', 'meg', 'thoughts', 'scare', 'prime', 'soldier', 'todd', 'suffers', 'greg', 'p', 'shop', 'discovered', 'bear', 'melvin', 'dragon', 'heroine', 'sudden', 'gag', 'killers', 'halfway', 'strikes', 'root', 'handled', 'handle', 'explosions', 'mickey', 'extraordinary', 'sports', 'collection', 'photography', 'speaks', 'issue', 'mid', 'proceedings', 'ethan', 'delightful', 'laughed', 'vacation', 'pitt', 'lebowski', 'lovers', 'quirky', 'texas', 'flesh', 'dean', 'crisis', 'touches', 'crow', 'dollar', 'attempting', 'murdered', '0', 'fugitive', 'values', 'loser', 'unable', 'drunk', 'kung', 'western', 'childhood', 'anywhere', 'gift', 'destroyed', 'chicken', 'tense', 'gonna', 'embarrassing', 'selling', 'sing', 'tragic', 'irritating', 'wind', 'barrymore', 'extended', 'dozen', 'enemy', 'frankly', 'drop', 'norton', 'hype', 'unusual', 'ordinary', 'finest', 'losing', 'ian', 'phil', 'cole', 'goodman', 'insight', 'promising', 'loss', 'weapons', 'twisted', 'deeper', 'nonetheless', 'advice', 'lake', 'campaign', 'lonely', 'karen', 'unknown', 'knock', 'blow', '80s', 'magazine', 'instinct', 'italian', 'throwing', 'costume', 'friendly', 'fairy', 'voices', 'helped', 'lived', 'universe', 'entertain', 'adventures', 'table', 'saturday', 'signs', 'comments', 'required', 'flashback', 'haunted', 'stretch', 'albeit', 'bugs', 'paid', 'soap', 'notes', 'sell', 'multiple', 'practically', 'obligatory']

def load_models(name):
    filepath = os.path.join(os.path.dirname(__file__), "models", f"{name}.pickle")

    with open(filepath, 'rb') as model:
        return pickle.load(model)

loadModels = {
    "KNearest_Neighbors": load_models("KNearest_Neighbors"),
    "Logistic_Regression": load_models("Logistic_Regression"),
    "Naive_Bayes": load_models("Naive_Bayes"),
    "Support_Vector_Classifier": load_models("Support_Vector_Classifier"),
    "Spacy": spacy.load("en_core_web_sm")
}

def find_features(words):
    features = {}
    for word in word_features:
        features[word] = (word in words)

    return features


@clasfier_router.post("/clasfier")
async def clasfier(req: PipelineReq) -> Any:
    model = None

    if req.preprocessor == PreprocessorType.SPACY:
        model = loadModels["Spacy"]
        doc = model(req.input)
        print(preprocess_text_spacy(doc, req.options))
        return preprocess_text_spacy(doc, req.options)

    elif req.preprocessor == PreprocessorType.NLTK:
        model = loadModels[req.models]
        input_text = preprocess_text_nltk(req.input, req.options)
        return model.classify_many(find_features(input_text))
    else:
        raise HTTPException(status_code=400, detail="Preprocessor type invalid")


